import numpy as np

from .bfs import BFS
from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Farm.farm import build_farm
from gdpc.vector_tools import Rect
from random import choice

class FarmAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = PlotType.FARM

    def evaluate(self, loc):
        traversable_n = self.blueprint.get_traversable_map()
        path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
            
        traversable = np.ones(self.blueprint.map.shape)
        path_to_own = BFS.find_minimal_path_to_network_numeric(traversable, loc, [tuple(x) for x in np.argwhere(self.blueprint.farms)])
        if path_to_own is None:
            return - len(path) - self.sum_steepness(loc), path
        return - len(path_to_own) - self.sum_steepness(loc), path
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        wood_type = choice(["oak", "spruce"])
        build_farm(self.blueprint, area, wood_type=wood_type)