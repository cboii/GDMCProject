import numpy as np

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Church.church import build_church
from gdpc.vector_tools import Rect


class ChurchAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = PlotType.CHURCH

    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        build_church(self.blueprint, area)