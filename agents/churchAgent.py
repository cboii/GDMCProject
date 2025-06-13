import numpy as np

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.church import build_church
from gdpc.vector_tools import Rect


class ChurchAgent(StructuralAgent):

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
        
        self.type = PlotType.CHURCH

    def evaluate(self, loc, border_size=3):
        traversable_n = self.blueprint.get_traversable_map(border_size)
        path = BFS.find_minimal_path_to_network_numeric(traversable_n, loc, [tuple(x) for x in np.argwhere(self.blueprint.road_network)])
        if path is None:
            return -np.inf
        return len(loc), path
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        build_church(self.blueprint.map_features.editor, area, (0,0,0), 0)