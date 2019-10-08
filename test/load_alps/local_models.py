import time
from multiprocessing import Pool
from test.load_alps.data_open_fct import *
from model.coordinate import Coordinate
from model.model import Model

path = "RSC\\"


def init():
    # construct Coordinate dict

    if Coordinate.isInit():
        return

    step, nb_pointsn, ilins = open_ilin(path + "Data_files/ilin_All.in")

    ilins = ilins[:]

    init_coords(path + "Data_files/ilin_coord.txt", ilins)


def getPoints(tuple_args):
    path, coordinate = tuple_args

    return get_points_coordinate(path, coordinate)


def getAlpsModel():
    print("Construct AlpsModel")

    # Tomographie Alpes
    t0 = time.time()
    last_percent = 0

    init()
    pool = Pool()

    Llat, Llon, Ldepths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6 = [], [], [], [], [], [], [], [], []

    args = []

    for latitude in Coordinate.getLatitudes():
        for longitude in Coordinate.getLatitudes()[latitude]:
            args.append((path, Coordinate.fromLatLong(latitude, longitude)))

    for data in pool.imap(getPoints, args, chunksize=1):
        lat, lon, depths, p1, p2, p3, p4, p5, p6 = data

        Llat.extend(lat)
        Llon.extend(lon)
        Ldepths.extend(depths)
        Lp1.extend(p1)
        Lp2.extend(p2)
        Lp3.extend(p3)
        Lp4.extend(p4)
        Lp5.extend(p5)
        Lp6.extend(p6)

        if len(Llat) / (150 * len(Coordinate.indexs)) >= last_percent:  # 150 = len(depths)
            print(int(100 * 100 * len(Llat) / (150 * len(Coordinate.indexs))) / 100, "%",
                  int((time.time() - t0) * 100) / 100, "seconds")
            last_percent += 0.05

    pool.close()
    pool.join()

    model_alpes = Model(Llat, Llon, Ldepths, Lp1, Lp2, Lp3, Lp4, Lp5, Lp6)
    print("AlpsModel end after", time.time() - t0, "seconds")
    return model_alpes
