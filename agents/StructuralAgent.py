from collections import deque
import random
from matplotlib import pyplot as plt
import numpy as np

from Error import CustomError
from .bfs import BFS

from .plots import PlotType
from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from scipy.signal import convolve2d
from .roadAgent import RoadConnectorAgent
import random
import numpy as np
from scipy.ndimage import label
from scipy import ndimage
from scipy.signal import convolve2d

class StructuralAgent(Agent):
    def __init__(self, 
                 blueprint, 
                 search_area, 
                 road_connector_agent: RoadConnectorAgent, 
                 activation_step, priority, 
                 max_slope, 
                 min_width, 
                 min_height, 
                 max_width, 
                 max_height,
                 max_plots):
        super().__init__(blueprint)
        self.road_connector_agent = road_connector_agent
        self.min_coords = search_area[0]
        self.max_coords = search_area[1]
        self.activation_step = activation_step
        self.priority = priority
        self.max_slope = max_slope
        self.current_choice = None

        self.min_width=min_width
        self.min_height=min_height
        self.max_width=max_width
        self.max_height=max_height
        self.min_size = self.min_width * self.min_height

        self.plots_left = max_plots
        
        self.terrain_manipulator = TerrainManipulator(self.blueprint)

    @staticmethod
    def extract_random_box_and_border(region_mask: np.ndarray,
                                            min_width: int,
                                            min_height: int,
                                            max_width: int,
                                            max_height: int,
                                            border: int = 1
                                           ) -> tuple[np.ndarray, np.ndarray] | None:
        
        mask_int = region_mask.astype(np.int32)
        rows, cols = mask_int.shape

        sizes = [(h, w)
                 for h in range(min_height, max_height + 1)
                 for w in range(min_width,  max_width + 1)]
        random.shuffle(sizes)

        matching_locs = []
        for h, w in sizes:
            
            if h > rows or w > cols:
                continue

            kernel = np.ones((h, w), dtype=np.int32)
            conv = convolve2d(mask_int, kernel, mode="valid")
            target = h * w
            matches = np.argwhere(conv == target)
            if matches.size:
                i, j = matches[random.randrange(len(matches))]
                top, left = int(i), int(j)
                bottom, right = top + h, left + w

                rect_mask = np.zeros_like(region_mask, dtype=bool)
                rect_mask[top:bottom, left:right] = True

                inner_top = top + border
                inner_left = left + border
                inner_bottom = bottom - border
                inner_right = right - border

                if inner_top < inner_bottom and inner_left < inner_right:
                    inner_mask = np.zeros_like(region_mask, dtype=bool)
                    inner_mask[inner_top:inner_bottom, inner_left:inner_right] = True
                    border_mask = rect_mask & ~inner_mask
                else:
                    border_mask = rect_mask.copy()

                matching_locs.append([rect_mask, border_mask])
                # return rect_mask, border_mask

        return matching_locs
    
    def choose(self, expansion, gaussian=False, radius=1):
        expansion = expansion

        expansion_left = expansion
        expansion_right = expansion
        expansion_top = expansion
        expansion_bottom = expansion

        if (self.min_coords[0] - expansion < 0 and self.min_coords[1] - expansion < 0) and (self.max_coords[0] + expansion > (self.blueprint.map.shape[0] - 1) and self.max_coords[1] + expansion > (self.blueprint.map.shape[1] - 1)):
            raise IndexError(f"Agent of type {self.type.name}: Borders reached")
        
        if self.max_coords[1] + expansion > (self.blueprint.map.shape[1] - 1):
            expansion_top = 0
        
        if self.min_coords[1] - expansion < 0:
            expansion_bottom = 0

        if self.min_coords[0] - expansion < 0:
            expansion_left = 0

        if self.max_coords[0] + expansion > (self.blueprint.map.shape[0] - 1):
            expansion_right = 0

        
        
        region_size = max([(self.max_coords[0] + expansion_right) - (self.min_coords[0] - expansion_left) + 1, (self.max_coords[1] + expansion_top) - (self.min_coords[1] - expansion_bottom) + 1])
        
        height_map, ground_water_map, steepness_map, subregion = self.blueprint.get_subregion((self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom), region_size=region_size, gaussian=gaussian, radius=radius)
        
        buildable_areas = steepness_map <= self.max_slope
        buildable_areas &= ~(ground_water_map != 255)

        build_mask = np.logical_and(buildable_areas, (self.blueprint.map[(self.min_coords[0] - expansion_left): (self.min_coords[0] - expansion_left) + region_size, (self.min_coords[1] - expansion_bottom): (self.min_coords[1] - expansion_bottom) + region_size] == 0))
        build_mask &= ~(self.create_border_mask(build_mask))
        labeled_array, num_features = label(build_mask, structure=[[0,1,0], [1,1,1], [0,1,0]])

        sizes = ndimage.sum(labeled_array, labeled_array, range(num_features + 1))/range(num_features + 1)
        mask = (sizes >= self.min_size)


        filtered_labels = np.where(mask)[0]
        result = np.copy(labeled_array)
        result[~np.isin(result, filtered_labels)] = 0

        max_label = num_features + 1 

        boxes = []
        region_sizes = []
        for label_id in filtered_labels:
            region_mask = (labeled_array == label_id)
            region_size = np.sum(region_mask)
            region_sizes.append(region_size)

            region_mask = (labeled_array == label_id)
            region_size = np.sum(region_mask)

            boxes.extend(self.extract_random_box_and_border(region_mask, self.min_width, self.min_height, self.max_width, self.max_height, border=1))
        
        if len(boxes) == 0:
            self.min_coords = [self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom]
            self.max_coords = [self.max_coords[0] + expansion_right, self.max_coords[1] + expansion_top]
            self.current_choice = None
            return
        
        max_score = -np.inf
        for b in boxes:
            result = np.copy(labeled_array)
            result[~np.isin(result, filtered_labels)] = 0
            sub_region = b[0]
            border_mask = b[1]

            if not np.sum(sub_region) < self.min_size:
                result[sub_region] = max_label

            area = result == max_label
            area &= ~border_mask
            indices = np.argwhere(area)
            indices_borders = np.argwhere(border_mask)

            offset_coords = indices + np.array([self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom])
            offset_coords_border = indices_borders + np.array([self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom])
            
            score = self.evaluate(offset_coords)
            if score > max_score:
                max_score = score
                self.current_choice = [offset_coords, offset_coords_border]
            
        print(f"Max score: {max_score}")

    def create_border_mask(self, matrix, border_size=3):
        if not isinstance(border_size, int) or border_size < 0:
            raise ValueError("border_size must be a non-negative integer")

        rows, cols = matrix.shape
        mask = np.zeros((rows, cols), dtype=bool)

        effective_border_size = min(border_size, (rows + 1) // 2, (cols + 1) // 2)

        if effective_border_size == 0:
            return mask


        mask[:effective_border_size, :] = True
        mask[rows - effective_border_size:, :] = True
        mask[:, :effective_border_size] = True
        mask[:, cols - effective_border_size:] = True
        
        return mask

    def evaluate(self, loc):
        _, dist = BFS.find_minimal_path_to_network(self.blueprint, self.road_connector_agent.max_slope, loc, self.blueprint.road_network)
        if dist == None:
            return -np.inf
        return -dist

    def place(self):
        super().place(self.current_choice[0])
        self.blueprint.place(self.current_choice[1], PlotType.BORDER)
        self.plots_left -= 1
        pass
