from skimage import filters, color, morphology
from skimage.segmentation import flood, flood_fill
from .featureMaps import MapFeatureExtractor
from gdpc import Editor, Block
import numpy as np
from scipy.ndimage import gaussian_filter

class BuildMap:
    def __init__(self, editor: Editor):
        self.editor = editor
        self.map_features = MapFeatureExtractor(editor)
        self.height_map = self.map_features.create_heightmap()
        self.ground_water_map = self.map_features.create_groundwater_map()
        self.steepness_map = self.map_features.create_gradient_maps()[4]
        self.offest = self.map_features.build_area.offset

    def get_buildable_area(self, step_size = 4, gaussian = False):

        # Initialize a grid of size (self.steepness_map.shape[0]/step_size, self.steepness_map.shape[1]/step_size)
        buildable_regions = np.empty((int(self.steepness_map.shape[0]/step_size), int(self.steepness_map.shape[1]/step_size)), dtype=float) 
        for x in range(0, self.steepness_map.shape[0], step_size):
            for z in range(0, self.steepness_map.shape[1], step_size):

                buildable_regions[round(x/(self.steepness_map.shape[0] - step_size) * (self.steepness_map.shape[0]/step_size - 1)), round(z/(self.steepness_map.shape[1] - step_size) * (self.steepness_map.shape[1]/step_size - 1))] = np.mean(self.steepness_map[x: x + step_size,z: z + step_size])

        # Exclude water
        max = np.max(buildable_regions)
        for x in range(0, self.steepness_map.shape[0], step_size):
            for z in range(0, self.steepness_map.shape[1], step_size):
                
                if np.any(self.ground_water_map[x: x + step_size,z: z + step_size] != 255): 
                    buildable_regions[round(x/(self.steepness_map.shape[0] - step_size) * (self.steepness_map.shape[0]/step_size - 1)), round(z/(self.steepness_map.shape[1] - step_size) * (self.steepness_map.shape[1]/step_size - 1))] = max

        if gaussian:
            buildable_regions = gaussian_filter(buildable_regions, sigma=1, radius=1)
        
        return buildable_regions
    
    def get_town_center(self, step_size=32, gaussian=False):
        b_area = self.get_buildable_area(step_size=step_size, gaussian=gaussian)
        rel_pos = np.array(np.unravel_index(np.argmin(b_area), b_area.shape))
        rel_pos = (rel_pos[0]*step_size, rel_pos[1]*step_size)
        
        return b_area, rel_pos
    
    def get_subregion(self, pos, region_size = 32):
        subregion = self.get_buildable_area(step_size=1)[pos[0]: pos[0] + region_size, pos[1]: pos[1] + region_size]
        return subregion
    
    def get_center_district_map(self, step_size=32):
        pass