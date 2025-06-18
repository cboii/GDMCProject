from random import choice
import numpy as np

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.TownHall.townhall import build_townhall
from gdpc.vector_tools import Rect


class TownHallAgent(StructuralAgent):

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
        
        self.type = PlotType.TOWNHALL
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        wood_type = choice(["oak", "spruce"])
        build_townhall(self.blueprint, area, wood_type=wood_type)
