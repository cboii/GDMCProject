from .agentClass import Agent
from .plots import PlotType

class RoadAgent(Agent):

    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.max_distance_to_road = 10
        self.max_slope = 2
        self.type = PlotType.FARM

    def evaluate_location_fitness(self, loc):
        pass

    def place(self, loc):
        super().place(loc)
        pass