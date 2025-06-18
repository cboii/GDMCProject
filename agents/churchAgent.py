import numpy as np

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Church.church import build_church
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

    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        build_church(self.blueprint, area)