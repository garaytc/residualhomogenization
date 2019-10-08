import numpy as np
from math import radians, sin, cos, atan2, sqrt
from model.model import Model


def get_distance_km(lat1, lng1, lat2=0, lng2=0):
    earth_radius = 6378137  # Earth radius = 6378 km
    rlo1 = radians(lng1)  # CONVERSION
    rla1 = radians(lat1)
    rlo2 = radians(lng2)
    rla2 = radians(lat2)
    dlo = (rlo2 - rlo1) / 2
    dla = (rla2 - rla1) / 2

    a = (sin(dla) * sin(dla)) + cos(rla1) * cos(rla2) * (sin(dlo) * sin(dlo))
    d = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * d / 1000


def get_backus_parameters(rho, Vpv, Vph, Vsv, Vsh, eta=1):
    # transform rho, vpv, vph, vsv, vsh, eta to p1, p2, p3, p4, p5, p6

    C = rho * Vpv ** 2
    A = rho * Vph ** 2
    L = rho * Vsv ** 2
    N = rho * Vsh ** 2

    F = eta * (A - 2 * L)

    p1 = rho
    p2 = 1 / C
    p3 = 1 / L
    p4 = (A - F ** 2 / C)
    p5 = F / C
    p6 = N

    return p1, p2, p3, p4, p5, p6


def simplify(model, min_lat, max_lat, delta_lat, min_lon, max_lon, delta_lon, min_z, max_z, delta_z):
    # change the grid of parameters of a model

    # construct new grid
    grid_latitudes, grid_longitudes, grid_depths = np.mgrid[min_lat:max_lat:(max_lat - min_lat + 1) / delta_lat * 1j,
                                                   min_lon:max_lon:(max_lon - min_lon + 1) / delta_lon * 1j,
                                                   min_z:max_z:(max_z - min_z + 1) / delta_z * 1j]

    grid = np.array((grid_latitudes.flatten(), grid_longitudes.flatten(), grid_depths.flatten())).T

    # get parameters interpolate on new grid
    parameters_grid = model.getParameters(grid).T

    # remove undefined values
    bool_nan = [np.isnan(parameter_grid) for parameter_grid in parameters_grid]
    out_of_range = np.logical_or(bool_nan[0], bool_nan[1])
    for i in range(2, len(bool_nan)):
        out_of_range = np.logical_or(out_of_range, bool_nan[i])

    latitudes = grid_latitudes.flatten()[~out_of_range]
    longitudes = grid_longitudes.flatten()[~out_of_range]
    depths = grid_depths.flatten()[~out_of_range]

    parameters_in_range = [parameter_grid[~out_of_range] for parameter_grid in parameters_grid]
    p1, p2, p3, p4, p5, p6 = parameters_in_range

    return Model(latitudes, longitudes, depths, p1, p2, p3, p4, p5, p6)
