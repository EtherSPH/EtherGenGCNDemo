'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 19:46:20
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

import yaml

from py_config_base import ConfigBase
from py_config_info import Info
from py_config_geometry import Geometry
from py_config_global import Global
from py_config_kernel import Kernel
from py_config_simulation import Simulation
from py_config_output import Output
from py_config_material import Material

class Config(ConfigBase):
    
    def __init__(
        self,
        template_yaml_file_name: str = "template/delta_sph.yaml",
        file_name: str = "case.yaml",
    ) -> None:
        self.file_name: str = file_name
        self.template_yaml_file_name: str = template_yaml_file_name
        self.loadConfig()
        pass
    
    def loadConfig(self) -> dict:
        with open(self.template_yaml_file_name, "r", encoding="utf-8") as file:
            self.config_dict: dict = yaml.load(file, Loader=yaml.FullLoader)
            pass
        self.info: Info = Info(
            **self.config_dict["info"]
        )
        self.geometry: Geometry = Geometry(
            **self.config_dict["geometry"]
        )
        self.global_: Global = Global(
            **self.config_dict["global"]
        )
        self.kernel: Kernel = Kernel(
            **self.config_dict["kernel"]
        )
        self.simulation: Simulation = Simulation(
            **self.config_dict["simulation"]
        )
        self.output: Output = Output(
            **self.config_dict["output"]
        )
        self.material: Material = Material(
            **self.config_dict["material"]
        )
        pass
    
    def getInfo(self) -> Info:
        return self.info
        pass
    
    def getGeometry(self) -> Geometry:
        return self.geometry
        pass
    
    def getGlobal(self) -> Global:
        return self.global_
        pass
    
    def getKernel(self) -> Kernel:
        return self.kernel
        pass
    
    def getSimulation(self) -> Simulation:
        return self.simulation
        pass
    
    def getOutput(self) -> Output:
        return self.output
        pass
    
    def getMaterial(self) -> Material:
        return self.material
        pass
    
    def getKeys(self) -> list:
        return [item.getKeyName() for item in [
            self.getInfo(),
            self.getGeometry(),
            self.getGlobal(),
            self.getKernel(),
            self.getSimulation(),
            self.getOutput(),
            self.getMaterial(),
        ]]
        pass
    
    def getValues(self) -> list:
        return [item.getDict() for item in [
            self.getInfo(),
            self.getGeometry(),
            self.getGlobal(),
            self.getKernel(),
            self.getSimulation(),
            self.getOutput(),
            self.getMaterial(),
        ]]
        pass
    
    def getKeyName(self) -> str:
        return self.file_name
        pass
    
    def writeCase(self) -> None:
        case_file_name, config_dict = self()
        with open(case_file_name, "w", encoding="utf-8") as file:
            yaml.dump(config_dict, file, sort_keys=False, line_break="\n")
            pass
        pass
    
    def getCaseName(self) -> str:
        return self.getKeyName()
        pass
    
    def getResultFolder(self) -> str:
        if self.output.getUseName() == True:
            return os.path.join(
                self.output.getOutputPath(),
                self.info.getName(),
            )
            pass
        else:
            return self.output.getOutputPath()
            pass
        pass
    
    def getScriptName(self) -> None:
        script_map_dict: dict = {
            "delta_sph": "jl_script/jl_delta_sph.jl",
            "kernel_weighted": "jl_script/jl_kernel_weighted.jl",
        }
        return script_map_dict[self.getSimulation().getDensityFilterType()]
        pass
    
    pass