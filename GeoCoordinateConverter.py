import math # to round numbers

class GeoCoordinateConverter:
    '''Convert latitude and longitude within a geogrpahic region 
    to xy coordinates corresponding to the pixels in an image.
    Note: units per degree (x_per_lon and y_per_lat) are determined 
    exogenously and passed as parameters. So, the ultimate size of the 
    Cartesian plane  (e.g. pixel image) is determined by the size of the 
    geographic region to be mapped, instead of vice versa, e.g. by passing 
    xy_region as a paramter. For example, I calclated the default
    values manually/independently by experimenting with the 
    Google maps API while downloading images of New York city at zoom level 16. 
    I imagine that the x_per_lon would be different at other latitudes, e.g. 
    near the north and south pole, where the lines of longitude converge. '''
    def __init__(self, geo_region, x_per_lon=46600.0, y_per_lat=61500.0):
        self.lon0 = geo_region['lon0']
        self.lon1 = geo_region['lon1']
        self.lat0 = geo_region['lat0']
        self.lat1 = geo_region['lat1']
        self.lon_span = self.lon1 - self.lon0
        self.lat_span = self.lat1 - self.lat0
        self.x_per_lon = x_per_lon
        self.y_per_lat = y_per_lat
        self.x = int(math.ceil(self.lon_span * self.x_per_lon))
        self.y = int(math.ceil(self.lat_span * self.y_per_lat))
    def lon_to_x(self, lon):
        '''Convert given longitude to the x pixel dimension in an image.'''
        return int((lon-self.lon0)*self.x_per_lon)
    def lat_to_y(self, lat):
        '''Convert given latitude to the y pixel dimension in an image.
        Note: y dimension is inverted because (0,0) is the top left 
        corner of an image.'''
        return int(self.y - int((lat-self.lat0)*self.y_per_lat))