import numpy as np
from random import choice

from .bfs import BFS

from .StructuralAgent import StructuralAgent
from .plots import PlotType
from buildings.buildingModules.Inn.inn import build_inn
from gdpc.vector_tools import Rect


class InnAgent(StructuralAgent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = PlotType.INN
    
    def build(self, loc, w, h):
        area = Rect((loc[0],loc[1]), (w,h))
        wood_type = choice(["oak", "spruce"])
        build_inn(self.blueprint, area, wood_type=wood_type)