import numpy as np

from Error import CustomError
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from .plots import PlotType
import numpy as np

class RoadExtendorAgent(Agent):

    def __init__(self, blueprint, max_width, max_slope):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = max_width
        self.max_slope = max_slope

    def place(self, loc):
        super().place(loc)
        pass



class RoadConnectorAgent(Agent):
    def __init__(self, blueprint, max_width, max_slope):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = max_width
        self.max_slope = max_slope

        self.terrain_manipulator = TerrainManipulator(self.blueprint)

    def penalty(self, x):
        if x:
            return 10000
        return 0

    def connect_to_road_network(self, path, execute = False):
        # penalty = np.vectorize(self.penalty)
        # traversable_n = self.blueprint.steepness_map + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(self.blueprint.map > 15).astype(int) + penalty(self.deactivate_border_region(self.blueprint.map, border_size=border_size))
        # path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        # if path is None:
        #     raise CustomError("No optimal path found!")
        path = self.construct_road(path)
        self.place(path)

        if execute:
            self.terrain_manipulator.place_road_segment(path)

    def construct_road(self, road_coords):
        road_coordinates = set(road_coords)
        
        for wc in road_coords:
            x, y = wc
            movements = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

            for dx, dy in movements:
                neighbor_x, neighbor_y = x + dx, y + dy
                if 0 <= neighbor_x < self.blueprint.map.shape[0] and 0 <= neighbor_y < self.blueprint.map.shape[1] and self.blueprint.map[neighbor_x, neighbor_y] <=15:
                    road_coordinates.add((neighbor_x, neighbor_y))
        return list(road_coordinates)
    
    def place(self, loc):
        super().place(loc)
        pass

