# Julian Smoller ~ 2017

import os
import pandas as pd
from PIL import Image
import time
import math

# Custom classes 
import GoogleMapDownloader
import GeoCoordinateConverter

class MapMaker:
    '''Given a geographic region and basic info about the 
    Google maps API, download a series of small maps and comile
    them into one large map that spans the geographic reigon.'''
    def __init__(self,geo_region):
        # The GoogleMapDownloader handles small map / image info
        self.gmd = GoogleMapDownloader.GoogleMapDownloader()
        # The GeoCoordinateConverter handles big map / image info
        self.gcc = GeoCoordinateConverter.GeoCoordinateConverter(
            geo_region,
            x_per_lon = self.gmd.x_pixels_per_lon, 
            y_per_lat = self.gmd.y_pixels_per_lat)
        # Maximum size for big map
        self.max_pixels = 100000000
        # Default path for saving big map
        self.path_directory = 'data/MapMaker'
        if not os.path.exists(self.path_directory):
            os.mkdir(self.path_directory) 
        self.path_big_map = self.path_directory + '/big_map.jpg'
    def dice(self,segment=[0,1],n=4):
        '''Divide a given segment, e.g. [0,1], into n evenly spaced points,
        excluding the minimum and maximum points in that sgement'''
        increment = float(segment[1]-segment[0]) / n
        points = [segment[0] + increment/2 + increment*i for i in range(n)]
        return points
    def position_maps(self):
        '''Calculate the lon/lat coordinates for the small maps'''
        self.n_images_x = int(math.ceil(abs(self.gcc.lon_span)/self.gmd.lon_per_image))
        self.n_images_y = int(math.ceil(abs(self.gcc.lon_span)/self.gmd.lat_per_image))
        self.lons = self.dice(segment=[self.gcc.lon0,self.gcc.lon1],n=self.n_images_x)
        self.lats = self.dice(segment=[self.gcc.lat0,self.gcc.lat1],n=self.n_images_y)
        self.maps = [(lon,lat) for lon in self.lons for lat in self.lats]
        self.maps = pd.DataFrame(self.maps,columns=['lon','lat'])
        # Calculate center
        self.maps['x_center'] = self.maps['lon'].map(lambda i: self.gcc.lon_to_x(i))
        self.maps['y_center'] = self.maps['lat'].map(lambda i: self.gcc.lat_to_y(i))
        # Calculate top left corner
        x_offset = int(self.gmd.x_pixels_per_image/2)
        y_offset = int(self.gmd.y_pixels_per_image/2)
        self.maps['x_top_left'] = self.maps['x_center'].map(lambda x: x-x_offset)
        self.maps['y_top_left'] = self.maps['y_center'].map(lambda y: y-y_offset)
        return self.maps
    def make_big_map(self,path=None,n=3,delay=1):
        '''Download each of the small maps using the Google maps API and 
        compile into one large map, then save to specified path'''
        # Emergency cutoff if big map is too big
        if self.gcc.x * self.gcc.y > self.max_pixels: 
            print('This map is too big!')
            print(self.gcc.x*self.gcc.y,'>',self.max_pixels)
            return
        # Create big map with black background
        big_map = Image.new('RGB', (self.gcc.x, self.gcc.y), (0,0,0))
        # Iterate through small maps: download and paste into big map
        for i in self.maps.index[:n]: # max number of small maps to download
            lat = self.maps.ix[i,'lat']
            lon = self.maps.ix[i,'lon']
            path_small_map = self.gmd.download(lat=lat,lon=lon)
            small_map = Image.open(path_small_map)
            xy = (self.maps.ix[i,'x_top_left'],self.maps.ix[i,'y_top_left'])
            big_map.paste(small_map, xy)
            time.sleep(delay)
        # Save big map
        path = self.path_big_map if path is None else path
        big_map.save(path)
        return path  