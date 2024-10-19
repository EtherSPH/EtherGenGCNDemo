#=
  @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
  @ date: 2024/09/29 21:02:56
  @ license: MIT
  @ description:
 =#

using EtherSPH
using ProgressBars
using YAML

const config = YAML.load_file("case.yaml")
# const config = YAML.load_file("template/kernel_weighted.yaml")

const dim = config["geometry"]["dimension"]
const dr = config["geometry"]["particle_gap"]
const gap = dr
const h = config["kernel"]["influence_radius_ratio"] * dr
const kernel_type = config["kernel"]["type"]

if kernel_type == "cubic_spline"
    const kernel = CubicSpline{dim}(h)
elseif kernel_type == "wendlandc2"
    const kernel = WendlandC2{dim}(h)
else
    error("Unsupported kernel type: $kernel_type")
end

@inline function W(r::Float64)::Float64
    return kernelValue(r, kernel)
end
@inline function DW(r::Float64)::Float64
    return kernelGradient(r, kernel)
end

const box_start = Point2D(config["geometry"]["box_start"])
const box_end = Point2D(config["geometry"]["box_end"])
const fluid_start = Point2D(config["geometry"]["fluid_start"])
const fluid_end = fluid_start .+ Point2D(config["geometry"]["fluid_shape"] .* dr)
const wall_width = ceil(config["kernel"]["influence_radius_ratio"]) * dr

if all(box_start .<= fluid_start .< fluid_end .<= box_end) == false
    error("Fluid domain is not inside the box, please check the configuration yaml.")
end

const rho_0 = config["global"]["density"]
const mass = rho_0 * dr^dim
const g = Vector2D(config["global"]["gravity"])
const c_0 = config["global"]["sound_speed"]
const c_0_2 = c_0^2
const mu = config["global"]["viscosity"]
const artificial_alpha = config["global"]["artificial_alpha"]
const artificial_beta = config["global"]["artificial_beta"]

const dt = config["simulation"]["time_step_ratio"] * h / c_0
const total_time = config["simulation"]["total_time"]
const output_interval = config["simulation"]["output_interval"]
const density_filter_interval = config["simulation"]["density_filter_interval"]

const FLUID_TAG = config["material"]["fluid"]
const WALL_TAG = config["material"]["wall"]

@inline function eos(rho::Float64)::Float64
    return c_0_2 * (rho - rho_0)
end

@kwdef mutable struct Particle <: AbstractParticle2D
    # must have
    x_vec_::Vector2D = Vector2D(0.0, 0.0)
    rho_::Float64 = rho_0
    mass_::Float64 = mass
    type_::Int64 = FLUID_TAG
    # neighbour info
    neighbour_index_list_::IndexContainer = IndexContainer()
    neighbour_position_list_::Vector2DContainer = Vector2DContainer()
    neighbour_distance_list_::RealNumberContainer = RealNumberContainer()
    # additonal properties
    p_::Float64 = 0.0
    drho_::Float64 = 0.0
    v_vec_::Vector2D = Vector2D(0.0, 0.0)
    dv_vec_::Vector2D = Vector2D(0.0, 0.0)
    c_::Float64 = c_0
    mu_::Float64 = mu
    gap_::Float64 = dr
    sum_kernel_weight_::Float64 = 0.0
    sum_kernel_weighted_rho_::Float64 = 0.0
    sum_kernel_weighted_p_::Float64 = 0.0
end

@inline function continuityAndPressureExpolation!(p::Particle, q::Particle, rpq::Vector2D, r::Float64)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        dw = DW(r)
        EtherSPH.libTraditionalContinuity!(p, q, rpq, r; kernel_gradient = dw)
        return nothing
    elseif p.type_ == FLUID_TAG && q.type_ == WALL_TAG
        dw = DW(r)
        EtherSPH.libBalancedContinuity!(p, q, rpq, r; kernel_gradient = dw)
        return nothing
    elseif p.type_ == WALL_TAG && q.type_ == FLUID_TAG
        w = W(r)
        EtherSPH.libPressureExtrapolationInteraction!(p, q, rpq, r; kernel_value = w, body_force_vec = g)
        return nothing
    end
    return nothing
end

@inline function updateDensityAndPressure!(p::Particle; dt::Float64 = 0.0)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libUpdateDensity!(p; dt = dt)
        p.p_ = eos(p.rho_)
        return nothing
    elseif p.type_ == WALL_TAG
        EtherSPH.libPressureExtrapolationSelfaction!(p)
        return nothing
    end
end

