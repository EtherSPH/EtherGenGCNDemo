'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/19 18:03:26
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from py_config_base import ConfigBase

class Output(ConfigBase):
    
    def __init__(
        self,
        output_path: str = "./datasets",
        use_name: bool = True,
        file_name: str = "demo_delta_sph_",
        step_digit: int = 6,
    ) -> None:
        self.output_path: str = output_path
        self.use_name: bool = use_name
        self.file_name: str = file_name
        self.step_digit: int = step_digit
        pass
    
    def getValues(self) -> list:
        return [
            self.getOutputPath(),
            self.getUseName(),
            self.getFileName(),
            self.getStepDigit(),
        ]
        pass
    
    def getKeys(self) -> list:
        return [
            "output_path",
            "use_name",
            "file_name",
            "step_digit",
        ]
        pass
    
    def getKeyName(self) -> str:
        return "output"
        pass
    
    def getOutputPath(self) -> str:
        return self.output_path
        pass
    
    def setOutputPath(self, output_path: str) -> None:
        self.output_path = output_path
        pass
    
    def getUseName(self) -> bool:
        return self.use_name
        pass
    
    def setUseName(self, use_name: bool) -> None:
        self.use_name = use_name
        pass
    
    def getFileName(self) -> str:
        return self.file_name
        pass
    
    def setFileName(self, file_name: str) -> None:
        self.file_name = file_name
        pass
    
    def getStepDigit(self) -> int:
        return self.step_digit
        pass
    
    def setStepDigit(self, step_digit: int) -> None:
        self.step_digit = step_digit
        pass
    
    pass