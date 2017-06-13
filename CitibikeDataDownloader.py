# Julian Smoller ~ 2017

import os # to check make directory
import urllib.request # to download map

class CitibikeDataDownloader:
    '''Download Citibike data from Citibike API'''
    def __init__(self):
        self.url = 'https://www.citibikenyc.com/stations/json'
        # Default path for data
        self.path_directory = 'data/CitibikeDataDownloader'
        self.path_downloads = self.path_directory + '/downloads'
        self.path_default = self.path_downloads + '/default.json'
        if not os.path.exists(self.path_directory):
            os.mkdir(self.path_directory)
        if not os.path.exists(self.path_downloads):
            os.mkdir(self.path_downloads)
    def download(self,path=None):
        response = urllib.request.urlopen(self.url)
        data = response.read()
        # Write to file
        path = self.path_default if path is None else path
        file = open(path,'wb')
        file.write(data)
        return data
    