@inline function momentum!(p::Particle, q::Particle, rpq::Vector2D, r::Float64)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        w = W(r)
        rw = W(0.5 * p.gap_ + q.gap_)
        dw = DW(r)
        EtherSPH.libTraditionalPressureForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = dw,
            kernel_value = w,
            reference_kernel_value = rw,
        )
        EtherSPH.libTraditionalViscosityForce!(p, q, rpq, r; kernel_gradient = dw, h = 0.5 * h)
        EtherSPH.libArtificialViscosityForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = dw,
            h = 0.5 * h,
            alpha = artificial_alpha,
            beta = artificial_beta,
        )
        return nothing
    elseif p.type_ == FLUID_TAG && q.type_ == WALL_TAG
        w = W(r)
        rw = W(0.5 * p.gap_ + q.gap_)
        dw = DW(r)
        EtherSPH.libDensityWeightedPressureForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = dw,
            kernel_value = w,
            reference_kernel_value = rw,
        )
        EtherSPH.libTraditionalViscosityForce!(p, q, rpq, r; kernel_gradient = dw, h = 0.5 * h)
        # * apply artificial viscosity only
        EtherSPH.libArtificialViscosityForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = dw,
            h = 0.5 * h,
            alpha = artificial_alpha,
            beta = artificial_beta,
        )
        return nothing
    end
end

@inline function accelerateAndMove!(p::Particle; dt::Float64 = 0.0)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libAccelerateAndMove!(p; dt = dt, body_force_vec = g)
        return nothing
    end
    return nothing
end

@inline function densityFilterInteraction!(p::Particle, q::Particle, rpq::Vector2D, r::Float64)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        EtherSPH.libKernelAverageDensityFilterInteraction!(p, q, rpq, r; kernel_value = W(r))
    end
    return nothing
end

@inline function densityFilterSelfaction!(p::Particle)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libKernelAverageDensityFilterSelfaction!(p; kernel_value = kernel.kernel_value_0_)
    end
    return nothing
end

@inline function modifyFluid!(p::Particle)::Nothing
    p.type_ = FLUID_TAG
    return nothing
end

@inline function modifyWall!(p::Particle)::Nothing
    p.type_ = WALL_TAG
    p.mu_ *= 1e4
    return nothing
end

const fluid_column = Rectangle(fluid_start, fluid_end)

const bottom_wall =
    Rectangle(Point2D(box_start.x - wall_width, box_start.y - wall_width), Point2D(box_end.x + wall_width, box_start.y))
const top_wall =
    Rectangle(Point2D(box_start.x - wall_width, box_end.y), Point2D(box_end.x + wall_width, box_end.y + wall_width))
const left_wall = Rectangle(Point2D(box_start.x - wall_width, box_start.y), Point2D(box_start.x, box_end.y))
const right_wall = Rectangle(Point2D(box_end.x, box_start.y), Point2D(box_end.x + wall_width, box_end.y))

fluid_particles = createParticles(Particle, gap, fluid_column; modify! = modifyFluid!)
bottom_wall_particles = createParticles(Particle, gap, bottom_wall; modify! = modifyWall!)
top_wall_particles = createParticles(Particle, gap, top_wall; modify! = modifyWall!)
left_wall_particles = createParticles(Particle, gap, left_wall; modify! = modifyWall!)
right_wall_particles = createParticles(Particle, gap, right_wall; modify! = modifyWall!)
particles = vcat(fluid_particles, bottom_wall_particles, top_wall_particles, left_wall_particles, right_wall_particles)

system = ParticleSystem(
    Particle,
    h,
    box_start .- Vector2D(wall_width, wall_width),
    box_end .+ Vector2D(wall_width, wall_width),
)
append!(system, particles)

vtp_writer = VTPWriter()
@inline getPressure(p::Particle)::Float64 = p.p_
@inline getVelocity(p::Particle)::Vector2D = p.v_vec_
addScalar!(vtp_writer, "Pressure", getPressure)
addVector!(vtp_writer, "Velocity", getVelocity)
vtp_writer.step_digit_ = config["output"]["step_digit"]
vtp_writer.file_name_ = config["output"]["file_name"]
vtp_writer.output_path_ = config["output"]["output_path"]
if config["output"]["use_name"] == true
    vtp_writer.output_path_ = joinpath(vtp_writer.output_path_, config["info"]["name"])
end

@info vtp_writer

function main()::Nothing
    t = 0.0
    n_steps = round(Int, total_time / dt)
    assurePathExist(vtp_writer)
    saveVTP(vtp_writer, system, 0, t)
    createNeighbourIndexList!(system)
    for step in ProgressBar(1:n_steps)
        applyInteractionWithNeighbours!(system, continuityAndPressureExpolation!)
        applySelfaction!(system, updateDensityAndPressure!; dt = dt)
        applyInteractionWithNeighbours!(system, momentum!)
        applySelfaction!(system, accelerateAndMove!; dt = dt)
        createNeighbourIndexList!(system)
        if step % density_filter_interval == 0
            applyInteractionWithNeighbours!(system, densityFilterInteraction!)
            applySelfaction!(system, densityFilterSelfaction!)
        end
        if step % output_interval == 0
            saveVTP(vtp_writer, system, step, t)
        end
        t += dt
    end
    return nothing
end

@time main()
