from scipy.spatial import ConvexHull

from maps.blueprint import Blueprint
from terrain.terrain_manipulator import TerrainManipulator
from .StructuralAgent import Agent
from .plots import PlotType
import numpy as np


class CityWallAgent(Agent):

    def __init__(self, blueprint: Blueprint,
                 activation_step, 
                 priority, 
                 max_slope,
                 min_width, 
                 min_height, 
                 max_width, 
                 max_height,
                 max_plots):
        super().__init__(blueprint)

        self.activation_step = activation_step
        self.priority = priority
        
        self.max_slope = max_slope
        self.type = PlotType.CITYWALL

        self.min_border_size = 2
        self.terrain_manipulator = TerrainManipulator(self.blueprint)


        self.min_width=min_width
        self.min_height=min_height
        self.max_width=max_width
        self.max_height=max_height
        self.min_size = self.min_width * self.min_height
        
        self.max_plots = max_plots

    def getHull(self):
        house_coordinates = np.argwhere(self.blueprint.map)
        area = []
        for x_step in [-2,0,2]:
            for z_step in [-2,0,2]:
                for coord in house_coordinates:
                    if coord[0]+x_step > self.blueprint.map.shape[0] - 1 or coord[0]+x_step < 0 or coord[1]+z_step > self.blueprint.map.shape[1] - 1 or coord[1]+z_step < 0:
                        continue
                    area.append([coord[0]+x_step, coord[1]+z_step])

        area = np.array(area)
        hull = ConvexHull(area)

        for i, vertex in enumerate(hull.vertices):
            self.place([area[vertex]])
                
            


    def place(self, loc):
        super().place(loc)
        pass