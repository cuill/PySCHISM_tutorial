# PySCHISM_tutorial

## Install mamba
    https://mamba.readthedocs.io/en/latest/installation.html

## Create a Python environment
    mamba create -n pyschism_tutorial python=3.9

## Install pyschism package
### From PyPI using pip
    conda activate pyschism_tutorial
    pip install pyschism

### From source
    git clone https://github.com/schism-dev/pyschism.git
    cd pyschism
    pip install .

### Optional (replace cfgrib pip version with conda version)
    pip uninstall cfgrib
    conda install -c conda-forge cfgrib

## Generate input files
    git clone https://github.com/cuill/PySCHISM_tutorial.git
    cd PySCHISM_tutorial
### Download grid files
    mkdir data
    wget -O data/hgrid.gr3 http://ccrm.vims.edu/yinglong/Cui/PySCHISM_tutorial/hgrid.gr3
    wget -O data/vgrid.in http://ccrm.vims.edu/yinglong/Cui/PySCHISM_tutorial/vgrid.in
