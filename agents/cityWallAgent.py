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
                 deactivation_step,
                 priority, 
                 max_slope,
                 max_plots,
                 road_connector_agent: RoadConnectorAgent,
                 number_of_gates):
        super().__init__(blueprint)

        self.activation_step = activation_step
        self.deactivation_step = deactivation_step
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
                    if self.blueprint.ground_water_map[coord[0]+x_step,coord[1]+z_step] != 255 or self.blueprint.lava_map[coord[0]+x_step,coord[1]+z_step] != 255:
                        continue
                    area.append([coord[0]+x_step, coord[1]+z_step])

        area = np.array(area)
        hull = ConvexHull(area)


        penalty = np.vectorize(self.penalty)
        exp_penalty = np.vectorize(self.blueprint.exp_penalty)
        n_build_map = exp_penalty(self.blueprint.steepness_map) + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(self.blueprint.lava_map != 255).astype(int) + penalty(np.logical_and(self.blueprint.map > 35, self.blueprint.map != 200)).astype(int)
        n_traversable = n_build_map

        walls = self.connect_coordinates_in_order([tuple(area[vertex]) for vertex in hull.vertices], n_traversable)
        last_segment = self.connect_coordinates_in_order([tuple(area[hull.vertices[-1]]), tuple(area[hull.vertices[0]])], n_traversable)
        
        if walls != None and last_segment != None:
            walls.extend(last_segment)
            wall_coordinates = self.construct_wall(walls)
            self.place(wall_coordinates)
            road_segments = []
            split = int((len(walls)-1)/self.number_of_gates)
            for i, w in enumerate(walls):
                if i % split == 0:
                    new_road_segments = self.road_connector_agent.construct_road([w], ignore_walls=True)
                    road_segments.append(new_road_segments)
                    self.road_connector_agent.place(new_road_segments)
                    penalty = np.vectorize(self.penalty)
                    traversable = exp_penalty(self.blueprint.steepness_map) + penalty(self.blueprint.ground_water_map != 255).astype(int) + penalty(self.blueprint.lava_map != 255).astype(int) + penalty(np.logical_and(self.blueprint.map > 1, self.blueprint.map != 200)).astype(int) + penalty(self.blueprint.deactivate_border_region(self.blueprint.map)) + penalty(self.blueprint.outside_walls_area)
                    rn_copy = np.ones_like(self.blueprint.road_network, dtype=bool)
                    for s in road_segments:
                        for c in s:
                            rn_copy[c] = False
                    path = BFS.find_minimal_path_to_network_numeric(traversable, [w], [tuple(x) for x in np.argwhere(self.blueprint.road_network & rn_copy)])
                    if path is None:
                        continue
                    self.road_connector_agent.connect_to_road_network(path, True)
            # self.blueprint.show()
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
                if 0 <= neighbor_x < self.blueprint.map.shape[0] and 0 <= neighbor_y < self.blueprint.map.shape[1] and self.blueprint.map[neighbor_x, neighbor_y] <= 35:
                    wall_coordinates.add((neighbor_x, neighbor_y))

        return list(wall_coordinates)
    
    def execute_wall_placement(self):
        editor = self.blueprint.map_features.editor
        build_area = self.blueprint.map_features.build_area
        built_wall = np.zeros(self.blueprint.city_walls.shape, dtype=int)
        directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        wall_blocks = 6*[Block("stone_bricks")]+2*[Block("stone")]+ [Block("mossy_stone_bricks"), Block("cracked_stone_bricks"), Block("cobblestone")]
        for x,z in np.argwhere(self.blueprint.city_walls):
            
            neighborhood = np.zeros((3,3), dtype=int)
            for i,j in directions:
                if 0 <= x+i < self.blueprint.city_walls.shape[0] and 0 <= z+j < self.blueprint.city_walls.shape[1]:
                    neighborhood[i+1,j+1] = self.blueprint.outside_walls_area[x+i, z+j]
                else: 
                 neighborhood[i+1,j+1] = 1
            if not (neighborhood == 0).all():
                placeCuboid(editor, (build_area.offset.x + x, self.blueprint.height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, self.blueprint.height_map[x,z]+8, build_area.offset.z + z), wall_blocks)
                built_wall[x,z] = self.blueprint.height_map[x,z]+8
        for k in range(3):
            indices_built = {}
            for x,z in np.argwhere(self.blueprint.city_walls != built_wall.astype(bool)):
                neighborhood = np.zeros((3,3), dtype=int)
                for i,j in directions:
                    if built_wall[x+i,z+j]:
                        editor.placeBlock((build_area.offset.x + x, built_wall[x+i,z+j]-1, build_area.offset.z + z), Block("oak_planks"))
                        if k == 0:
                            match (i,j):
                                case (0,-1):
                                    block = Block("stone_brick_stairs",{"facing": "north", "half": "top"})
                                case (-1,0):
                                    block = Block("stone_brick_stairs",{"facing": "west", "half": "top"})
                                case (1,0):
                                    block = Block("stone_brick_stairs",{"facing": "east", "half": "top"})
                                case (0,1):
                                    block = Block("stone_brick_stairs",{"facing": "south", "half": "top"})
                            editor.placeBlock((build_area.offset.x + x, built_wall[x+i,z+j]-2, build_area.offset.z + z), block)
                        indices_built[(x,z)] = built_wall[x+i,z+j]
                        break
            for k,v in indices_built.items():
                built_wall[k] = v
        
        for x,z in np.argwhere(self.blueprint.city_walls & self.blueprint.road_network):
            placeCuboid(editor, (build_area.offset.x + x, self.blueprint.height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, self.blueprint.height_map[x,z]+3, build_area.offset.z + z), Block("air"))
    
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