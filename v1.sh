# you need:
# julia environment with `Project.toml`'s environment prepared
# python environment with `requirements.txt`'s environment prepared
# `julia` and `python` in your PATH

# generate the data
python v1/py_dataset_generator_v1.py # this step is time consuming

# convert the data to hdf5
python v1/py_dataset_h5_convertion_v1.py # this step takes several seconds

# read the data's demo
python v1/py_read_demo_v1.py