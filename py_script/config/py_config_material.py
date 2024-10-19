'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 18:10:07
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Material(ConfigBase):
    
    def __init__(
        self,
        fluid: int = 1,
        wall: int = 2
    ) -> None:
        super().__init__()
        self.fluid: int = fluid
        self.wall: int = wall
        pass
    
    def getValues(self) -> list:
        return [
            self.getFluid(),
            self.getWall(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "fluid",
            "wall",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "material"
        pass
    
    def getFluid(self) -> int:
        return self.fluid
        pass
    
    def setFluid(self, fluid: int) -> None:
        self.fluid = fluid
        pass
    
    def getWall(self) -> int:
        return self.wall
        pass
    
    def setWall(self, wall: int) -> None:
        self.wall = wall
        pass
    
    pass