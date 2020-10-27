# On the Jetson Nano, place the files in the following path:  
**Note:** a `models` folder is also required. It can be downloaded [here](https://1drv.ms/u/s!AlG0FKaSj9fegbMK0vMFMjWB9uLZfw?e=9X4zr6). It should also be placed in this path.  
`/home/dlinano/nvdli-nano/`

# Dependencies:
- Python 3 - Tested working with 3.6 and 3.7. It will NOT work with 3.8.
- Tensorflow
- pynetworktables
- OpenCV (pre-installed)
- matplotlib
- Pillow (PIL)

**A partially automated version of dependencies installation is available as a shell script:**  
[auto installer](https://1drv.ms/u/s!AlG0FKaSj9fegbJvXlqB30WBOcnAtA?e=9u6APm)  
This will install all dependencies mentioned. Pillow should be installed manually and OpenCV should be checked manually.  

# How to install dependencies on the Jetson Nano:
**1. Tensorflow**  
Below is a summary of [Nvidia's guide](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html), which was used to install Tensorflow

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

**2. NetworkTables**  
Install [pynetworktables](https://github.com/robotpy/robotpy-docs/blob/55e7ab2427824d4c8af3740c3a178e373e4f6ede/install/pynetworktables.rst) using pip:  
`$ pip3 install pynetworktables`

**3. OpenCV**  
Check and make sure you're on openCV 4.1.1 or higher:  
`$ python3`  
`>>> import cv2`  
`>>> cv2.__version__`  
expected default outputs: `'4.1.1'` or `'3.2.0'`  

if you have 3.2.0, try this:  
`$ sudo apt-get autoremove python3-opencv`  
if the above commands doesn't work, try uninstalling all versions of opencv (pip, apt, etc.) and run [this file](https://github.com/milq/milq/blob/master/scripts/bash/install-opencv.sh)

**4. matplotlib**  
`$ sudo apt-get install --upgrade python3-matplotlib`  

**5. Pillow (PIL)**  
Make sure all versions of Pillow are uninstalled  
`$ sudo apt-get autoremove python3-pil`  
`$ pip3 uninstall Pillow`  

then install the latest version using one of the two commands (either should work the same way):  
`$ sudo apt-get install python3-pil` **or** *(not both)*  
`$ pip3 install Pillow`  
