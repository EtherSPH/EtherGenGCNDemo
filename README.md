# EtherGenGCNDemo

A repo to generate dataset for graph neural network.

## Setup

```bash
julia
```

```julia
> ] # Enter package mode
> activate . # Activate the environment
> instantiate # Install the dependencies
```

## Usage

1. Modify [`template/xxx.yaml`](template/delta_sph.yaml) to specify the parameters. Or you can create a new yaml file and pass it to the script.
2. Modify [`jl_kernel_weighted.jl`](jl_script/jl_kernel_weighted.jl) to specify the `yaml` file you want to use. The path is relative to the root of the project.
3. Run the script

```bash
julia -t 4 # specify the number of threads
```

In julia REPL

```julia
> ] # Enter package mode
> activate . # Activate the environment
> include("jl_script/jl_kernel_weighted.jl") # Run the script
```
