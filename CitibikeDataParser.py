# Julian Smoller ~ 2017

import json
import pandas as pd
import os
import pickle

class CitibikeDataParser:
    '''Parse Citibike data downloaded from Citibike API'''
    def __init__(self):
        self.path_directory = 'data/CitibikeDataParser'
        self.path_default = self.path_directory + '/default.p'
        if not os.path.exists(self.path_directory):
            os.mkdir(self.path_directory)  
    def parse(self,data):
        data = data.decode('utf-8')
        data = json.loads(data)
        self.data = data
        self.execution_time = self.parse_execution_time(data)
        self.stations = self.parse_stations(data)
        self.geo_region = self.parse_geo_region(self.stations)
    def parse_stations(self,data):
        return pd.DataFrame(data['stationBeanList'])
    def parse_execution_time(self,data):
        return data['executionTime']
    def parse_geo_region(self,data):
        '''Find the min/max for latitude and longitude'''
        geo_region = {}
        geo_region['lat0'] = data['latitude'].min()
        geo_region['lat1'] = data['latitude'].max()
        geo_region['lon0'] = data['longitude'].min()
        geo_region['lon1'] = data['longitude'].max()
        return geo_region
    def save(self,path=None):
        path = self.path_default if path is None else path
        pickle.dump(self,open(path,'wb'))