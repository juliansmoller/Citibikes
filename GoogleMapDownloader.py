# Julian Smoller ~ 6/12/2017

import os # to check make directory
import urllib.request # to download map


class GoogleMapDownloader:
    '''This component is responsible for downloading a static map 
    (as an image) using the Google maps API.'''
    def __init__(self):
        # Default lat and long (for testing)
        self.lat_default = 40.744419
        self.lon_default = -74.001684
        # Basic info about images returned by Google maps API
        # At zoom=16, the Google maps API returns an image that's 640x640 pixels
        self.x_pixels_per_image = 640
        self.y_pixels_per_image = 640
        # Near NYC, the images returned by the Google maps API contain approx.
        # 46600 pixels per degree longitude and 61500 pixels per degree latitude
        self.x_pixels_per_lon = 46600.0
        self.y_pixels_per_lat = 61500.0
        # Calculate the approx. size of each image in degrees of lon/lat
        self.lon_per_image = self.x_pixels_per_image / self.x_pixels_per_lon
        self.lat_per_image = self.y_pixels_per_image / self.y_pixels_per_lat
        # Default paths and directories for downloads
        self.path_directory = 'data/GoogleMapDownloader'
        self.path_downloads = self.path_directory + '/downloads'
        self.path_default = self.path_downloads + '/default.jpg'
        if not os.path.exists(self.path_directory):
            os.mkdir(self.path_directory)
        if not os.path.exists(self.path_downloads):
            os.mkdir(self.path_downloads)
    def get_url(self,lat=None,lon=None,zoom=16,size=(1000,1000)):
        '''Generate a url that can be used to get a static map 
        centered at given longitude and latitude from Google maps API'''
        url = 'https://maps.googleapis.com/maps/api/staticmap?'
        lat = self.lat_default if lat is None else lat
        lon = self.lon_default if lon is None else lon
        url += 'center='+str(lat)+','+str(lon)
        url += '&zoom='+str(zoom)
        url += '&size='+str(size[0])+'x'+str(size[1])
        url += '&maptype=roadmap'
        return url
    def download(self,lat=None,lon=None,zoom=16,size=(1000,1000),path=None):
        '''Download a static map (image) centered at given 
        latitude and longitude from Google maps API'''
        url = self.get_url(lat=lat,lon=lon,zoom=zoom,size=size)
        path = self.path_default if path is None else path
        urllib.request.urlretrieve(url,path)
        return path