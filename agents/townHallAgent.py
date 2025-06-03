import numpy as np

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType


class TownHallAgent(StructuralAgent):

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
        
        self.type = PlotType.TOWNHALL

    def penalty(self, x):
        if x:
            return 10000
        return 0

    def evaluate(self, loc, border_size=3):
        penalty = np.vectorize(self.penalty)
        traversable_n = self.blueprint.steepness_map + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(self.blueprint.map >= 1).astype(int) + penalty(self.deactivate_border_region(self.blueprint.map, border_size=border_size))
        path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        return len(loc), path