import numpy as np
from random import choice

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Decoration.decoration import build_decoration
from gdpc.vector_tools import Rect


class DecorationAgent(StructuralAgent):

    def __init__(self, 
                 blueprint,
                 road_connector_agent, 
                 activation_step, 
                 priority, 
                 max_slope,
                 max_plots,
                 outside_walls,
                 border=1,
                 sizes=[]):
        super().__init__(blueprint,
                         road_connector_agent, 
                         activation_step, 
                         priority, 
                         max_slope,
                         max_plots,
                         outside_walls,
                         border,
                         sizes)
        
        self.type = PlotType.DECORATION

    def evaluate(self, loc):
        penalty = np.vectorize(self.blueprint.penalty)
        n_build_map = 1 + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(self.blueprint.map >= 1).astype(int) + penalty(self.deactivate_border_region(self.blueprint.map))
        n_traversable = n_build_map
        path = BFS.find_minimal_path_to_network_numeric(n_traversable, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        return - len(path) - self.sum_steepness(loc), path
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        wood_type = choice(["oak", "spruce"])
        build_decoration(self.blueprint, area, wood_type=wood_type)