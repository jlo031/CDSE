# CDSE

Library for search and download of data from Copernicus Data Space Ecpsystem (CDSE).


### Preparation
Create anaconda environment:

    # create and activate new environment
    conda create -y --name CDSE python=3.12
    conda activate CDSE

    pip install ipython
    conda install -y loguru requests


### Installation
You can install this library directly from github (1) or locally after cloning (2).  
For both installation options, first set up the environment as described above.

1. **Installation from github**

       # install this package
       pip install git+https://github.com/jlo031/CDSE

2. **Local installation**

       # clone the repository
       git clone git@github.com:jlo031/CDSE

   Change into the main directory of the cloned repository (it should contain the *setup.py* file) and install the library:

       # installation
       pip install .
