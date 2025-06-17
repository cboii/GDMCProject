import numpy as np
from random import choice

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Misc.misc import build_misc, tile_sizes
from gdpc.vector_tools import Rect

class MiscAgent(StructuralAgent):

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
        
        self.type = PlotType.MISC

    def evaluate(self, loc, border_size=3):
        traversable_n = self.blueprint.get_traversable_map(border_size)
        path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        return len(loc), path
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        module = None
        for m, ts in tile_sizes.items():
            if (ts.x == area.size.x and ts.z == area.size.y) or (ts.x == area.size.y and ts.z == area.size.x):
                module = m
                self.sizes.remove((ts.x,ts.z))
                self.sizes.remove((ts.z,ts.x))
                break
        
        wood_type = choice(["oak", "spruce"])
        build_misc(self.blueprint, module, area, wood_type=wood_type)