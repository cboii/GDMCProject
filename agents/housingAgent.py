import itertools
import random

from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from .plots import PlotType
import numpy as np
from scipy.ndimage import label
from scipy import ndimage
from scipy.signal import convolve2d
from .roadAgent import RoadConnectorAgent


class HousingAgent(Agent):

    def __init__(self, blueprint, step_size = 32):
        super().__init__(blueprint)
        self.max_distance_to_road = 2
        self.max_slope = 2
        self.type = PlotType.HOUSE

        self.min_border_size = 1
        self.step_size = step_size
        self.terrain_manipulator = TerrainManipulator(self.blueprint)
        _, begin = self.blueprint.get_town_center(step_size=step_size)
        end = [begin[0] + step_size - 1, begin[1] + step_size - 1]
        self.min_coords = begin
        self.max_coords = end

        self.road_connector = RoadConnectorAgent(self.blueprint)
        self.road_connector.place([[begin[0]  + step_size // 2, begin[1] + step_size // 2]])

        self.min_width=8
        self.min_height=8
        self.max_width=14
        self.max_height=14
        self.min_size = self.min_width * self.min_height
        


    def find_suitable_build_areas(self, execute = False):
        expansion = self.step_size - 1
        if not self.blueprint.houses.any(where=lambda x: x):
            pass
        else:
            indices = np.argwhere(self.blueprint.houses)

            expansion_left = expansion
            expansion_right = expansion
            expansion_top = expansion
            expansion_bottom = expansion

            if (self.min_coords[0] - expansion < 0 and self.min_coords[1] - expansion < 0) and (self.max_coords[0] + expansion > (self.blueprint.map.shape[0] - 1) and self.max_coords[1] + expansion > (self.blueprint.map.shape[1] - 1)):
                raise IndexError("Borders reached")
            
            if self.max_coords[1] + expansion > (self.blueprint.map.shape[1] - 1):
                expansion_top = 0
                print("Upper Border reached")
            
            if self.min_coords[1] - expansion < 0:
                expansion_bottom = 0
                print("Lower Border reached")

            if self.min_coords[0] - expansion < 0:
                expansion_left = 0
                print("Left Border reached")

            if self.max_coords[0] + expansion > (self.blueprint.map.shape[0] - 1):
                expansion_right = 0
                print("Right Border reached")

            
            
            region_size = max([(self.max_coords[0] + expansion_right) - (self.min_coords[0] - expansion_left) + 1, (self.max_coords[1] + expansion_top) - (self.min_coords[1] - expansion_bottom) + 1])
            
            height_map, ground_water_map, steepness_map, subregion = self.blueprint.get_subregion((self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom), region_size=region_size, gaussian=False)
            
            buildable_areas = steepness_map < self.max_slope
            buildable_areas &= ~(ground_water_map != 255)

            # buildable_areas = subregion

            build_mask = np.logical_and(buildable_areas, ~self.blueprint.houses[(self.min_coords[0] - expansion_left): (self.min_coords[0] - expansion_left) + region_size, (self.min_coords[1] - expansion_bottom): (self.min_coords[1] - expansion_bottom) + region_size])
            
            build_mask&=(self.blueprint.map[(self.min_coords[0] - expansion_left): (self.min_coords[0] - expansion_left) + region_size, (self.min_coords[1] - expansion_bottom): (self.min_coords[1] - expansion_bottom) + region_size] == 0)
        

            labeled_array, num_features = label(build_mask, structure=[[0,1,0], [1,1,1], [0,1,0]])

            sizes = ndimage.sum(labeled_array, labeled_array, range(num_features + 1))/range(num_features + 1)
            mask = (sizes >= self.min_size)


            filtered_labels = np.where(mask)[0]
            result = np.copy(labeled_array)
            result[~np.isin(result, filtered_labels)] = 0

            max_label = num_features + 1 

            box = None
            region_sizes = []
            for label_id in filtered_labels:
                region_mask = (labeled_array == label_id)
                region_size = np.sum(region_mask)
                region_sizes.append(region_size)

                region_mask = (labeled_array == label_id)
                region_size = np.sum(region_mask)

                box = self.extract_random_box_and_border(region_mask, self.min_width, self.min_height, self.max_width, self.max_height, border=1)

                if box != None:
                    
                    break
            
            if box == None:
                self.min_coords = [self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom]
                self.max_coords = [self.max_coords[0] + expansion_right, self.max_coords[1] + expansion_top]
                raise ValueError

            sub_region = box[0]
            border_mask = box[1]


            if not np.sum(sub_region) < self.min_size:
            
                result[sub_region] = max_label

            house_area = result == max_label
            house_area &= ~border_mask
            indices = np.argwhere(house_area)
            indices_borders = np.argwhere(border_mask)

            offset_coords = indices + np.array([self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom])
            offset_coords_border = indices_borders + np.array([self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom])
            

            self.place(offset_coords)
            self.blueprint.place(offset_coords_border, PlotType.BORDER)
            self.road_connector.connect_to_road_network(offset_coords_border, execute=execute)

            if execute:
                w, h = [offset_coords[-1][0] - offset_coords[0][0] + 1, offset_coords[-1][1] - offset_coords[0][1] + 1]
                self.terrain_manipulator.place_base(offset_coords[0], w, h)

        # self.min_coords = [self.min_coords[0] - expansion_left, self.min_coords[1] - expansion_bottom]
        # self.max_coords = [self.max_coords[0] + expansion_right, self.max_coords[1] + expansion_top]


    def evaluate_location_fitness(self, loc):
        pass


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

                return rect_mask, border_mask

        return None
    

    def place(self, loc):
        super().place(loc)
        pass
