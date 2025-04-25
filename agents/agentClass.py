from abc import ABC, abstractmethod
import numpy as np
from maps.blueprint import Blueprint
from .plots import PlotType

class Agent(ABC):
    def __init__(self, blueprint: Blueprint):
        self.type: PlotType
        self.blueprint = blueprint

    @abstractmethod
    def evaluate_location_fitness(self, loc: np.ndarray):
        pass

    def place(self, loc: np.ndarray):
        self.blueprint.place(loc, self.type)
        pass
