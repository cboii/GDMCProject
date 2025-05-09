from abc import ABC
import numpy as np
from maps.blueprint import Blueprint
from .plots import PlotType

class Agent(ABC):
    def __init__(self, blueprint: Blueprint):
        self.type: PlotType
        self.blueprint = blueprint
        self.activation_step = 0

    def place(self, loc: np.ndarray):
        self.blueprint.place(loc, self.type)
        pass
