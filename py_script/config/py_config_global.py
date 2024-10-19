'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 17:02:03
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Global(ConfigBase):
    
    def __init__(
        self,
        density: float = 1.0,
        gravity: list = [0.0, -8.0],
        viscosity: float = 1e-6,
        estimated_max_velocity: float = 4.0, # \sqrt{2gh}
        sound_speed: float = 50.0,
        delta_sph_coefficient: float = 0.1,
        artificial_alpha: float = 0.1,
        artificial_beta: float = 0.1
    ) -> None:
        super().__init__()
        self.density: float = density
        self.gravity: list = gravity
        self.viscosity: float = viscosity
        self.estimated_max_velocity: float = estimated_max_velocity
        self.sound_speed: float = sound_speed
        self.delta_sph_coefficient: float = delta_sph_coefficient
        self.artificial_alpha: float = artificial_alpha
        self.artificial_beta: float = artificial_beta
        pass
    
    def getValues(self) -> list:
        return [
            self.getDensity(),
            self.getGravity(),
            self.getViscosity(),
            self.getEstimatedMaxVelocity(),
            self.getSoundSpeed(),
            self.getDeltaSphCoefficient(),
            self.getArtificialAlpha(),
            self.getArtificialBeta(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "density",
            "gravity",
            "viscosity",
            "estimated_max_velocity",
            "sound_speed",
            "delta_sph_coefficient",
            "artificial_alpha",
            "artificial_beta",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "global"
        pass
    
    def getDensity(self) -> float:
        return self.density
        pass
    
    def setDensity(self, density: float) -> None:
        self.density = density
        pass
    
    def getGravity(self) -> list:
        return self.gravity
        pass
    
    def setGravity(self, gravity: list) -> None:
        for i_dim in range(len(gravity)):
            self.gravity[i_dim] = gravity[i_dim]
            pass
        pass
    
    def getViscosity(self) -> float:
        return self.viscosity
        pass
    
    def setViscosity(self, viscosity: float) -> None:
        self.viscosity = viscosity
        pass
    
    def getEstimatedMaxVelocity(self) -> float:
        return self.estimated_max_velocity
        pass
    
    def setEstimatedMaxVelocity(self, estimated_max_velocity: float) -> None:
        self.estimated_max_velocity = estimated_max_velocity
        pass
    
    def getSoundSpeed(self) -> float:
        return self.sound_speed
        pass
    
    def setSoundSpeed(self, sound_speed: float) -> None:
        self.sound_speed = sound_speed
        pass
    
    def getDeltaSphCoefficient(self) -> float:
        return self.delta_sph_coefficient
        pass
    
    def setDeltaSphCoefficient(self, delta_sph_coefficient: float) -> None:
        self.delta_sph_coefficient = delta_sph_coefficient
        pass
    
    def getArtificialAlpha(self) -> float:
        return self.artificial_alpha
        pass
    
    def setArtificialAlpha(self, artificial_alpha: float) -> None:
        self.artificial_alpha = artificial_alpha
        pass
    
    def getArtificialBeta(self) -> float:
        return self.artificial_beta
        pass
    
    def setArtificialBeta(self, artificial_beta: float) -> None:
        self.artificial_beta = artificial_beta
        pass
    
    pass