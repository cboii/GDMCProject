import numpy as np
from .bfs import BFS
from terrain.terrain_manipulator import TerrainManipulator
from .StructuralAgent import StructuralAgent
from .plots import PlotType


class HousingAgent(StructuralAgent):

    def __init__(self, blueprint, 
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
                         activation_step, priority, 
                         max_slope,
                         min_width, 
                         min_height, 
                         max_width, 
                         max_height,
                         max_plots)
        
        self.type = PlotType.HOUSE

    def evaluate(self, loc):
        traversable = self.blueprint.map <= 15
        traversable &= self.blueprint.steepness_map <= self.road_connector_agent.max_slope
        path = BFS.find_minimal_path_to_network_boolean(traversable, loc, self.blueprint.road_network)
        if path is None:
            f = np.vectorize(self.penalty)
            traversable_n = self.blueprint.steepness_map + f(self.blueprint.ground_water_map != 255).astype(int) + f(self.blueprint.map >= 1).astype(int)
            path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
            if path is None:
                return -np.inf
        
        traversable = np.ones((self.blueprint.map.shape[0], self.blueprint.map.shape[1]), dtype=bool)
        path_to_church = BFS.find_minimal_path_to_network_boolean(traversable, loc, self.blueprint.church)
        if path_to_church is None:
            return - len(path)
        return -len(path_to_church)