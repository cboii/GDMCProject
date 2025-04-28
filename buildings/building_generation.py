from gdpc import Editor
from gdpc.vector_tools import Box
from pyglm.glm import ivec3
import numpy as np
import numpy.typing as npt
from tile import *

TILE_SIZE = ivec3(3,4,3)

TILES_ALL = 0
TILES_INNER = 1
TILES_NORTH = 2
TILES_EAST = 3
TILES_TOP = 4
TILES_SOUTH = 5
TILES_WEST = 6
TILES_BOTTOM = 7

def create_tile_array(area: Box, tile_rules: list, tile_directions: dict):
    tile_array_size = area.size // TILE_SIZE
    tile_array = np.array([[[Tile((x,y,z), 
                                  (area.offset.x + TILE_SIZE.x * x, 
                                   area.offset.y + TILE_SIZE.y * y, 
                                   area.offset.z + TILE_SIZE.z * z))
                                   for z in range(tile_array_size.z)] 
                                   for y in range(tile_array_size.y)] 
                                   for x in range(tile_array_size.x)], dtype=Tile)
    
    for x in range(tile_array_size.x):
        for y in range(tile_array_size.y):
            for z in range(tile_array_size.z):
                
                inner = True
                building_modules_for_tile = set(tile_rules[TILES_ALL])
                if x == 0: 
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_WEST])
                    inner = False
                elif x == tile_array_size.x-1: 
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_EAST])
                    inner = False
                
                if y == 0: 
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_BOTTOM])
                elif y == tile_array_size.y-1: 
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_TOP])
                
                if z == 0: 
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_NORTH])
                    inner = False
                elif z == tile_array_size.z-1: 
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_SOUTH])
                    inner = False
                
                if inner:
                    building_modules_for_tile = building_modules_for_tile.intersection(tile_rules[TILES_INNER])
                
                tile_array[x,y,z].add_possible_modules({module: tile_directions[module] for module in list(building_modules_for_tile)})

                if x > 0: tile_array[x,y,z].set_neighbor(WEST, tile_array[x-1,y,z])
                if x < tile_array_size.x-1: tile_array[x,y,z].set_neighbor(EAST, tile_array[x+1,y,z])
                if y > 0: tile_array[x,y,z].set_neighbor(BOTTOM, tile_array[x,y-1,z])
                if y < tile_array_size.y-1: tile_array[x,y,z].set_neighbor(TOP, tile_array[x,y+1,z])
                if z > 0: tile_array[x,y,z].set_neighbor(NORTH, tile_array[x,y,z-1])
                if z < tile_array_size.z-1: tile_array[x,y,z].set_neighbor(SOUTH, tile_array[x,y,z+1])

    return tile_array
    


def wave_function_collapse(tile_array: npt.NDArray[any],
                           tile_weights: list,
                           first_tile_grid_pos: ivec3 = None, 
                           first_tile_module: str = None):
    first_tile = tile_array[first_tile_grid_pos.x,first_tile_grid_pos.y,first_tile_grid_pos.z]
    
    assert first_tile_module in first_tile.possible_modules, "Module not possible for this tile"
    first_tile.set_possible_modules({first_tile_module: first_tile.possible_modules[first_tile_module]})
    first_tile.select(tile_weights)
    for i in range(tile_array.size-1):
        print()
        print()
        print()
        entropies = []
        for tile in tile_array.flat:
            entropy = 256
            for nb in tile.neighbors.values():
                if nb.entropy == 0 and tile.entropy != 0:
                    entropy = tile.entropy
            entropies.append(entropy)
            tile.updated = False

        x,y,z = np.unravel_index(np.array(np.argmin(entropies)), tile_array.shape)
        print(f"SELECTING TILE ({x},{y},{z}).")
        tile_array[x,y,z].select(tile_weights)
    return tile_array


from buildingModules.houseGroundFloorWood.tile_rules import tile_rules, tile_directions, tile_weights, variation_weights

editor = Editor()
print("Start Tile Array")
tile_array = create_tile_array(editor.getBuildArea(), tile_rules, tile_directions)
print("Start WFC")
tile_array = wave_function_collapse(tile_array, tile_weights, ivec3(1,0,0), ("HouseGroundFloorWood_Door",0))
for x in range(len(tile_array)):
    for y in range(len(tile_array[0])):
        for z in range(len(tile_array[0,0])):
            print(f"Pos: {tile_array[x,y,z].grid_pos}, Module: {tile_array[x,y,z].selected_module}")
            tile_array[x,y,z].build(editor,variation_weights)
    
    
    
