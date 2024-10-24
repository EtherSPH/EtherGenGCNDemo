"""
# Author: Xu Ran
# Date: 2024-10-21 21:39:14
# LastEditors: Xu Ran
# LastEditTime: 2024-10-24 12:21:38
# Description: 
"""
'''
 # @ author: bcynuaa <bcynuaa@163.com> | vox-1 <xur2006@163.com>
 # @ date: 2024/10/20 22:01:06
 # @ license: MIT
 # @ description:
 '''

import h5py
import yaml
import pprint
import numpy as np

h5_file_name: str = "datasets/v1/v1.hdf5"

with h5py.File(h5_file_name, "r") as h5_file:
    # keys length is the total case number
    print(f"Total case number: {len(h5_file.keys())}")
    print(f"Keys: {list(h5_file.keys())}")
    # let's take case_00 as an example
    # `config` `sequence`
    case_0 = h5_file["case_00"]
    print(f"case_00 keys: {list(case_0.keys())}")
    # let's read config first
    case_0_config = case_0["config"]
    case_0_config_dict = yaml.safe_load(case_0_config[()])
    print(f"case_00 config: {type(case_0_config_dict)}")
    pprint.pprint(case_0_config_dict)
    # for k,v in case_0.attrs.items():
    #     print(f'{k}: {v}')
    # let's read sequence
    case_0_sequence = case_0["sequence"]
    case_0_sequence_np = np.array(case_0_sequence)
    print(f"case_00 sequence (time_step, particle_number, particle_feature)")
    print(f"case_00 sequence shape: {case_0_sequence_np.shape}")
    pass