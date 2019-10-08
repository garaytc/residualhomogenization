class Coordinate:

    # dict to find coordinate from index, lat or long
    indexs = {}
    latitudes = {}
    longitudes = {}

    def __init__(self, index, latitude, longitude, register = True):

        self.index_ = index
        self.latitude_ = latitude
        self.longitude_ = longitude

        if not(register):
            return

        # save coordinate to dict index, lat or long

        Coordinate.indexs[index] = self

        if not(latitude in Coordinate.latitudes):
            Coordinate.latitudes[latitude] = {}

        Coordinate.latitudes[latitude][longitude] = self

        if not (longitude in Coordinate.longitudes):
            Coordinate.longitudes[longitude] = {}

        Coordinate.longitudes[longitude][latitude] = self

    def getIndex(self):
        return self.index_

    def getLatitude(self):
        return self.latitude_

    def getLongitude(self):
        return self.longitude_

    def getTuple(self):
        # Get tuple (latitude, longitude)
        return self.latitude_, self.longitude_

    def __str__(self):
        return str(self.latitude_) + "°, " + str(self.longitude_) + "° [" + str(self.index_) + "]"

    def __eq__(self, other):
        return other.getLatitude() == self.getLatitude() and other.getLongitude() == self.getLongitude()

    def __hash__(self):
        return hash((self.latitude_, self.longitude_))

    def distance_pwr2(self, other):
        return (self.getLatitude() - other.getLatitude()) ** 2 + (self.getLongitude() - other.getLongitude()) ** 2

    @staticmethod
    def fromIndex(index):
        # get coordinate from its index
        return Coordinate.indexs[index]

    @staticmethod
    def fromLatLong(latitude, longitude):
        # get coordinate from latitude and longitude
        return Coordinate.latitudes[latitude][longitude]

    @staticmethod
    def getLatitudes():
        # get dict latitudes
        return Coordinate.latitudes

    @staticmethod
    def getLongitudes():
        # get dict longitudes
        return Coordinate.longitudes

    @staticmethod
    def isInit():
        # check if coordinate dict are empty
        return len(Coordinate.indexs) > 1