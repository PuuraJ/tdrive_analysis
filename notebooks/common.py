import pandas as pd
import numpy as np

import folium
from folium import plugins
from folium.plugins import HeatMap
import datetime


import geopandas
from shapely.geometry import Polygon
from geopandas import GeoSeries


def haversine_np(lon1, lat1, lon2, lat2):
    """
    Source: https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas

    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length.    

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km



# Define mapping function. Map coordinate into grid slot

class RectangularTessellation:
    """
    Class for creating a tessellation. 
    Contains functions for mapping points into a tessellation.
    """
    
    def __init__(self, min_lon, min_lat, max_lon, max_lat, size: int):
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat
        self.size = size
        assert min_lon < max_lon
        assert min_lat < max_lat
        
        ## Create linspaces and meshgrid, probably will not need
        self.x_linspace = np.linspace(min_lon, max_lon, num=self.size+1)
        self.y_linspace = np.linspace(min_lat, max_lat, num=self.size+1)
    
        # Figure out stepsizes for boxes. This we need to map to bo
        self.x_stepsize = self.x_linspace[1] - self.x_linspace[0]
        self.y_stepsize = self.y_linspace[1] - self.y_linspace[0]
        
    
    def get_polygons(self):
        """
        Creates geopandas Poly objects. Returns a series of it.
        The order of creation is from smallest long to max long (left-to-right)
                                and inner loop is smallest lat to max lat (down-to-up)
        
        
        
        Therefore the order of grid is
        
        3 6 9
        2 5 8
        1 4 7
        """
        polygons = []
        for i in range(len(self.x_linspace)-1):
            for j in range(len(self.y_linspace)-1):
                #print(len(polygons), i, j, i*self.size+j)
                poly = Polygon([(self.x_linspace[i], self.y_linspace[j]),
                                (self.x_linspace[i+1], self.y_linspace[j]),
                                (self.x_linspace[i+1], self.y_linspace[j+1]),
                                (self.x_linspace[i], self.y_linspace[j+1])
                               ])
                polygons.append(poly)
                
        g = GeoSeries(polygons)
        
        return g
    
    def map_to_grid(self, lon, lat):
        """
        Maps latitude and longitude to created meshgrid.
        f(lon, lat) -> grid_i, grid_j
        """
        #print("lon_diff", lon - self.min_lon)
        #print("lat_diff", lat - self.min_lat)

        
        x_grid = np.int64((lon - self.min_lon) / self.x_stepsize)
        y_grid = np.int64((lat - self.min_lat) / self.y_stepsize)
        
        ## HACK!! Fix edge case.. Some points are in size+1'th box
        x_grid = np.clip(x_grid, a_min=0, a_max=self.size-1)
        y_grid = np.clip(y_grid, a_min=0, a_max=self.size-1)
            
        return x_grid, y_grid
    
    def calculate_occurrences_by_grid_slot(self, df):
        """
        df: input data with mapped already columns grid_x and grid_y
        """
        assert "grid_x" in df.columns and "grid_y" in df.columns
        
        occurrences_by_grid = df.groupby(["grid_x", 
                                          "grid_y"]).count().reset_index()[["grid_x", "grid_y", "taxi_id"]]
        
        occurrences_by_grid = occurrences_by_grid.rename(columns={"taxi_id": "count"})


        # Add missing counts. If not all boxes are filled.
        index_ = pd.MultiIndex.from_product([[i for i in range(self.size)], 
                                             [i for i in range(self.size)]], 
                                            names=["grid_x", "grid_y"])
        
        occurrences_by_grid = occurrences_by_grid.set_index(
            ["grid_x", "grid_y"]).join(pd.DataFrame(index=index_), how="right").fillna(0)
        
        occurrences_by_grid["count"] = occurrences_by_grid.astype(int)
        occurrences_by_grid = occurrences_by_grid.reset_index()

        # Get grid nr! it is grid_y (row) * grid_size + grid_x
        occurrences_by_grid["grid_nr"] = (
            occurrences_by_grid["grid_y"]*self.size + occurrences_by_grid["grid_x"]).astype("str")


        return occurrences_by_grid


