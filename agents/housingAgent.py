import numpy as np
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.house import build_wooden_house
from gdpc.vector_tools import Rect

class HousingAgent(StructuralAgent):

    def __init__(self, blueprint,
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
                         activation_step, priority, 
                         max_slope,
                         max_plots,
                         outside_walls,
                         border,
                         sizes)
        
        self.type = PlotType.HOUSE

    def evaluate(self, loc, border_size=3):
        traversable = self.blueprint.map <= 15
        traversable &= self.blueprint.steepness_map <= self.road_connector_agent.max_slope
        path = BFS.find_minimal_path_to_network_boolean(traversable, loc, self.blueprint.road_network)
        if path is None:
            traversable_n = self.blueprint.get_traversable_map(border_size)
            path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
            if path is None:
                return -np.inf
        
        traversable = np.ones((self.blueprint.map.shape[0], self.blueprint.map.shape[1]), dtype=bool)
        path_to_church = BFS.find_minimal_path_to_network_boolean(traversable, loc, self.blueprint.church)
        if path_to_church is None:
            return - len(path), path
        return -len(path_to_church), path
    
    def build(self, loc, w, h):
        print(f"loc: {loc}, w: {w}, h:{h}")
        area = Rect((loc[0],loc[1]), (w,h))
        build_wooden_house(self.blueprint.map_features.editor, area, (1,0,0), 0)