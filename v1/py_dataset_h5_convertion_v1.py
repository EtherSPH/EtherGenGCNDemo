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

from py_script.h5_dataset.py_h5_dataset import H5Dataset

if __name__ == "__main__":
    working_directory: str = "datasets/v1"
    h5_dataset: H5Dataset = H5Dataset(working_directory)
    h5_dataset.generateH5File()
    pass