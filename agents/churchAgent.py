import itertools
import random

import numpy as np

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType


class ChurchAgent(StructuralAgent):

    def __init__(self, 
                 blueprint, 
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
                         activation_step, 
                         priority, 
                         max_slope,
                         min_width, 
                         min_height, 
                         max_width, 
                         max_height,
                         max_plots)
        
        self.type = PlotType.CHURCH

    def evaluate(self, loc):
        traversable = self.blueprint.map <= 15
        traversable &= self.blueprint.steepness_map <= self.road_connector_agent.max_slope
        _, dist = BFS.find_minimal_path_to_network(traversable, loc, self.blueprint.road_network)
        if dist == None:
            return -np.inf
        return len(loc)