'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 16:01:32
 # @ license: MIT
 # @ description:
 '''

import subprocess

# julia -t 32 -O3 --math-mode=fast --project=. run_delta_sph.jl

subprocess.run(["julia", "-t", "32", "-O3", "--math-mode=fast", "--project=.", "jl_script/jl_delta_sph.jl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)