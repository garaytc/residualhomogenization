from functions.graphics import *
from functions.utils_fct import *
from functions.homo_fct import *
from math import pi

# lambda to homogenize
lambda_ = 30

# nb of longitudes
nb_lon = 400

delta_z = 0.5
depths_ = np.arange(0, 200 + delta_z, delta_z)
depths = np.tile(depths_, nb_lon)

latitudes = [45.] * len(depths_) * nb_lon
longitudes_ =  np.linspace(0, 3, nb_lon)
Lp1, Lp2, Lp3, Lp4, Lp5, Lp6 = [], [], [], [], [], []
longitudes = []

# construct one "truth model"
ZMoho = 40
ZDiscontinuity2 = 70
ZDiscontinuity3 = 150

for longitude in longitudes_:
    for z in depths_:
        Vs = 3
        Vp = 6
        rho = 2.7

        if z >= ZMoho + cos(longitude / 3 * 2 * pi * 5) * 10:
            Vs = 4.4
            Vp = 8
            rho = 3.4

        Vsv = Vsh = Vs
        Vpv = Vph = Vp

        if z >= ZDiscontinuity2:
            Vsv = 4.4
            Vsh = 4.6
            Vpv = 7.94
            Vph = 7.78
            rho = 3.4

        if z >= ZDiscontinuity3 + cos(longitude / 3 * 2 * pi * 1.5) * 5:
            Vsv = Vsh = 4.5
            Vpv = Vph = 8.2
            rho = 3.4

        p1, p2, p3, p4, p5, p6 = get_backus_parameters(rho, Vpv, Vph, Vsv, Vsh)

        Lp1.append(p1)
        Lp2.append(p2)
        Lp3.append(p3)
        Lp4.append(p4)
        Lp5.append(p5)
        Lp6.append(p6)
        longitudes.append(longitude)

truthModel = Model(latitudes, longitudes, depths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6)

# construct one "reference model"

Lp1, Lp2, Lp3, Lp4, Lp5, Lp6 = [], [], [], [], [], []
longitudes = []

ZMoho = 40

for longitude in longitudes_:
    for z in depths_:
        Vs = 3
        Vp = 6
        rho = 2.7

        if z >= ZMoho + cos(pi + longitude / 3 * 2 * pi * 5) * 10:
            Vs = 4.4
            Vp = 8
            rho = 3.4

        p1, p2, p3, p4, p5, p6 = get_backus_parameters(rho, Vp, Vp, Vs, Vs)

        Lp1.append(p1)
        Lp2.append(p2)
        Lp3.append(p3)
        Lp4.append(p4)
        Lp5.append(p5)
        Lp6.append(p6)
        longitudes.append(longitude)

referenceModel = Model(latitudes, longitudes, depths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6)

# homogenization

modelHomogen = residual_homogenization(truthModel, referenceModel, lambda_=lambda_)

# show profile

models = [truthModel, referenceModel, modelHomogen]
models_name = ["Mtruth", "Mref", "Mhomo"]

# 1d profile
latitude = 45
longitude = 1
fonctions = [Model.getVsv, Model.getXi]
fonctions_label = ["Vsv", "Anisotropie"]

style.use("seaborn-ticks")

print_1D(models, latitude, longitude, models_name, fonctions, fonctions_label, 1)

# 2d profile
latitude_1 = 45
longitude_1 = 0
latitude_2 = 45
longitude_2 = 3

vmins = [2.5, 0.5]
vmaxs = [7., 1.5]

fonctions = [Model.getVsv, Model.getXi]
fonctions_label = ["Vsv", "Xi"]

print_models_2D(models, latitude_1, longitude_1, latitude_2, longitude_2, models_name, fonctions, fonctions_label, 2,
                nb_x=nb_lon, vmins=vmins, vmaxs=vmaxs, suptitle="Models 2d profile", aspect="equal")

show()
