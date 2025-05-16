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
        path, dist = BFS.find_minimal_path_to_network(self.blueprint, self.max_slope, loc, self.blueprint.road_network)
        if dist == None:
            raise CustomError("No optimal path found!")
        self.place(path)

        if execute:
            self.terrain_manipulator.place_road_segment(path)
        pass
    
    def place(self, loc):
        super().place(loc)
        pass

