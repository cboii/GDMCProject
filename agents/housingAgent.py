from random import choice
import numpy as np
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.plot_utils import get_entrance_direction
from buildings.buildingModules.House.house import build_wooden_house
from gdpc.vector_tools import Rect

class HousingAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = PlotType.HOUSE

    def evaluate(self, loc):
        traversable_n = self.blueprint.get_traversable_map()
        path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        
        traversable = np.ones(self.blueprint.map.shape)
        path_to_church = BFS.find_minimal_path_to_network_numeric(traversable, loc, [tuple(x) for x in np.argwhere(self.blueprint.church)])
        if path_to_church is None:
            return - len(path) - self.sum_steepness(loc), path
        return -len(path_to_church) - self.sum_steepness(loc), path
    
    def build(self, loc, w, h):
        print(f"loc: {loc}, w: {w}, h:{h}")
        area = Rect((loc[0],loc[1]), (w,h))
        wood_type = choice(["oak", "spruce"])
        self.blueprint.house_locs[f"house_{self.max_plots-self.plots_left}"] = Rect((loc[0],loc[1]), (w,h))
        build_wooden_house(self.blueprint, area, wood_type=wood_type)