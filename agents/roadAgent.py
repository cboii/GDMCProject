import numpy as np

from Error import CustomError
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from .plots import PlotType
import numpy as np

class RoadConnectorAgent(Agent):
    def __init__(self, blueprint, max_width, max_slope):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = max_width
        self.max_slope = max_slope

        self.terrain_manipulator = TerrainManipulator(self.blueprint)

    def connect_to_road_network(self, path, execute = False):
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
                if 0 <= neighbor_x < self.blueprint.map.shape[0] and 0 <= neighbor_y < self.blueprint.map.shape[1] and self.blueprint.map[neighbor_x, neighbor_y] <=35:
                    road_coordinates.add((neighbor_x, neighbor_y))
        return list(road_coordinates)
    
    def place(self, loc):
        super().place(loc)
        pass

