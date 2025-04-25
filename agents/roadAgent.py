import numpy as np
from .agentClass import Agent
from .plots import PlotType
import random

class RoadExtendorAgent(Agent):

    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = 3
        self.max_slope = 1


    def evaluate_location_fitness(self, loc):
        pass

    def place(self, loc):
        super().place(loc)
        pass



class RoadConnectorAgent(Agent):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = 3
        self.max_slope = 1
    
    def optimize(self):
        pass