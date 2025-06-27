import itertools
import math
from matplotlib.colors import Normalize
import numpy as np
from .featureMaps import MapFeatureExtractor
from agents.plots import PlotType
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from gdpc.vector_tools import Rect

class Blueprint:
    def __init__(self, map_features: MapFeatureExtractor = None):
        
        self.map_features = map_features
        self.ground_water_map = self.map_features.create_groundwater_map()
        self.lava_map = self.map_features.create_lava_map()
        self.steepness_map = self.map_features.create_gradient_maps()[4]
        self.height_map = self.map_features.create_heightmap()

        self.map: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]))
        self.plot_heights = np.zeros((self.height_map.shape[0],self.height_map.shape[1]))
        self.current_area: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.road_network: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.houses: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.borders: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.farms: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.church: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.decoration: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.well: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.misc: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.city_walls: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.town_hall: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.inn: np.ndarray = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.outside_walls_area = np.zeros((self.height_map.shape[0],self.height_map.shape[1]), dtype=bool)
        self.border_size = 4

        self.house_locs = {}

    def place(self, loc: np.ndarray, type: PlotType):
        for x, y in loc:
            
            x = int(x)
            y = int(y)
            match type:
                case PlotType.ROAD:
                    if self.map[x,y] <= 35:
                        self.map[x, y] = 200
                        self.road_network[x,y] = True
                case PlotType.HOUSE:
                    self.map[x, y] = 255
                    self.houses[x,y] = True
                case PlotType.TOWNHALL:
                    self.map[x,y]=225
                    self.town_hall[x,y] = True
                case PlotType.FARM:
                    self.map[x, y] = 175
                    self.farms[x,y] = True              
                case PlotType.MISC:
                    self.map[x,y]=150
                    self.misc[x,y] = True
                case PlotType.INN:
                    self.map[x,y]=125
                    self.inn[x,y] = True
                case PlotType.WELL:
                    self.map[x, y] = 100
                    self.well[x,y] = True
                case PlotType.DECORATION:
                    self.map[x, y] = 75
                    self.decoration[x,y] = True
                case PlotType.CHURCH:
                    self.map[x,y]=50
                    self.church[x,y] = True
                case PlotType.BORDER:
                    self.map[x,y]=35
                case PlotType.CITYWALL:
                    self.map[x,y]=15
                    self.city_walls[x,y]=True

    def show(self, save = True):
        rotated_image = np.rot90(self.map)
        pixel_assignments = {
            15: "CITYWALL",
            35: "BORDER",
            50: "CHURCH",
            75: "DECORATION",
            100: "WELL",
            125: "INN",
            150: "MISC",
            175: "FARM",
            200: "ROAD",
            225: "TOWNHALL",
            255: "HOUSE",
        }

        legend_values = sorted(list(pixel_assignments.keys()))
        legend_labels = [pixel_assignments[val] for val in legend_values]

        fig, ax = plt.subplots(figsize=(8, 6))

        im = ax.imshow(rotated_image, interpolation='nearest', origin='lower',
                        vmin=0, vmax=255)
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.8)

        cbar.set_label('Pixel Value (Intensity)', fontsize=12)

        cbar.set_ticks(legend_values)
        cbar.set_ticklabels(legend_labels, fontsize=10)
        if save:
            plt.savefig("blueprint")
        plt.show()

    def save_water_map(self, save = True):
        rotated_image = np.rot90(self.ground_water_map)
        pixel_assignments = {
            1: "Water",
            255: "No water presence",
        }

        legend_values = sorted(list(pixel_assignments.keys()))
        legend_labels = [pixel_assignments[val] for val in legend_values]

        fig, ax = plt.subplots(figsize=(8, 6))

        im = ax.imshow(rotated_image, interpolation='nearest', origin='lower',
                        vmin=0, vmax=255)
        cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.8)

        cbar.set_label('Pixel Value (Intensity)', fontsize=12)

        cbar.set_ticks(legend_values)
        cbar.set_ticklabels(legend_labels, fontsize=10)
        if save:
            plt.savefig("water_map")
        plt.show()

    def penalty(self, x):
        if x:
            return 10000
        return 0
    
    def feature_map_penalty(self, x):
        if x:
            return 255
        return 0

    def exp_penalty(self, x):
        if x:
            if x < 30:
                return math.exp(x)
            else:
                return 10000
        return 0

    def deactivate_border_region(self, matrix):
        if not isinstance(self.border_size, int) or self.border_size < 0:
            raise ValueError("--- border_size must be a non-negative integer ---")

        rows, cols = matrix.shape
        mask = np.zeros((rows, cols), dtype=bool)

        effective_border_size = min(self.border_size, (rows + 1) // 2, (cols + 1) // 2)

        if effective_border_size == 0:
            return mask


        mask[:effective_border_size, :] = True
        mask[rows - effective_border_size:, :] = True
        mask[:, :effective_border_size] = True
        mask[:, cols - effective_border_size:] = True
        
        return mask
    
    def get_traversable_map(self):
        penalty = np.vectorize(self.penalty)
        exp_penalty = np.vectorize(self.exp_penalty)
        traversable = exp_penalty(self.steepness_map) + penalty(self.ground_water_map != 255).astype(int) + penalty(self.lava_map != 255).astype(int) + penalty(np.logical_and(self.map > 1, self.map != 200)).astype(int) + penalty(self.deactivate_border_region(self.map))
        return traversable
    
    
    def get_buildable_area(self,
                       step_size=4,
                       gaussian=False,
                       radius=1):

        x_size = (self.steepness_map.shape[0] + step_size - 1) // step_size -1
        z_size = (self.steepness_map.shape[1] + step_size - 1) // step_size -1
        buildable_regions = np.empty((x_size, z_size), dtype=float)
        penalty = np.vectorize(self.feature_map_penalty)
        for i in range(x_size):
            for j in range(z_size):
                x_start = i * step_size
                x_end   = min(x_start + step_size, self.steepness_map.shape[0])
                z_start = j * step_size
                z_end   = min(z_start + step_size, self.steepness_map.shape[1])
                buildable_regions[i, j] = np.mean(self.steepness_map[x_start:x_end, z_start:z_end] + penalty(self.ground_water_map[x_start:x_end, z_start:z_end] != 255).astype(int) + penalty(self.lava_map[x_start:x_end, z_start:z_end] != 255).astype(int))

        if gaussian:
            buildable_regions = gaussian_filter(buildable_regions, sigma=1, radius=radius)

        return buildable_regions

    
    def get_town_center(self, step_size=32, gaussian=False, radius=1):
        b_area = self.get_buildable_area(step_size=step_size, gaussian=gaussian, radius=radius)
        print(b_area)
        rel_pos = np.array(np.unravel_index(np.argmin(b_area), b_area.shape))
        print(rel_pos)
        
        rel_pos = [rel_pos[0]*step_size, rel_pos[1]*step_size]
        return b_area, rel_pos
    
    def get_subregion(self, pos, region_size = 32, gaussian=False, radius=1):
        height_map = self.height_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        ground_water_map = self.ground_water_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        lava_map = self.lava_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        steepness_map = self.steepness_map[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        subregion = self.get_buildable_area(step_size=1, gaussian=gaussian, radius=radius)[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        
        return height_map, ground_water_map, lava_map, steepness_map, subregion
    
    def get_center_district_map(self, step_size=32):
        pass
    
    def reload_feature_maps(self):
        self.map_features.reload_world_slice()
        self.height_map = self.map_features.create_heightmap()
        self.steepness_map = self.map_features.create_gradient_maps()[4]
        self.ground_water_map = self.map_features.create_groundwater_map()
        self.lava_map = self.map_features.create_lava_map()

    def set_plot_height(self, plot: Rect, height: int):
        for x,y in plot:
            self.plot_heights[x,y] = height
        