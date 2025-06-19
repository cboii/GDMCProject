import numpy as np
from random import choice

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Misc.misc import build_misc, tile_sizes
from gdpc.vector_tools import Rect

class MiscAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = PlotType.MISC

    
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