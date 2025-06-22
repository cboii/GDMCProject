from .roadAgent import RoadConnectorAgent
from gdpc import Block
from gdpc.geometry import placeCuboid
from scipy.spatial import ConvexHull

from buildings.buildingModules.CityWall.patterns import wall_patterns
from buildings.building_module import build_module_global
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
                 max_plots,
                 road_connector_agent: RoadConnectorAgent,
                 number_of_gates: 2):
        super().__init__(blueprint)

        self.activation_step = activation_step
        self.priority = priority
        
        self.max_slope = max_slope
        self.type = PlotType.CITYWALL

        self.min_border_size = 2
        self.terrain_manipulator = TerrainManipulator(self.blueprint)
        
        self.max_plots = max_plots

        self.road_connector_agent = road_connector_agent
        self.number_of_gates = number_of_gates

    def penalty(self, x):
        if x:
            return 10000
        return 0

    def try_place(self):
        house_coordinates = np.argwhere(self.blueprint.map)
        area = []
        for x_step in [-3,0,3]:
            for z_step in [-3,0,3]:
                for coord in house_coordinates:
                    if coord[0]+x_step > self.blueprint.map.shape[0] - 1 or coord[0]+x_step < 0 or coord[1]+z_step > self.blueprint.map.shape[1] - 1 or coord[1]+z_step < 0:
                        continue
                    if self.blueprint.ground_water_map[coord[0]+x_step,coord[1]+z_step] != 255:
                        continue
                    area.append([coord[0]+x_step, coord[1]+z_step])

        area = np.array(area)
        hull = ConvexHull(area)

        # for i, vertex in enumerate(hull.vertices):
        #     self.place([area[vertex]])

        # self.blueprint.show()

        penalty = np.vectorize(self.penalty)
        n_build_map = penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(np.logical_and(self.blueprint.map > 35, self.blueprint.map != 200)).astype(int)
        n_traversable = n_build_map

        walls = self.connect_coordinates_in_order([tuple(area[vertex]) for vertex in hull.vertices], n_traversable)
        last_segment = self.connect_coordinates_in_order([tuple(area[hull.vertices[-1]]), tuple(area[hull.vertices[0]])], n_traversable)
        #self.place([tuple(area[vertex]) for vertex in hull.vertices])
        
        if walls != None and last_segment != None:
            walls.extend(last_segment)
            wall_coordinates = self.construct_wall(walls)
            self.place(wall_coordinates)
            road_segments = []
            split = int((len(walls)-1)/self.number_of_gates)
            for i, w in enumerate(walls):
                if i % split == 0:
                    road_segments.append(self.road_connector_agent.construct_road([w], ignore_walls=True))
                    self.road_connector_agent.place(self.road_connector_agent.construct_road([w], ignore_walls=True))
                    penalty = np.vectorize(self.penalty)
                    traversable = self.blueprint.steepness_map + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(np.logical_and(self.blueprint.map > 1, self.blueprint.map != 200)).astype(int) + penalty(self.blueprint.deactivate_border_region(self.blueprint.map)) + penalty(self.blueprint.outside_walls_area)
                    rn_copy = np.ones_like(self.blueprint.road_network, dtype=bool)
                    for s in road_segments:
                        for c in s:
                            rn_copy[c] = False
                    path = BFS.find_minimal_path_to_network_numeric(traversable, [w], [tuple(x) for x in np.argwhere(self.blueprint.road_network & rn_copy)])
                    if path is None:
                        continue
                    self.road_connector_agent.connect_to_road_network(path, True)
            self.blueprint.show()
        else:
            return False
        
        self.set_outside_area()
        
        return True


    def construct_wall(self, wall_coords):
        wall_coordinates = set([tuple(wall) for wall in wall_coords])
        
        for wc in wall_coords:
            x, y = wc
            movements = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]

            for dx, dy in movements:
                neighbor_x, neighbor_y = x + dx, y + dy
                if 0 <= neighbor_x < self.blueprint.map.shape[0] and 0 <= neighbor_y < self.blueprint.map.shape[1] and self.blueprint.map[neighbor_x, neighbor_y] <= 1:
                    wall_coordinates.add((neighbor_x, neighbor_y))

        return list(wall_coordinates)
    
    """
    def execute_wall_placement(self):
        editor = self.blueprint.map_features.editor
        build_area = self.blueprint.map_features.build_area
        wall_coords = []
        for x,z in np.argwhere(self.blueprint.city_walls):
            directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
            neighborhood = np.zeros((3,3), dtype=int)
            
            for i,j in directions:
                if 0 <= x+i < self.blueprint.city_walls.shape[0] and 0 <= z+j < self.blueprint.city_walls.shape[1]:
                    neighborhood[i+1,j+1] = self.blueprint.city_walls[x+i,z+j]
                    wall_coords.append((x+i,z+j))
            if neighborhood.sum() != 3:
                print("No 2 neighbors")
                continue
            
            for p,n in wall_patterns:
                if np.equal(neighborhood, p).all():
                    build_module_global(editor, f"CityWall_{n[0]}#0", (build_area.offset.x + x - 2, self.blueprint.height_map[x,z], build_area.offset.z + z - 2), 
                                        (5,7,5), n[1], "oak", build_air=False)
                    
        wall_coords = list(set(wall_coords))
        
        self.place(wall_coords)            
        for x,z in np.argwhere(self.blueprint.city_walls & self.blueprint.road_network):
            placeCuboid(editor, (build_area.offset.x + x, self.blueprint.height_map[x,z]+1, build_area.offset.z + z), (build_area.offset.x + x, self.blueprint.height_map[x,z]+10, build_area.offset.z + z), Block("air"))
        """
    
    def execute_wall_placement(self):
        editor = self.blueprint.map_features.editor
        build_area = self.blueprint.map_features.build_area
        wall_coords = []
        for x,z in np.argwhere(self.blueprint.city_walls):
            directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
            neighborhood = np.zeros((3,3), dtype=int)
            for i,j in directions:
                if 0 <= x+i < self.blueprint.city_walls.shape[0] and 0 <= z+j < self.blueprint.city_walls.shape[1]:
                    neighborhood[i+1,j+1] = self.blueprint.outside_walls_area[x+i, z+j]
            
            placeCuboid(editor, (build_area.offset.x + x, self.blueprint.height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, self.blueprint.height_map[x,z]+6, build_area.offset.z + z), Block("stone_bricks"))
            if (neighborhood == 0).all():
                editor.placeBlockGlobal((build_area.offset.x + x, self.blueprint.height_map[x,z]+7, build_area.offset.z + z), Block("oak_planks"))
            else:
                placeCuboid(editor, (build_area.offset.x + x, self.blueprint.height_map[x,z]+7, build_area.offset.z + z), (build_area.offset.x + x, self.blueprint.height_map[x,z]+8, build_area.offset.z + z), Block("stone_bricks"))

    
    def connect_coordinates_in_order(self, coordinates, n_mask: np.ndarray):
        if not coordinates:
            return []

        full_tour = [coordinates[0]]

        for i in range(len(coordinates) - 1):
            start_node = coordinates[i]
            end_node = coordinates[i+1]

            path_segment = BFS.find_minimal_path_to_network_numeric(n_mask, [start_node], [end_node], use_start=True)
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