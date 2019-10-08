from scipy import ndimage
import numpy as np
from model.model import Model

def filtre(model, delta_z = None, lambda_=15):  # <model>

    latitudes = model.getLatitudes()
    longitudes = model.getLongitudes()
    depths = model.getDepths()

    if delta_z is None:
        delta_z = len(np.unique(depths)) / (max(depths) - min(depths) +1)

    # define new grid
    grid_latitudes, grid_longitudes, grid_depths = np.mgrid[
                                                   min(latitudes):max(latitudes):len(np.unique(latitudes)) * 1j,
                                                   min(longitudes):max(longitudes):len(np.unique(longitudes)) * 1j,
                                                   min(depths):max(depths):delta_z * (
                                                               max(depths) - min(depths) +1) * 1j]

    grid = np.array((grid_latitudes.flatten(), grid_longitudes.flatten(), grid_depths.flatten())).T

    # get parameters
    parameters_grid = model.getParameters(grid).T
    bool_nan = [np.isnan(parameter_grid) for parameter_grid in parameters_grid]
    out_of_range = np.logical_or(bool_nan[0], bool_nan[1])

    for i in range(2, len(bool_nan)):
        out_of_range = np.logical_or(out_of_range, bool_nan[i])

    latitudes = grid_latitudes.flatten()[~out_of_range]
    longitudes = grid_longitudes.flatten()[~out_of_range]
    depths = grid_depths.flatten()[~out_of_range]

    parameters_in_range = np.array([parameter_grid[~out_of_range] for parameter_grid in parameters_grid])

    Lp1, Lp2, Lp3, Lp4, Lp5, Lp6 = [], [], [], [], [], []
    Lindex = []

    # find all lat/long couples
    lats_longs = np.array((latitudes, longitudes)).T
    lats_longs_reduce = np.unique(lats_longs, axis=0)

    # find depths associated with lat/long couples
    for lat_long_result in lats_longs_reduce:

        lat, long = lat_long_result

        depths_ = depths[np.where(latitudes == lat * (longitudes == long))]

        # save len of depths_
        Lindex.append(len(depths_))

    # filter by chunk
    for i in range(len(Lindex)):

        parameters_filtre = ndimage.gaussian_filter1d(parameters_in_range[:, sum(Lindex[:i]):sum(Lindex[:i]) + Lindex[i]], lambda_ * delta_z / (2 * 1.4),
                                                      mode="mirror")  # 1.4 Empirique cf. Capdeville

        p1, p2, p3, p4, p5, p6 = parameters_filtre
        Lp1.extend(p1)
        Lp2.extend(p2)
        Lp3.extend(p3)
        Lp4.extend(p4)
        Lp5.extend(p5)
        Lp6.extend(p6)

    return Model(latitudes, longitudes, depths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6)

def residual_homogenization(model1, model2, delta_z = None, lambda_=15):  # model2 + <model1 - model2>

    latitudes = model1.getLatitudes()
    longitudes = model1.getLongitudes()
    depths = model1.getDepths()

    if delta_z is None:
        delta_z = len(np.unique(depths)) / (max(depths) - min(depths) +1)

    # define new grid
    grid_latitudes, grid_longitudes, grid_depths = np.mgrid[
                                                   min(latitudes):max(latitudes):len(np.unique(latitudes)) * 1j,
                                                   min(longitudes):max(longitudes):len(np.unique(longitudes)) * 1j,
                                                   min(depths):max(depths):delta_z * (
                                                               max(depths) - min(depths) +1) * 1j]

    grid = np.array((grid_latitudes.flatten(), grid_longitudes.flatten(), grid_depths.flatten())).T

    # get parameters
    parameters_grid_1 = model1.getParameters(grid).T
    parameters_grid_2 = model2.getParameters(grid).T

    bool_nan_1 = [np.isnan(parameter_grid) for parameter_grid in parameters_grid_1]
    bool_nan_2 = [np.isnan(parameter_grid) for parameter_grid in parameters_grid_2]

    out_of_range = np.logical_or(bool_nan_1[0], bool_nan_1[1])

    for i in range(2, len(bool_nan_1)):
        out_of_range = np.logical_or(out_of_range, bool_nan_1[i])

    for i in range(len(bool_nan_2)):
        out_of_range = np.logical_or(out_of_range, bool_nan_2[i])

    longitudes = grid_longitudes.flatten()[~out_of_range]
    latitudes = grid_latitudes.flatten()[~out_of_range]
    depths = grid_depths.flatten()[~out_of_range]

    parameters_in_range_1 = np.array([parameter_grid[~out_of_range] for parameter_grid in parameters_grid_1])
    parameters_in_range_2 = np.array([parameter_grid[~out_of_range] for parameter_grid in parameters_grid_2])

    parameters_in_range = parameters_in_range_1 - parameters_in_range_2

    Lp1, Lp2, Lp3, Lp4, Lp5, Lp6 = [], [], [], [], [], []
    Lindex = []

    # find all lat/long couples
    lats_longs = np.array((latitudes, longitudes)).T
    lats_longs_reduce = np.unique(lats_longs, axis=0)

    # find depths associated with lat/long couples
    for lat_long_result in lats_longs_reduce:

        lat, long = lat_long_result

        depths_ = depths[np.where(latitudes == lat * (longitudes == long))]

        # save len of depths_
        Lindex.append(len(depths_))

    # filter by chunk
    for i in range(len(Lindex)):

        parameters_filtre = ndimage.gaussian_filter1d(parameters_in_range[:, sum(Lindex[:i]):sum(Lindex[:i]) + Lindex[i]], lambda_ * delta_z / (2 * 1.4),
                                                      mode="mirror")  # 1.4 Empirique cf. Capdeville

        p1, p2, p3, p4, p5, p6 = parameters_filtre
        Lp1.extend(p1)
        Lp2.extend(p2)
        Lp3.extend(p3)
        Lp4.extend(p4)
        Lp5.extend(p5)
        Lp6.extend(p6)

    Lp1 = np.array(Lp1) + parameters_in_range_2[0]
    Lp2 = np.array(Lp2) + parameters_in_range_2[1]
    Lp3 = np.array(Lp3) + parameters_in_range_2[2]
    Lp4 = np.array(Lp4) + parameters_in_range_2[3]
    Lp5 = np.array(Lp5) + parameters_in_range_2[4]
    Lp6 = np.array(Lp6) + parameters_in_range_2[5]

    return Model(latitudes, longitudes, depths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6)

