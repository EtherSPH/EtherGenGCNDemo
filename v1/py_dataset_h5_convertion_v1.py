'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/20 17:38:30
 # @ license: MIT
 # @ description:
 '''

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pyvista as pv

from py_script.h5_dataset.py_h5_dataset import H5Dataset

FLUID_TAG: int = 1

class H5DatasetV1(H5Dataset):
    
    def __init__(
        self,
        working_directory: str,
    ) -> None:
        super().__init__(working_directory)
        pass
    
    def getPolyData(self, vtp_file_name) -> pv.PolyData:
        poly_data: pv.PolyData =  super().getPolyData(vtp_file_name)
        type_array: np.ndarray = poly_data.point_data["Type"]
        fluid_mask: np.ndarray = type_array == FLUID_TAG
        return poly_data.extract_points(fluid_mask)
        pass
    
    pass

if __name__ == "__main__":
    working_directory: str = "datasets/v1"
    h5_dataset_v1: H5DatasetV1 = H5DatasetV1(working_directory)
    h5_dataset_v1.generateH5File()
    pass