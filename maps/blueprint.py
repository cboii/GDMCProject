import itertools
import numpy as np
from .featureMaps import MapFeatureExtractor
from agents.plots import PlotType
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

class Blueprint:
    def __init__(self, map_features: MapFeatureExtractor = None):
        
        
        self.map: np.ndarray = np.zeros((256,256))
        self.current_area: np.ndarray = np.zeros((256,256), dtype=bool)
        self.road_network: np.ndarray = np.zeros((256,256), dtype=bool)
        self.houses: np.ndarray = np.zeros((256,256), dtype=bool)
        self.borders: np.ndarray = np.zeros((256,256), dtype=bool)
        self.farms: np.ndarray = np.zeros((256,256), dtype=bool)
        self.well: np.ndarray = np.zeros((256,256), dtype=bool)
        self.map_features = map_features
        self.ground_water_map = self.map_features.create_groundwater_map()
        self.steepness_map = self.map_features.create_gradient_maps()[4]
        self.height_map = self.map_features.create_heightmap()

    def place(self, loc: np.ndarray, type: PlotType):
        for x, y in loc:
            
            x = int(x)
            y = int(y)
            match type:
                case PlotType.ROAD:
                    self.map[x, y] = 200
                    self.road_network[x,y] = True
                case PlotType.HOUSE:
                    self.map[x, y] = 255
                    self.houses[x,y] = True
                case PlotType.FARM:
                    self.map[x, y] = 150
                    self.farms[x,y] = True
                case PlotType.WELL:
                    self.map[x, y] = 100
                    self.well[x,y] = True
                case PlotType.BORDER:
                    self.map[x,y]=50

    def show(self):
        plt.imshow(self.map)
        plt.show()


    @staticmethod
    def get_buildable_area(steepness_map: np.ndarray, ground_water_map: np.ndarray, step_size = 4, gaussian = False, radius = 1):

        buildable_regions = np.empty((int(steepness_map.shape[0]/step_size), int(steepness_map.shape[1]/step_size)), dtype=float) 
        for x in range(0, steepness_map.shape[0], step_size):
            for z in range(0, steepness_map.shape[1], step_size):

                buildable_regions[round(x/(steepness_map.shape[0] - step_size) * (steepness_map.shape[0]/step_size - 1)), round(z/(steepness_map.shape[1] - step_size) * (steepness_map.shape[1]/step_size - 1))] = np.mean(steepness_map[x: x + step_size,z: z + step_size])

        # Exclude water
        max = np.max(buildable_regions)
        for x in range(0, steepness_map.shape[0], step_size):
            for z in range(0, steepness_map.shape[1], step_size):
                
                if np.any(ground_water_map[x: x + step_size,z: z + step_size] != 255): 
                    buildable_regions[round(x/(steepness_map.shape[0] - step_size) * (steepness_map.shape[0]/step_size - 1)), round(z/(steepness_map.shape[1] - step_size) * (steepness_map.shape[1]/step_size - 1))] = max

        if gaussian:
            buildable_regions = gaussian_filter(buildable_regions, sigma=1, radius=radius)
        
        return buildable_regions
    
    def get_town_center(self, step_size=32, gaussian=False, radius=1):
        b_area = self.get_buildable_area(self.steepness_map, self.ground_water_map, step_size=step_size, gaussian=gaussian, radius=radius)
        rel_pos = np.array(np.unravel_index(np.argmin(b_area), b_area.shape))
        rel_pos = (rel_pos[0]*step_size, rel_pos[1]*step_size)
        
        return b_area, rel_pos
    
    def get_subregion(self, pos, region_size = 32, gaussian=False):
        height_map = self.height_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        ground_water_map = self.ground_water_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        steepness_map = self.steepness_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        subregion = self.get_buildable_area(steepness_map, ground_water_map, step_size=1, gaussian=gaussian)
        
        return height_map, ground_water_map, steepness_map, subregion
    
    def get_center_district_map(self, step_size=32):
        pass
        