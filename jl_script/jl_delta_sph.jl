#=
  @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
  @ date: 2024/10/19 00:48:15
  @ license: MIT
  @ description:
 =#

using EtherSPH
using ProgressBars
using YAML

const config = YAML.load_file("case.yaml")
# const config = YAML.load_file("template/delta_sph.yaml")

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
const delta_sph_coefficient = config["global"]["delta_sph_coefficient"]
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
    neighbour_kernel_gradient_list_::RealNumberContainer = RealNumberContainer()
    # additonal properties
    p_::Float64 = 0.0
    drho_::Float64 = 0.0
    v_vec_::Vector2D = Vector2D(0.0, 0.0)
    dv_vec_::Vector2D = Vector2D(0.0, 0.0)
    c_::Float64 = c_0
    mu_::Float64 = mu
    gap_::Float64 = dr
    # * pressure extrapolation
    sum_kernel_weight_::Float64 = 0.0
    sum_kernel_weighted_p_::Float64 = 0.0
    # * δ SPH
    corrected_mat_::Matrix2D = Matrix2D(0.0, 0.0, 0.0, 0.0) # Lᵢ
    corrected_density_gradient_vec_::Vector2D = Vector2D(0.0, 0.0) # ∇ρᵢ
end

# ! for speed issue, neighbour kenel gradient is stored
@inline function findNeighbourKernelGradientSelfaction!(p::Particle)::Nothing
    reset!(p.neighbour_kernel_gradient_list_)
    @simd for i_neighbour in eachindex(p.neighbour_index_list_)
        @inbounds kernel_gradient = DW(p.neighbour_distance_list_[i_neighbour])
        push!(p.neighbour_kernel_gradient_list_, kernel_gradient)
    end
    return nothing
end

@inline function continuity!(
    p::Particle,
    q::Particle,
    rpq::Vector2D,
    r::Float64;
    kernel_gradient::Float64 = 0.0,
)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        EtherSPH.libTraditionalContinuity!(p, q, rpq, r; kernel_gradient = kernel_gradient)
        return nothing
    elseif p.type_ == FLUID_TAG && q.type_ == WALL_TAG
        EtherSPH.libBalancedContinuity!(p, q, rpq, r; kernel_gradient = kernel_gradient)
        return nothing
    end
    return nothing
end

@inline function deltaSPHStep1!(p::Particle)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libDeltaSPHClear!(p)
        return nothing
    end
    return nothing
end

@inline function deltaSPHStep2!(
    p::Particle,
    q::Particle,
    rpq::Vector2D,
    r::Float64;
    kernel_gradient::Float64 = 0.0,
)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        EtherSPH.libDeltaSPHGatherCorrectedMatrix!(p, q, rpq, r; kernel_gradient = kernel_gradient)
        return nothing
    end
    return nothing
end

@inline function deltaSPHStep3!(p::Particle)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libDeltaSPHGenerateCorrectedMatrix!(p)
        return nothing
    end
    return nothing
end

@inline function deltaSPHStep4!(
    p::Particle,
    q::Particle,
    rpq::Vector2D,
    r::Float64;
    kernel_gradient::Float64 = 0.0,
)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        EtherSPH.libDeltaSPHGatherDensityGradientVector!(p, q, rpq, r; kernel_gradient = kernel_gradient)
        return nothing
    end
    return nothing
end

@inline function deltaSPHStep5!(
    p::Particle,
    q::Particle,
    rpq::Vector2D,
    r::Float64;
    kernel_gradient::Float64 = 0.0,
)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        EtherSPH.libDeltaSPHDiffusiveFilter!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = kernel_gradient,
            delta_sph_coefficient = delta_sph_coefficient,
            h = h,
            sound_speed = c_0,
        )
        return nothing
    end
    return nothing
end

@inline function updateDensityAndPressure!(p::Particle; dt::Float64 = 0.0)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libUpdateDensity!(p; dt = dt)
        p.p_ = eos(p.rho_)
        return nothing
    end
    return nothing
end

