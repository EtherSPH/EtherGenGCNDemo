'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/12/14 15:09:06
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pyvista as pv
import pandas as pd
import pprint

from py_script.config.py_config import Config
from py_script.case_runner.py_multi_case_runner import MultiCaseRunnerBase

class DatasetGeneratorV2(MultiCaseRunnerBase):
    
    def __init__(
        self,
        working_directory: str = "datasets/v2",
        case_typical_name: str = "case",
        file_name: str = "step_",
        digit_number: int = 2
    ) -> None:
        super().__init__(working_directory, case_typical_name, file_name, digit_number)
        self.fluid_shape_list: np.array = np.array([
            [24, 24],
            [12, 48],
            [48, 12],
            [16, 36],
            [36, 16],
            [8, 72],
            [72, 8],
        ], dtype=int)
        self.partical_gap: float = 0.01
        self.fluid_start_point_list: np.array = np.array([
            [0.0, 0.0],
            [0.1, 0.0],
            [0.2, 0.0],
            [0.3, 0.0],
            [0.4, 0.0],
            [0.5, 0.0],
        ], dtype=float)
        self.n_shape: int = self.fluid_shape_list.shape[0]
        self.n_start_point: int = self.fluid_start_point_list.shape[0]
        self.case_number: int = self.n_shape * self.n_start_point
        self.case_data_frame: pd.DataFrame = pd.DataFrame(
            columns=[
                "case_id",
                "fluid_start_x", "fluid_start_y",
                "fluid_shape_x", "fluid_shape_y",
                "start_particles_number", "end_particles_number"
            ]
        )
        pass
    
    def linearIndexToBinaryIndex(self, linear_index: int) -> tuple:
        return linear_index // self.n_start_point, linear_index % self.n_start_point
        pass
    
    def binaryIndexToLinearIndex(self, binary_index: tuple) -> int:
        return binary_index[0] * self.n_start_point + binary_index[1]
        pass
    
    def getParticleNumber(self, file_name: str) -> int:
        return pv.read(file_name).n_points
        pass
    
    def generateCaseConfig(self, case_id: int) -> Config:
        config: Config = self.generateConfig(case_id)
        shape_index, start_point_index = self.linearIndexToBinaryIndex(case_id)
        config.getGeometry().setFluidShape(self.fluid_shape_list[shape_index].tolist())
        config.getGeometry().setFluidStart(self.fluid_start_point_list[start_point_index].tolist())
        config.getGlobal().setArtificialAlpha(0.2)
        config.getGlobal().setArtificialBeta(0.2)
        return config
        pass
    
    def runSingleCase(self, case_id: int) -> None:
        config: Config = self.generateCaseConfig(case_id)
        if os.path.exists(config.getResultFolder()):
            if len(os.listdir(config.getResultFolder())) > 1:
                pass
            pass
        else:
            self.run(config)
            pass
        result_file_list: list = os.listdir(config.getResultFolder())
        result_file_list = [file for file in result_file_list if file.endswith(".vtp")]
        result_file_list.sort()
        start_particles_number: int = self.getParticleNumber(os.path.join(config.getResultFolder(), result_file_list[0]))
        end_particles_number: int = self.getParticleNumber(os.path.join(config.getResultFolder(), result_file_list[-1]))
        case_info: dict = {
            "case_id": case_id,
            "fluid_start_x": config.getGeometry().getFluidStart()[0],
            "fluid_start_y": config.getGeometry().getFluidStart()[1],
            "fluid_shape_x": config.getGeometry().getFluidShape()[0],
            "fluid_shape_y": config.getGeometry().getFluidShape()[1],
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
            if case_id >= 39:
                break
                pass
            self.runSingleCase(case_id)
            pass
        self.saveCaseData()
        pass
    
    pass

if __name__ == "__main__":
    data_gen = DatasetGeneratorV2()
    data_gen.runAllCases()
    pass