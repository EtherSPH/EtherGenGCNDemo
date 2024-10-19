'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 16:58:22
 # @ license: MIT
 # @ description:
 '''
 
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Geometry(ConfigBase):
    
    def __init__(
        self,
        dimension: int = 2,
        box_start: list = [0.0, 0.0],
        box_end: list = [1.0, 1.0],
        particle_gap: float = 0.01,
        fluid_start: list = [0.0, 0.0],
        fluid_shape: list = [24, 24],
    ) -> None:
        super().__init__()
        self.dimension: int = dimension
        self.box_start: list = box_start
        self.box_end: list = box_end
        self.particle_gap: float = particle_gap
        self.fluid_start: list = fluid_start
        self.fluid_shape: list = fluid_shape
        pass
    
    def getValues(self) -> list:
        return [
            self.getDimension(),
            self.getBoxStart(),
            self.getBoxEnd(),
            self.getParticleGap(),
            self.getFluidStart(),
            self.getFluidShape(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "dimension",
            "box_start",
            "box_end",
            "particle_gap",
            "fluid_start",
            "fluid_shape",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "geometry"
        pass
    
    def getDimension(self) -> int:
        return self.dimension
        pass
    
    def setDimension(self, dimension: int) -> None:
        self.dimension = dimension
        pass
    
    def getBoxStart(self) -> list:
        return self.box_start
        pass
    
    def setBoxStart(self, box_start: list) -> None:
        for i_dim in range(self.dimension):
            self.box_start[i_dim] = box_start[i_dim]
            pass
        pass
    
    def getBoxEnd(self) -> list:
        return self.box_end
        pass
    
    def setBoxEnd(self, box_end: list) -> None:
        for i_dim in range(self.dimension):
            self.box_end[i_dim] = box_end[i_dim]
            pass
        pass
    
    def getParticleGap(self) -> float:
        return self.particle_gap
        pass
    
    def setParticleGap(self, particle_gap: float) -> None:
        self.particle_gap = particle_gap
        pass
    
    def getFluidStart(self) -> list:
        return self.fluid_start
        pass
    
    def setFluidStart(self, fluid_start: list) -> None:
        for i_dim in range(self.dimension):
            self.fluid_start[i_dim] = fluid_start[i_dim]
            pass
        pass
    
    def getFluidShape(self) -> list:
        return self.fluid_shape
        pass
    
    def setFluidShape(self, fluid_shape: list) -> None:
        for i_dim in range(self.dimension):
            self.fluid_shape[i_dim] = fluid_shape[i_dim]
            pass
        pass
    
    pass