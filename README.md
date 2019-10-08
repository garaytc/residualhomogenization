# Residual Homogenization

Implementation of seismic residual homogenization in 1D see **Capdeville Y., Stuzmann E., Wang N. & Montagner J.-P., 2013. «Residual homogenization for seismic
forward and inverse problems in layered media.»** ***Geophysical Journal International***

## Dependencies
> matplotlib, numpy, scipy 

## [model/model.py](model/model.py)
> It contains class of model, to manipulate it more easily.  
> Based on Backus parameters **Backus, G., 1962. «Long-wave elastic anisotropy produced by horizontal layering.»** ***Journal of Geophysical
Research Volume 67, No. 11***
## [model/coordinate.py](model/coordinate.py)
> It contains class of coordinate, to manipulate it more easily
## [functions/homo_fct.py](functions/homo_fct.py)
> It contains main functions of residual homogenisation:  
> **filtre** and **residual_homogenization**
## [functions/utils_fct.py](functions/utils_fct.py)
> It contains some utils functions:  
> **get_distance_km**, **get_backus_parameters** and **simplify**
## [functions/graphics.py](functions/graphics.py)
> It contains functions to print model:  
> **print_1D** and **print_models_2D**
## [test/](test/)
> It contains one folder to load data from Alps Model and one example file to manipulate residual homogenisation
