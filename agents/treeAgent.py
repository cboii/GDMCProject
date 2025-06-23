import numpy as np
from random import choice

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Tree.tree import build_tree, tile_sizes
from gdpc.vector_tools import Rect


class TreeAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = PlotType.TREE

    def evaluate(self, loc):
        penalty = np.vectorize(self.blueprint.penalty)
        exp_penalty = np.vectorize(self.blueprint.exp_penalty)
        n_build_map = exp_penalty(self.blueprint.steepness_map) + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(np.logical_and(self.blueprint.map >= 1, self.blueprint.map != 200)).astype(int) + penalty(self.deactivate_border_region(self.blueprint.map))
        n_traversable = n_build_map
        path = BFS.find_minimal_path_to_network_numeric(n_traversable, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        return len(loc) - len(path) - self.sum_steepness(loc), path
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        module = None
        for m, ts in tile_sizes.items():
            if (ts.x == area.size.x and ts.z == area.size.y) or (ts.x == area.size.y and ts.z == area.size.x):
                module = m
                break

        wood_type = choice(["oak", "spruce"])
        build_tree(self.blueprint, module, area, wood_type=wood_type)