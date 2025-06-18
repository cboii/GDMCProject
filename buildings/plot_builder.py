from gdpc import Editor
from gdpc.vector_tools import Box
from pyglm.glm import ivec3
import numpy as np
import numpy.typing as npt
from .tile import Tile
from .tile import DIR_NORTH, DIR_EAST, DIR_TOP, DIR_SOUTH, DIR_WEST, DIR_BOTTOM

TILES_ALL = 0
TILES_INNER = 1
TILES_NORTH = 2
TILES_EAST = 3
TILES_TOP = 4
TILES_SOUTH = 5
TILES_WEST = 6
TILES_BOTTOM = 7

class PlotBuilder:
     
    def __init__(self, area: Box, floors: int, tile_size: ivec3, tile_rules: list, tile_directions: dict, 
                  tile_quantity_limits: dict, tile_weights: list):
        self.area = area
        self.floors = floors
        self.tile_size = tile_size
        self.tile_rules = tile_rules
        self.tile_directions = tile_directions
        self.tile_quantity_limits = tile_quantity_limits.copy()
        self.tile_weights = tile_weights

        self.tile_array = None
         

    def create_tile_array(self):
        tile_array_size = ivec3(self.area.size.x // self.tile_size.x, self.floors, self.area.size.z // self.tile_size.z)
        tile_array_offset_x = (self.area.size.x - (tile_array_size.x * self.tile_size.x)) // 2
        tile_array_offset_z = (self.area.size.z - (tile_array_size.z * self.tile_size.z)) // 2
        tile_array = np.array([[[Tile((x,y,z), 
                                    (self.area.offset.x + tile_array_offset_x + self.tile_size.x * x, 
                                    self.area.offset.y + self.tile_size.y * y, 
                                    self.area.offset.z + tile_array_offset_z + self.tile_size.z * z), self.tile_size)
                                    for z in range(tile_array_size.z)] 
                                    for y in range(tile_array_size.y)] 
                                    for x in range(tile_array_size.x)], dtype=Tile)
        
        for x in range(tile_array_size.x):
            for y in range(tile_array_size.y):
                for z in range(tile_array_size.z):
                    
                    inner = True
                    building_modules_for_tile = set(self.tile_rules[TILES_ALL])
                    if x == 0: 
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_WEST])
                        inner = False
                    elif x == tile_array_size.x-1: 
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_EAST])
                        inner = False
                    
                    if y == 0: 
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_BOTTOM])
                        inner = False
                    elif y == tile_array_size.y-1: 
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_TOP])
                        inner = False
                    
                    if z == 0: 
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_NORTH])
                        inner = False
                    elif z == tile_array_size.z-1: 
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_SOUTH])
                        inner = False
                    
                    if inner:
                        building_modules_for_tile = building_modules_for_tile.intersection(self.tile_rules[TILES_INNER])
                    
                    tile_array[x,y,z].add_possible_modules({module: self.tile_directions[module] for module in list(building_modules_for_tile)})

                    if x > 0: tile_array[x,y,z].set_neighbor(DIR_WEST, tile_array[x-1,y,z])
                    if x < tile_array_size.x-1: tile_array[x,y,z].set_neighbor(DIR_EAST, tile_array[x+1,y,z])
                    if y > 0: tile_array[x,y,z].set_neighbor(DIR_BOTTOM, tile_array[x,y-1,z])
                    if y < tile_array_size.y-1: tile_array[x,y,z].set_neighbor(DIR_TOP, tile_array[x,y+1,z])
                    if z > 0: tile_array[x,y,z].set_neighbor(DIR_NORTH, tile_array[x,y,z-1])
                    if z < tile_array_size.z-1: tile_array[x,y,z].set_neighbor(DIR_SOUTH, tile_array[x,y,z+1])

        self.tile_array = tile_array
    


    def wfc(self, first_tile_grid_pos: ivec3 = None, first_tile_module: str = None):
        first_tile_grid_pos = ivec3(first_tile_grid_pos)
        first_tile = self.tile_array[first_tile_grid_pos.x,first_tile_grid_pos.y,first_tile_grid_pos.z]
        
        assert first_tile_module in first_tile.possible_modules, "Module not possible for this tile"
        first_tile.set_possible_modules({first_tile_module: first_tile.possible_modules[first_tile_module]})
        first_tile.select(self.tile_quantity_limits, self.tile_weights)
        for i in range(self.tile_array.size-1):
            entropies = []
            for tile in self.tile_array.flat:
                entropy = 256
                for nb in tile.neighbors.values():
                    if nb.entropy == 0 and tile.entropy != 0:
                        entropy = tile.entropy
                entropies.append(entropy)
                tile.updated = False

            x,y,z = np.unravel_index(np.array(np.argmin(entropies)), self.tile_array.shape)
            self.tile_array[x,y,z].select(self.tile_quantity_limits,self.tile_weights)
        return self.tile_array
    
    def build(self, editor: Editor, variation_weights: dict, wood_type: str ="oak"):
        for x in range(len(self.tile_array)):
            for y in range(len(self.tile_array[0])):
                for z in range(len(self.tile_array[0,0])):
                    #print(f"Grid Pos: {tuple(self.tile_array[x,y,z].grid_pos)}, World Pos: {tuple(self.tile_array[x,y,z].pos)}, Module: {self.tile_array[x,y,z].selected_module}")
                    self.tile_array[x,y,z].build(editor,variation_weights,wood_type)

    
    
    
