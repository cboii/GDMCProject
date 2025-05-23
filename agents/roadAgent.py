import numpy as np

from Error import CustomError
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from .plots import PlotType
import random
import numpy as np
from collections import deque

class RoadExtendorAgent(Agent):

    def __init__(self, blueprint, search_area, max_width, max_slope):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = max_width
        self.max_slope = max_slope

        self.min_coords = search_area[0]
        self.max_coords = search_area[1]

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

    def connect_to_road_network(self, loc, execute = False):
        build_map = self.blueprint.map <= 15
        build_map &= self.blueprint.steepness_map <= self.max_slope
        traversable = build_map
        path, dist = BFS.find_minimal_path_to_network(traversable, loc, self.blueprint.road_network)
        if dist == None:
            raise CustomError("No optimal path found!")
        path = self.construct_road(path)
        self.place(path)

        if execute:
            self.terrain_manipulator.place_road_segment(path)
        pass

    def construct_road(self, road_coords):
        road_coordinates = set([tuple(wall) for wall in road_coords])
        
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