@inline function pressureExtrapolationInteraction!(p::Particle, q::Particle, rpq::Vector2D, r::Float64;)::Nothing
    if p.type_ == WALL_TAG && q.type_ == FLUID_TAG
        w = W(r)
        EtherSPH.libPressureExtrapolationInteraction!(p, q, rpq, r; kernel_value = w, body_force_vec = g)
        return nothing
    end
    return nothing
end

@inline function pressureExtrapolationSelfaction!(p::Particle)::Nothing
    if p.type_ == WALL_TAG
        EtherSPH.libPressureExtrapolationSelfaction!(p;)
        return nothing
    end
    return nothing
end

@inline function momentum!(p::Particle, q::Particle, rpq::Vector2D, r::Float64; kernel_gradient::Float64 = 0.0)::Nothing
    if p.type_ == FLUID_TAG && q.type_ == FLUID_TAG
        w = W(r)
        rw = W(0.5 * p.gap_ + q.gap_)
        EtherSPH.libTraditionalPressureForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = kernel_gradient,
            kernel_value = w,
            reference_kernel_value = rw,
        )
        EtherSPH.libTraditionalViscosityForce!(p, q, rpq, r; kernel_gradient = kernel_gradient, h = 0.0 * h)
        # * apply artificial viscosity only
        EtherSPH.libArtificialViscosityForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = kernel_gradient,
            h = 0.5 * h,
            alpha = artificial_alpha,
            beta = artificial_beta,
        )
        return nothing
    elseif p.type_ == FLUID_TAG && q.type_ == WALL_TAG
        w = W(r)
        rw = W(0.5 * p.gap_ + q.gap_)
        EtherSPH.libDensityWeightedPressureForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = kernel_gradient,
            kernel_value = w,
            reference_kernel_value = rw,
        )
        EtherSPH.libTraditionalViscosityForce!(p, q, rpq, r; kernel_gradient = kernel_gradient, h = 0.0 * h)
        # * apply artificial viscosity only
        EtherSPH.libArtificialViscosityForce!(
            p,
            q,
            rpq,
            r;
            kernel_gradient = kernel_gradient,
            h = 0.5 * h,
            alpha = artificial_alpha,
            beta = artificial_beta,
        )
        return nothing
    end
    return nothing
end

@inline function accelerateAndMove!(p::Particle; dt::Float64 = 0.0)::Nothing
    if p.type_ == FLUID_TAG
        EtherSPH.libAccelerateAndMove!(p; dt = dt, body_force_vec = g)
        return nothing
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

# * main loop
function main()::Nothing
    t = 0.0
    n_steps = round(Int, total_time / dt)
    assurePathExist(vtp_writer)
    saveVTP(vtp_writer, system, 0, t)
    createNeighbourIndexList!(system)
    applySelfaction!(system, findNeighbourKernelGradientSelfaction!)
    for step in ProgressBar(1:n_steps)
        applyInteractionByKernelGradient!(system, continuity!)
        applySelfaction!(system, deltaSPHStep1!)
        applyInteractionByKernelGradient!(system, deltaSPHStep2!)
        applySelfaction!(system, deltaSPHStep3!)
        applyInteractionByKernelGradient!(system, deltaSPHStep4!)
        applyInteractionByKernelGradient!(system, deltaSPHStep5!)
        applySelfaction!(system, updateDensityAndPressure!; dt = dt) # update the density and pressure
        applyInteractionWithNeighbours!(system, pressureExtrapolationInteraction!)
        applySelfaction!(system, pressureExtrapolationSelfaction!)
        applyInteractionByKernelGradient!(system, momentum!) # calculate the momentum
        applySelfaction!(system, accelerateAndMove!; dt = dt) # accelerate and move
        createNeighbourIndexList!(system) # create neighbour index list
        applySelfaction!(system, findNeighbourKernelGradientSelfaction!)
        if step % output_interval == 0
            saveVTP(vtp_writer, system, step, t)
        end
        t += dt
    end
    return nothing
end

@time main()
