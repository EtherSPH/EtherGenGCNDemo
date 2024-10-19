'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 17:55:53
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Simulation(ConfigBase):
    
    def __init__(
        self,
        time_step_ratio: float = 0.1,
        total_time: float = 1.5,
        output_interval: float = 100,
        density_filter_type: str = "delta_sph",
        density_filter_interval: int = 20,
    ) -> None:
        super().__init__()
        self.time_step_ratio: float = time_step_ratio
        self.total_time: float = total_time
        self.output_interval: float = output_interval
        self.density_filter_type: str = density_filter_type
        self.density_filter_interval: int = density_filter_interval
        pass
    
    def getValues(self) -> list:
        return [
            self.getTimeStepRatio(),
            self.getTotalTime(),
            self.getOutputInterval(),
            self.getDensityFilterType(),
            self.getDensityFilterInterval(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "time_step_ratio",
            "total_time",
            "output_interval",
            "density_filter_type",
            "density_filter_interval",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "simulation"
        pass
    
    def getTimeStepRatio(self) -> float:
        return self.time_step_ratio
        pass
    
    def setTimeStepRatio(self, time_step_ratio: float) -> None:
        self.time_step_ratio = time_step_ratio
        pass
    
    def getTotalTime(self) -> float:
        return self.total_time
        pass
    
    def setTotalTime(self, total_time: float) -> None:
        self.total_time = total_time
        pass
    
    def getOutputInterval(self) -> float:
        return self.output_interval
        pass
    
    def setOutputInterval(self, output_interval: float) -> None:
        self.output_interval = output_interval
        pass
    
    def getDensityFilterType(self) -> str:
        return self.density_filter_type
        pass
    
    def setDensityFilterType(self, density_filter_type: str) -> None:
        self.density_filter_type = density_filter_type
        pass
    
    def getDensityFilterInterval(self) -> int:
        return self.density_filter_interval
        pass
    
    def setDensityFilterInterval(self, density_filter_interval: int) -> None:
        self.density_filter_interval = density_filter_interval
        pass
    
    pass