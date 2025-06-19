import random
import numpy as np

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
                 road_connector_agent: RoadConnectorAgent, 
                 activation_step, priority, 
                 max_slope,
                 max_plots,
                 outside_walls=False,
                 inside_walls=None,
                 border=1,
                 sizes=[],
                 road_connection=True):
        super().__init__(blueprint)
        self.road_connector_agent = road_connector_agent
        self.activation_step = activation_step
        self.priority = priority
        self.max_slope = max_slope
        self.current_choice = None
        self.current_path = None
        self.border_size = border
        self.road_connection = road_connection

        self.outside_walls = outside_walls

        self.sizes = sizes
        self.min_size = np.min([h + 2*border for h,w in sizes]) * np.min([w + 2*border for h,w in sizes])
        print(self.min_size)
        self.plots_left = max_plots
        
        self.terrain_manipulator = TerrainManipulator(self.blueprint)
        self.inside_walls = inside_walls
        # print(self.sizes)

    def __extract_boxes_and_borders(self, region_mask: np.ndarray,
                                            border: int = 1
                                           ) -> tuple[np.ndarray, np.ndarray] | None:
        
        mask_int = region_mask.astype(np.int32)
        rows, cols = mask_int.shape

        sizes = [(h + 2 * border, w + 2 * border) for h,w in self.sizes]
        # sizes = [(h, w)
        #          for h in range(min_height, max_height + 1)
        #          for w in range(min_width,  max_width + 1)]
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


    def choose(self, search_area, gaussian=False, radius=1, border_size=3):
        region_size = max([(search_area[1][0]) - (search_area[0][0]) + 1, (search_area[1][1]) - (search_area[0][1]) + 1])
        height_map, ground_water_map, steepness_map, subregion = self.blueprint.get_subregion((search_area[0][0], search_area[0][1]), region_size=region_size, gaussian=gaussian, radius=radius)
        buildable_areas = steepness_map <= self.max_slope
        buildable_areas &= ~(ground_water_map != 255)

        build_mask = np.logical_and(buildable_areas, (self.blueprint.map[(search_area[0][0]): (search_area[0][0]) + region_size, (search_area[0][1]): (search_area[0][1]) + region_size] == 0))
        build_mask &= ~(self.deactivate_border_region(build_mask, border_size=border_size))

        if self.outside_walls and self.blueprint.outside_walls_area.any():
            print(f"--- Wall restriction active for agent of type {self.type.name} ---")
            build_mask = np.logical_and(build_mask, (self.blueprint.outside_walls_area[(search_area[0][0]): (search_area[0][0]) + region_size, (search_area[0][1]): (search_area[0][1]) + region_size]))
        elif (self.outside_walls):
            self.current_choice = None
            self.current_path = None
            raise NoneTypeChoice("--- No city walls placed yet ---")
        
        if self.inside_walls and self.blueprint.outside_walls_area.any():
            print(f"--- Wall restriction active for agent of type {self.type.name} ---")
            build_mask = np.logical_and(build_mask, ~(self.blueprint.outside_walls_area[(search_area[0][0]): (search_area[0][0]) + region_size, (search_area[0][1]): (search_area[0][1]) + region_size]))


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

            boxes.extend(self.__extract_boxes_and_borders(region_mask, border=border_size))
        
        if len(boxes) == 0:
            self.current_choice = None
            self.current_path = None
            raise NoneTypeChoice("--- No candidates found ---")
        
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

            offset_coords = indices + np.array([search_area[0][0], search_area[0][1]])
            offset_coords_border = indices_borders + np.array([search_area[0][0], search_area[0][1]])
            
            res = self.evaluate(offset_coords)
            if type(res) == float:
                self.current_choice = None
                self.current_path = None
                raise NoValidPath("--- Cannot connect to road network ---")
             
            score, path = res
            if score > max_score:
                max_score = score
                self.current_choice = [offset_coords, offset_coords_border]
                self.current_path = path
            
        if max_score == -np.inf:
            self.current_choice = None
            self.current_path = None
            raise NoValidPath("--- Cannot connect to road network ---") 

    def deactivate_border_region(self, matrix, border_size=3):
        if not isinstance(border_size, int) or border_size < 0:
            raise ValueError("--- border_size must be a non-negative integer ---")

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

    def sum_steepness(self, loc):
        return sum([self.blueprint.steepness_map[tuple(l)] for l in loc])
    
    def evaluate(self, loc):
        traversable_n = self.blueprint.get_traversable_map()
        path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        return len(loc) - self.sum_steepness(loc), path

    def place(self):
        super().place(self.current_choice[0])
        self.blueprint.place(self.current_choice[1], PlotType.BORDER)
        self.plots_left -= 1
        pass


class NoneTypeChoice(Exception):
    pass

class NoValidPath(Exception):
    pass