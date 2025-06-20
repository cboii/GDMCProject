import numpy as np
from random import choice

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Decoration.decoration import build_decoration
from gdpc.vector_tools import Rect


class DecorationAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = PlotType.DECORATION

    def evaluate(self, loc, border_size=3):
        f = np.vectorize(self.blueprint.penalty)
        n_build_map = 1 + f(self.blueprint.ground_water_map != 255).astype(int) + f(self.blueprint.map >= 1).astype(int) + f(self.deactivate_border_region(self.blueprint.map, border_size=border_size))
        n_traversable = n_build_map
        path = BFS.find_minimal_path_to_network_numeric(n_traversable, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        
        traversable = np.ones((self.blueprint.map.shape[0], self.blueprint.map.shape[1]), dtype=bool)
        path_to_church = BFS.find_minimal_path_to_network_boolean(traversable, loc, self.blueprint.church)
        if path_to_church is None:
            return - len(path), path
        return -len(path_to_church), path
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        wood_type = choice(["oak", "spruce"])
        build_decoration(self.blueprint, area, wood_type=wood_type)