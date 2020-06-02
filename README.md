# On the Jetson Nano, place the files in the following path:  
**Note:** a `models` folder is also required. It can be downloaded [here](https://1drv.ms/u/s!AlG0FKaSj9fe3Eau4bCdaAzXpJZI?e=hp4BPO). It should also be placed in this path.  
`/home/dlinano/nvdli-nano/`

# Dependencies:
- Tensorflow
- pynetworktables
- CUDA 10.2
- OpenCV

# How to install dependencies on the Jetson Nano:
# 1. Tensorflow
Tensorflow was installed using [Nvidia's guide](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html)

Download Tensorflow's dependencies:  
`$ sudo apt-get update`  
`$ sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran`

Install pip3 package manager:  
`$ sudo apt-get install python3-pip`  
`$ sudo pip3 install -U pip testresources setuptools`

Install verified working versions of dependencies:  
`$ sudo pip3 install -U numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11`

Install Tensorflow:  
`$ sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 tensorflow`

# 2. NetworkTables
Install [pynetworktables](https://github.com/robotpy/robotpy-docs/blob/55e7ab2427824d4c8af3740c3a178e373e4f6ede/install/pynetworktables.rst) using pip:  
`$ pip3 install pynetworktables`


# 3. CUDA 10.2 (arm64)
Option 1: Download from [Nvidia](https://developer.nvidia.com/cuda-toolkit/arm) (use Toolkit for Ubuntu 18.04 LTS)  
Option 2: Download [deb package](https://1drv.ms/u/s!AlG0FKaSj9fegbJpzJOs8CaZJK6fKA?e=EquCLp) and install using Ubuntu Software Center or Synaptics

# 4. OpenCV
Install [OpenCV](https://github.com/opencv/opencv) using pip:  
`$ pip3 install opencv-python`
