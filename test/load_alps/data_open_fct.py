from model.coordinate import Coordinate
from functions.utils_fct import *

def open_ilin(file_name):
    file = open(file_name, "r", encoding="UTF-8")

    lat_NW_corner, lon_NW_corner, lat_SE_corner, lon_SE_corner = file.readline().split()
    step, nb_points = file.readline().split()

    ilins = []

    for line in file:

        if line.strip() != "":
            ilin = int(line.strip())
            ilins.append(ilin)

    return int(step), int(nb_points), ilins


def get_coord(file_name, ilin):
    file = open(file_name, "r", encoding="UTF-8")

    for i, line in enumerate(file, 1):
        if i == ilin:
            ilin, lat, lon = line.split()
            file.close()
            return float(lat), float(lon)

    file.close()


def init_coords(file_name, ilins):
    file = open(file_name, "r", encoding="UTF-8")

    for i, line in enumerate(file, 1):
        if i in ilins:
            ilin, lat, lon = line.split()

            Coordinate(int(ilin), float(lat), float(lon))

    file.close()

def get_points_coordinate(path, coordinate):
    file = open(path + "Data_files/Average_" + str(coordinate.getIndex()) + "_test15.out")

    lat = []
    lon = []
    depths = []
    Lp1 = []
    Lp2 = []
    Lp3 = []
    Lp4 = []
    Lp5 = []
    Lp6 = []

    line = file.readline()

    while len(line) != 0:
        depth, average_vsv, average_aniso, proba_of_anisotropy = line.split()

        line = file.readline()
        Vsv = float(average_vsv)
        Vsh = float(average_aniso) ** 0.5 * Vsv
        Vpv = 1.8 * Vsv
        Vph = Vpv
        rho = 2.35 + 0.036 * (Vpv - 3.0) ** 2

        p1, p2, p3, p4, p5, p6 = get_backus_parameters(rho, Vpv, Vph, Vsv, Vsh)

        lat.append(coordinate.getLatitude())
        lon.append(coordinate.getLongitude())
        depths.append(float(depth))
        Lp1.append(p1)
        Lp2.append(p2)
        Lp3.append(p3)
        Lp4.append(p4)
        Lp5.append(p5)
        Lp6.append(p6)

    file.close()

    return lat, lon, depths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6