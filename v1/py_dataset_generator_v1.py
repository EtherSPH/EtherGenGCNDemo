'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/20 14:45:52
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pprint
import numpy as np
import pandas as pd
import pyvista as pv

from py_script.config.py_config import Config
from py_script.case_runner.py_multi_case_runner import MultiCaseRunnerBase

class DatasetGeneratorV1(MultiCaseRunnerBase):
    
    def __init__(
        self,
        working_directory: str = "datasets/v1",
        case_typical_name: str = "case",
        file_name: str = "step_",
        digit_number: int = 2
    ) -> None:
        super().__init__(working_directory, case_typical_name, file_name, digit_number)
        self.fluid_shape: list = [24, 24]
        self.particle_gap: float = 0.01
        self.fluid_start_x_min: float = 0.0
        self.fluid_start_x_max: float = 1.0 - self.fluid_shape[0] * self.particle_gap
        self.fluid_start_y_min: float = 0.0
        self.fluid_start_y_max: float = 1.0 - self.fluid_shape[1] * self.particle_gap
        self.fluid_start_x: np.ndarray = np.linspace(self.fluid_start_x_min, self.fluid_start_x_max, 5)
        self.fluid_start_y: np.ndarray = np.linspace(self.fluid_start_y_min, self.fluid_start_y_max, 5)
        self.case_number: int = len(self.fluid_start_x) * len(self.fluid_start_y)
        # for in simulation, some numerical instability may occur
        # resulting the number of particles in the fluid domain is not exactly the same
        # these cases should be excluded
        self.case_data_frame: pd.DataFrame = pd.DataFrame(columns=["case_id", "fluid_start_x", "fluid_start_y", "start_particles_number", "end_particles_number"])
        pass
    
    def getCaseFluidStartPoint(self, case_id: int) -> tuple:
        x_index: int = case_id // len(self.fluid_start_y)
        y_index: int = case_id % len(self.fluid_start_y)
        return float(self.fluid_start_x[x_index]), float(self.fluid_start_y[y_index])
        pass
    
    def getParticleNumber(self, file_name: str) -> int:
        return pv.read(file_name).n_points
        pass
    
    def runSingleCase(self, case_id: int) -> None:
        config: Config = self.generateConfig(case_id)
        start_x, start_y = self.getCaseFluidStartPoint(case_id)
        config.getGeometry().setFluidStart([start_x, start_y])
        config.getGlobal().setArtificialAlpha(0.2) # 0.1 will meet numerical instability
        config.getGlobal().setArtificialBeta(0.2) # 0.1 will meet numerical instability
        self.run(config)
        result_file_list: list = os.listdir(config.getResultFolder())
        result_file_list = [file for file in result_file_list if file.endswith(".vtp")]
        result_file_list.sort()
        start_particles_number: int = self.getParticleNumber(os.path.join(config.getResultFolder(), result_file_list[0]))
        end_particles_number: int = self.getParticleNumber(os.path.join(config.getResultFolder(), result_file_list[-1]))
        case_info: dict = {
            "case_id": case_id,
            "fluid_start_x": start_x,
            "fluid_start_y": start_y,
            "start_particles_number": start_particles_number,
            "end_particles_number": end_particles_number
        }
        pprint.pprint(case_info)
        self.case_data_frame = pd.concat([self.case_data_frame, pd.DataFrame([case_info])], ignore_index=True)
        self.saveCaseData()
        pass
    
    def saveCaseData(self) -> None:
        self.case_data_frame.to_csv(os.path.join(self.getWorkingDirectory(), "case_data.csv"), index=False)
        pass
    
    def runAllCases(self) -> None:
        for case_id in range(self.case_number):
            self.runSingleCase(case_id)
            pass
        self.saveCaseData()
        pass
    
    pass

if __name__ == "__main__":
    dataset_generator = DatasetGeneratorV1()
    dataset_generator.runAllCases()
    pass