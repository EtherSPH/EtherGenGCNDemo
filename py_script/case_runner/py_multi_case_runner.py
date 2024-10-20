'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/20 00:15:12
 # @ license: MIT
 # @ description:
 '''
 
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from config.py_config import Config
from py_single_case_runner import SingleCaseRunner

class MultiCaseRunnerBase:
    
    def __init__(
        self,
        working_directory: str="dataset",
        case_typical_name: str="case",
        file_name: str="step_",
        digit_number: int=4
    ) -> None:
        self.setWorkingDirectory(working_directory)
        self.setCaseTypicalName(case_typical_name)
        self.setFileName(file_name)
        self.setDigitNumber(digit_number)
        pass
    
    def getWorkingDirectory(self) -> str:
        return self.working_directory
        pass
    
    def setWorkingDirectory(self, working_directory: str) -> None:
        self.working_directory = working_directory
        if not os.path.exists(working_directory):
            os.makedirs(working_directory)
            pass
        pass
    
    def getCaseTypicalName(self) -> str:
        return self.case_typical_name
        pass
    
    def setCaseTypicalName(self, case_typical_name: str) -> None:
        self.case_typical_name = case_typical_name
        pass
    
    def getCaseName(self, index: int) -> str:
        return f"{self.getCaseTypicalName()}_{index:0{self.getDigitNumber()}d}"
        pass
    
    def getCasePath(self, index: int) -> str:
        return os.path.join(self.getWorkingDirectory(), self.getCaseName(index))
        pass
    
    def getFileName(self) -> str:
        return self.file_name
        pass
    
    def setFileName(self, file_name: str) -> None:
        self.file_name = file_name
        pass
    
    def getDigitNumber(self) -> int:
        return self.digit_number
        pass
    
    def setDigitNumber(self, digit_number: int) -> None:
        self.digit_number = digit_number
        pass
    
    def generateConfig(self, index: int) -> Config:
        config: Config = Config()
        config.getInfo().setName(self.getCaseName(index))
        config.getOutput().setOutputPath(self.getWorkingDirectory())
        config.getOutput().setFileName(self.getFileName())
        return config
        pass
    
    def run(self, config: Config) -> None:
        runner: SingleCaseRunner = SingleCaseRunner(config)
        runner.run()
        pass
    
    pass