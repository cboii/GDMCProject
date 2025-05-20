from collections import deque

from matplotlib import pyplot as plt
from gdpc import Block
from scipy.spatial import ConvexHull

from maps.blueprint import Blueprint
from terrain.terrain_manipulator import TerrainManipulator
from .StructuralAgent import Agent
from .bfs import BFS
from .plots import PlotType
import numpy as np
import cv2 as cv


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

    def try_place(self):
        house_coordinates = np.argwhere(self.blueprint.map)
        area = []
        for x_step in [-3,0,3]:
            for z_step in [-3,0,3]:
                for coord in house_coordinates:
                    if coord[0]+x_step > self.blueprint.map.shape[0] - 1 or coord[0]+x_step < 0 or coord[1]+z_step > self.blueprint.map.shape[1] - 1 or coord[1]+z_step < 0:
                        continue
                    area.append([coord[0]+x_step, coord[1]+z_step])

        area = np.array(area)
        hull = ConvexHull(area)

        for i, vertex in enumerate(hull.vertices):
            self.place([area[vertex]])

        self.blueprint.show()
        build_map = self.blueprint.map <= 15
        build_map &= self.blueprint.steepness_map <= self.max_slope
        build_map &= ~(self.blueprint.ground_water_map != 255)
        traversable = build_map

        walls = self.connect_coordinates_in_order([tuple(area[vertex]) for vertex in hull.vertices], traversable)
        last_segment = self.connect_coordinates_in_order([tuple(area[hull.vertices[-1]]), tuple(area[hull.vertices[0]])], traversable)

        if walls != None and last_segment != None:
            walls.extend(last_segment)
            wall_coordinates = set([tuple(wall) for wall in walls])
        
            for wc in walls:
                x, y = wc
                movements = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

                for dx, dy in movements:
                    neighbor_x, neighbor_y = x + dx, y + dy
                    if 0 <= neighbor_x < self.blueprint.map.shape[0] and 0 <= neighbor_y < self.blueprint.map.shape[1]:
                        wall_coordinates.add((neighbor_x, neighbor_y))

            wall_coordinates = list(wall_coordinates)
            self.place(wall_coordinates)
        else:
            return False

        for l in wall_coordinates:
            for h in range(10):
                self.blueprint.map_features.editor.placeBlock((self.blueprint.map_features.build_area.offset.x + int(l[0]), self.blueprint.height_map[int(l[0]), int(l[1])] + h - 1, self.blueprint.map_features.build_area.offset.z + int(l[1])), Block("cobblestone"))
        
        self.set_outside_area()
        
        return True

    def connect_coordinates_in_order(self, coordinates, mask):
        if not coordinates:
            return []

        full_tour = [coordinates[0]]

        for i in range(len(coordinates) - 1):
            start_node = coordinates[i]
            end_node = coordinates[i+1]

            path_segment = BFS.find_minimal_path_to_point(mask, start_node, end_node)

            if path_segment is None:
                print(f"No path found between {start_node} and {end_node}")
                return None

            full_tour.extend(path_segment[1:])

        return full_tour
    
    def set_outside_area(self):
        tmp = self.blueprint.city_walls.astype(np.uint8).copy()

        (cnts, _) = cv.findContours(
            tmp, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cv.drawContours(
            image=tmp,
            contours=cnts, contourIdx=-1,
            color=1, thickness=cv.FILLED)

        tmp = ~(tmp.astype(bool))
        self.blueprint.outside_walls_area = tmp

    def place(self, loc):
        super().place(loc)
        pass