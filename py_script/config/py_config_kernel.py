'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 17:24:09
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Kernel(ConfigBase):
    
    def __init__(
        self,
        type: str = "cubic_spline",
        influence_radius_ratio: float = 2.5
    ) -> None:
        super().__init__()
        self.type: str = type
        self.influence_radius_ratio: float = influence_radius_ratio
        pass
    
    def getValues(self) -> list:
        return [
            self.getType(),
            self.getInfluenceRadiusRatio(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "type",
            "influence_radius_ratio",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "kernel"
        pass
    
    def getType(self) -> str:
        return self.type
        pass
    
    def setType(self, type: str) -> None:
        self.type = type
        pass
    
    
    def getInfluenceRadiusRatio(self) -> float:
        return self.influence_radius_ratio
        pass
    
    def setInfluenceRadiusRatio(self, influence_radius_ratio: float) -> None:
        self.influence_radius_ratio = influence_radius_ratio
        pass
    
    pass