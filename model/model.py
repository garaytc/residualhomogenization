from numpy import array, unique,  where, concatenate
from scipy.interpolate import griddata

def interpol(points, parameters, grid):

    # find nearest lat/lon couple

    lats_longs_pts = array((points.T[0], points.T[1])).T
    lats_longs_reduce_pts = unique(lats_longs_pts, axis=0)

    lats_longs_grid = array((grid.T[0], grid.T[1])).T
    lats_longs_reduce_grid = unique(lats_longs_grid, axis=0)

    lats_longs_result = griddata(lats_longs_reduce_pts, lats_longs_reduce_pts, lats_longs_reduce_grid, method="nearest")

    # get depths associated with nearest lat/long couples

    values = []

    for lat_long_result, lat_long_grid in zip(lats_longs_result, lats_longs_reduce_grid):

        lat, long = lat_long_result

        # construct grid
        points_ = points[where(points[:,0] == lat * (points[:, 1] == long))].T[2].T
        parameters_ = parameters[where(points[:,0] == lat * (points[:, 1] == long))]

        lat, long = lat_long_grid

        grid_ = grid[where(grid[:,0] == lat * (grid[:, 1] == long))].T[2].T

        # interpolation
        values.extend(griddata(points_, parameters_, grid_))

    return array(values)

class Model:

    def __init__(self, latitudes, longitudes, depths, p1, p2, p3, p4, p5, p6):
        # See [Capdeville et al. 2013]
        # p1 = rho
        # p2 = 1 / C
        # p3 = 1 / L
        # p4 = (A - F ** 2 / C)
        # p5 = F / C
        # p6 = N

        self.latitudes = array(latitudes)
        self.longitudes = array(longitudes)
        self.depths = array(depths)
        self.p1 = array(p1)
        self.p2 = array(p2)
        self.p3 = array(p3)
        self.p4 = array(p4)
        self.p5 = array(p5)
        self.p6 = array(p6)

    def getLatitudes(self):
        return self.latitudes

    def getLongitudes(self):
        return self.longitudes

    def getDepths(self):
        return self.depths

    def getP1(self):
        return self.p1

    def getP2(self):
        return self.p2

    def getP3(self):
        return self.p3

    def getP4(self):
        return self.p4

    def getP5(self):
        return self.p5

    def getP6(self):
        return self.p6

    def getParameters(self, xi):
        # get p1, p2, p3, p4, p5, p6 from xi grid [[latitudes, ...], [longitudes, ...], [depths, ...]]

        points = array([self.latitudes, self.longitudes, self.depths]).T
        parameters = array([self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]).T

        return interpol(points, parameters, xi)

    def getC(self):
        return 1 / self.p2

    def getL(self):
        return 1 / self.p3

    def getF(self):
        return self.p5 * self.getC()

    def getA(self):
        return self.p4 + self.p5 * self.getF()

    def getN(self):
        # Same getP6
        return self.p6

    def getEta(self):
        return self.getF() / (self.getA() - 2 * self.getL())

    def getXi(self):
        return self.getN() / self.getL()

    def getPhi(self):
        return self.getC() / self.getA()

    def getRho(self):
        # Same getP1
        return self.p1

    def getVpv(self):
        return (self.getC() / self.getRho()) ** 0.5

    def getVph(self):
        return (self.getA() / self.getRho()) ** 0.5

    def getVsv(self):
        return (self.getL() / self.getRho()) ** 0.5

    def getVsh(self):
        return (self.getN() / self.getRho()) ** 0.5

    def getVpVs(self):
        return self.getVpv() / self.getVsv()

    def add(self, latitudes, longitudes, depths, p1, p2, p3, p4, p5, p6):
        self.latitudes = concatenate((self.latitudes, latitudes))
        self.longitudes = concatenate((self.longitudes, longitudes))
        self.depths = concatenate((self.depths, depths))
        self.p1 = concatenate((self.p1, p1))
        self.p2 = concatenate((self.p2, p2))
        self.p3 = concatenate((self.p3, p3))
        self.p4 = concatenate((self.p4, p4))
        self.p5 = concatenate((self.p5, p5))
        self.p6 = concatenate((self.p6, p6))

    def add_unique(self, latitude, longitude, depth, p1, p2, p3, p4, p5, p6):

        # find nearest latitude/longitude couple
        lats_longs = array((self.latitudes, self.longitudes)).T
        lats_longs_reduce = unique(lats_longs, axis=0)

        lats_longs_result = griddata(lats_longs_reduce, lats_longs_reduce, (latitude, longitude),
                                     method="nearest")

        self.add([lats_longs_result[0]], [lats_longs_result[1]], [depth], [p1], [p2], [p3], [p4], [p5], [p6])