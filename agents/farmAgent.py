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
        
        self.max_distance_to_road = 10
        self.max_slope = max_slope
        self.type = PlotType.FARM

        self.min_width=min_width
        self.min_height=min_height
        self.max_width=max_width
        self.max_height=max_height

    def evaluate(self, loc):
        _, dist = BFS.find_minimal_path_to_network(self.blueprint, self.road_connector_agent.max_slope, loc, self.blueprint.road_network)
        if dist == None:
            return -np.inf
        _, dist_to_own = BFS.find_minimal_path_to_network(self.blueprint, self.max_slope, loc, self.blueprint.farms)
        if dist_to_own == None:
            return -dist
        return -dist_to_own