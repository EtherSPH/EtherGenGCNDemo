'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/20 17:14:07
 # @ license: MIT
 # @ description:
 '''
 
import os
import h5py
import numpy as np
import pyvista as pv
import yaml
import tqdm

class H5Dataset:
    
    def __init__(
        self,
        working_directory: str,
    ) -> None:
        self.setWorkingDirectory(working_directory)
        pass
    
    def setWorkingDirectory(self, working_directory: str) -> None:
        self.working_directory = working_directory
        self.case_folder_list: list = os.listdir(working_directory)
        self.case_folder_list = [folder for folder in self.case_folder_list if os.path.isdir(os.path.join(working_directory, folder))]
        self.case_folder_list.sort()
        pass
    
    def getWorkingDirectory(self) -> str:
        return self.working_directory
        pass
    
    def getCaseFolder(self, index: int) -> str:
        return os.path.join(self.working_directory, self.case_folder_list[index])
        pass
    
    def getH5FileName(self) -> str:
        folder_basename: str = os.path.basename(self.working_directory)
        return os.path.join(self.working_directory, f"{folder_basename}.hdf5")
        pass
    
    def getSingleCaseSingleStepFeatures(self, vtp_file_name: str) -> np.ndarray:
        poly_data: pv.PolyData = pv.read(vtp_file_name)
        x, y, _ = poly_data.points.T
        u, v = poly_data.point_data["Velocity"].T
        rho = poly_data.point_data["Density"]
        p = poly_data.point_data["Pressure"]
        return np.array([x, y, u, v, rho, p]).T
        pass
    
    def readSingleCase(self, case_folder: str) -> tuple:
        file_list: list = os.listdir(case_folder)
        yaml_file: str = [file for file in file_list if file.endswith(".yaml")][0]
        with open(os.path.join(case_folder, yaml_file), "r") as f:
            yaml_dict: dict = yaml.load(f, Loader=yaml.FullLoader)
            yaml_str: str = yaml.dump(yaml_dict)
            pass
        file_list: list = [file for file in file_list if file.endswith(".vtp")]
        file_list.sort()
        features_list: list = []
        for vtp_file_name in file_list:
            features: np.ndarray = self.getSingleCaseSingleStepFeatures(os.path.join(case_folder, vtp_file_name))
            features_list.append(features)
            pass
        features_array: np.ndarray = np.array(features_list)
        return yaml_str, features_array
        pass
    
    def generateH5File(self) -> None:
        h5_file_name: str = self.getH5FileName()
        with h5py.File(h5_file_name, "w") as f:
            for i_case in tqdm.tqdm(range(len(self.case_folder_list))):
                case_folder: str = self.getCaseFolder(i_case)
                yaml_str, features_array = self.readSingleCase(case_folder)
                group = f.create_group(f"{os.path.basename(case_folder)}")
                group.create_dataset("config", data=yaml_str)
                group.create_dataset("sequence", data=features_array)
                pass
            pass
        pass
    
    pass