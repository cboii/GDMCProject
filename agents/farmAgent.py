import numpy as np

from .bfs import BFS
from .StructuralAgent import StructuralAgent
from .plots import PlotType

class FarmAgent(StructuralAgent):

    def __init__(self, 
                 blueprint, 
                 search_area, 
                 road_connector_agent, 
                 activation_step, priority, 
                 max_slope,
                 min_width, 
                 min_height, 
                 max_width, 
                 max_height,
                 max_plots,
                 outside_walls):
        super().__init__(blueprint, 
                         search_area, 
                         road_connector_agent, 
                         activation_step, 
                         priority, 
                         max_slope,
                         min_width, 
                         min_height, 
                         max_width, 
                         max_height,
                         max_plots,
                         outside_walls)
        self.type = PlotType.FARM

    def evaluate(self, loc):
        build_map = self.blueprint.map <= 15
        build_map &= self.blueprint.steepness_map <= self.road_connector_agent.max_slope
        traversable = build_map
        _, dist = BFS.find_minimal_path_to_network(traversable, loc, self.blueprint.road_network)
        if dist == None:
            return -np.inf
        traversable = np.ones((self.blueprint.map.shape[0], self.blueprint.map.shape[1]), dtype=bool)
        _, dist_to_own = BFS.find_minimal_path_to_network(traversable, loc, self.blueprint.farms)
        if dist_to_own == None:
            return -dist
        return -dist_to_own