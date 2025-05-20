import numpy as np
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .StructuralAgent import StructuralAgent
from .plots import PlotType


class HousingAgent(StructuralAgent):

    def __init__(self, blueprint, 
                 search_area, 
                 road_connector_agent, 
                 activation_step, 
                 priority, 
                 max_slope,
                 min_width, 
                 min_height, 
                 max_width, 
                 max_height,
                 max_plots):
        super().__init__(blueprint, 
                         search_area, 
                         road_connector_agent, 
                         activation_step, priority, 
                         max_slope,
                         min_width, 
                         min_height, 
                         max_width, 
                         max_height,
                         max_plots)
        
        self.max_distance_to_road = 2
        self.max_slope = max_slope
        self.type = PlotType.HOUSE

        self.min_border_size = 1
        self.terrain_manipulator = TerrainManipulator(self.blueprint)


        self.min_width=min_width
        self.min_height=min_height
        self.max_width=max_width
        self.max_height=max_height
        self.min_size = self.min_width * self.min_height

    def evaluate(self, loc):
        build_map = self.blueprint.map < 1
        build_map &= self.blueprint.steepness_map <= self.road_connector_agent.max_slope
        traversable = build_map
        _, dist = BFS.find_minimal_path_to_network(traversable, loc, self.blueprint.road_network)
        if dist == None:
            return -np.inf
        else:
            traversable = np.ones((self.blueprint.map.shape[0], self.blueprint.map.shape[1]), dtype=bool)
            _, dist_to_church = BFS.find_minimal_path_to_network(traversable, loc, self.blueprint.church)
            if dist_to_church == None:
                return -dist
            return -dist_to_church - dist