# Directions: North = 0, East = 1, Bottom = 2, South = 3, West = 4, Top = 5
# Rotations Facing:  North = 0, East = 1, South = 2, West = 3, Don't Care = 4 
from ...tile import create_tile_direction_dict
from ...tile import ROT_NORTH, ROT_EAST, ROT_SOUTH, ROT_WEST, ROT_ANY
from ...tile import ROT_CNR_NE, ROT_CNR_SE, ROT_CNR_SW, ROT_CNR_NW
from ...tile import DIR_NORTH, DIR_EAST, DIR_TOP, DIR_SOUTH, DIR_WEST, DIR_BOTTOM
from pyglm.glm import ivec3

TILE_SIZE = ivec3(3,4,3)

tile_quantity_limits = {("House_Wood_GF_Corner",ROT_CNR_NE): 1,
                        ("House_Wood_GF_Corner",ROT_CNR_SE): 1,
                        ("House_Wood_GF_Corner",ROT_CNR_SW): 1,
                        ("House_Wood_GF_Corner",ROT_CNR_NW): 1}

tile_directions_zero = {    "House_Wood_Ceiling":           {   DIR_NORTH: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH), ("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH), ("House_Wood_Ceiling",4), ("House_Wood_Stairs",ROT_NORTH)],
                                                                DIR_EAST: [("House_Wood_GF_Wall",ROT_EAST),("House_Wood_GF_Window",ROT_EAST), ("House_Wood_UF_Wall",ROT_EAST),("House_Wood_UF_Window",ROT_EAST), ("House_Wood_Ceiling",4), ("House_Wood_Stairs",ROT_NORTH)],
                                                                DIR_TOP: [("House_Wood_Ceiling",ROT_ANY)],
                                                                DIR_SOUTH: [("House_Wood_GF_Wall",ROT_SOUTH),("House_Wood_GF_Window",ROT_SOUTH), ("House_Wood_UF_Wall",ROT_SOUTH),("House_Wood_UF_Window",ROT_SOUTH), ("House_Wood_Ceiling",ROT_ANY), ("House_Wood_Stairs",ROT_NORTH)],
                                                                DIR_WEST: [("House_Wood_GF_Wall",ROT_WEST),("House_Wood_GF_Window",ROT_WEST), ("House_Wood_UF_Wall",ROT_WEST),("House_Wood_UF_Window",ROT_WEST), ("House_Wood_Ceiling",ROT_ANY), ("House_Wood_Stairs",ROT_NORTH)],
                                                                DIR_BOTTOM: [("House_Wood_Ceiling",ROT_ANY)]},
                            "House_Wood_Stairs":            {   DIR_NORTH: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH), ("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH), ("House_Wood_Ceiling",ROT_ANY)],
                                                                DIR_EAST: [("House_Wood_GF_Wall",ROT_EAST),("House_Wood_GF_Window",ROT_EAST), ("House_Wood_UF_Wall",ROT_EAST),("House_Wood_UF_Window",ROT_EAST), ("House_Wood_Ceiling",ROT_ANY)],
                                                                DIR_TOP: [("House_Wood_Stairs",ROT_NORTH)],
                                                                DIR_SOUTH: [("House_Wood_GF_Wall",ROT_SOUTH),("House_Wood_GF_Window",ROT_SOUTH), ("House_Wood_UF_Wall",ROT_SOUTH),("House_Wood_UF_Window",ROT_SOUTH), ("House_Wood_Ceiling",ROT_ANY)],
                                                                DIR_WEST: [("House_Wood_GF_Wall",ROT_WEST),("House_Wood_GF_Window",ROT_WEST), ("House_Wood_UF_Wall",ROT_WEST),("House_Wood_UF_Window",ROT_WEST), ("House_Wood_Ceiling",ROT_ANY)],
                                                                DIR_BOTTOM: [("House_Wood_Stairs",ROT_NORTH)]},
                            "House_Wood_GF_Wall":           {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NE)],
                                                                DIR_TOP: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH)],
                                                                DIR_SOUTH: [("House_Wood_Ceiling",ROT_ANY), ("House_Wood_Stairs",ROT_NORTH),("House_Wood_GF_Wall",ROT_SOUTH),("House_Wood_GF_Window",ROT_SOUTH)],
                                                                DIR_WEST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: []},                    
                            "House_Wood_GF_Door":           {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NE)],
                                                                DIR_TOP: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH)],
                                                                DIR_SOUTH: [("House_Wood_Ceiling",ROT_ANY),("House_Wood_GF_Wall",ROT_SOUTH),("House_Wood_GF_Window",ROT_SOUTH)],
                                                                DIR_WEST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: []},
                            "House_Wood_GF_Window":         {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NE)],
                                                                DIR_TOP: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH)],
                                                                DIR_SOUTH: [("House_Wood_Ceiling",ROT_ANY), ("House_Wood_Stairs",ROT_NORTH),("House_Wood_GF_Wall",ROT_SOUTH),("House_Wood_GF_Window",ROT_SOUTH)],
                                                                DIR_WEST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: []},
                            "House_Wood_GF_Corner":         {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [("House_Wood_UF_Corner",ROT_CNR_NE)],
                                                                DIR_SOUTH: [("House_Wood_GF_Wall",ROT_EAST),("House_Wood_GF_Window",ROT_EAST),("House_Wood_GF_Corner",ROT_CNR_SE)],
                                                                DIR_WEST: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: []},
                            "House_Wood_UF_Wall":           {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH),("House_Wood_UF_Corner",ROT_CNR_NE)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("House_Wood_Ceiling",ROT_ANY), ("House_Wood_Stairs",ROT_NORTH),("House_Wood_UF_Wall",ROT_SOUTH),("House_Wood_UF_Window",ROT_SOUTH)],
                                                                DIR_WEST: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH),("House_Wood_UF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH)]},                    
                            "House_Wood_UF_Window":         {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH),("House_Wood_UF_Corner",ROT_CNR_NE)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("House_Wood_Ceiling",ROT_ANY), ("House_Wood_Stairs",ROT_NORTH),("House_Wood_UF_Wall",ROT_SOUTH),("House_Wood_UF_Window",ROT_SOUTH)],
                                                                DIR_WEST: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH),("House_Wood_UF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: [("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH)]},
                            "House_Wood_UF_Corner":         {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("House_Wood_UF_Wall",ROT_EAST),("House_Wood_UF_Window",ROT_EAST),("House_Wood_UF_Corner",ROT_CNR_SE)],
                                                                DIR_WEST: [("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH),("House_Wood_UF_Corner",ROT_CNR_NW)],
                                                                DIR_BOTTOM: [("House_Wood_GF_Corner",ROT_CNR_NE)]},
                            "Air":                          {   DIR_NORTH: [("Air",ROT_ANY), ("House_Wood_GF_Wall",ROT_SOUTH),("House_Wood_GF_Window",ROT_SOUTH),("House_Wood_GF_Corner",ROT_CNR_SE),("House_Wood_GF_Corner",ROT_CNR_SW),("House_Wood_UF_Wall",ROT_SOUTH),("House_Wood_UF_Window",ROT_SOUTH),("House_Wood_UF_Corner",ROT_CNR_SE),("House_Wood_UF_Corner",ROT_CNR_SW)],
                                                                DIR_EAST: [("Air",ROT_ANY), ("House_Wood_GF_Wall",ROT_WEST),("House_Wood_GF_Window",ROT_WEST),("House_Wood_GF_Corner",ROT_CNR_SW),("House_Wood_GF_Corner",ROT_CNR_NW),("House_Wood_UF_Wall",ROT_WEST),("House_Wood_UF_Window",ROT_WEST),("House_Wood_UF_Corner",ROT_CNR_SW),("House_Wood_UF_Corner",ROT_CNR_NW)],
                                                                DIR_TOP: [("Air",ROT_ANY)],
                                                                DIR_SOUTH: [("Air",ROT_ANY), ("House_Wood_GF_Wall",ROT_NORTH),("House_Wood_GF_Window",ROT_NORTH),("House_Wood_GF_Corner",ROT_CNR_NE),("House_Wood_GF_Corner",ROT_CNR_NW),("House_Wood_UF_Wall",ROT_NORTH),("House_Wood_UF_Window",ROT_NORTH),("House_Wood_UF_Corner",ROT_CNR_NE),("House_Wood_UF_Corner",ROT_CNR_NW)],
                                                                DIR_WEST: [("Air",ROT_ANY), ("House_Wood_GF_Wall",ROT_EAST),("House_Wood_GF_Window",ROT_EAST),("House_Wood_GF_Corner",ROT_CNR_NE),("House_Wood_GF_Corner",ROT_CNR_SE),("House_Wood_UF_Wall",ROT_EAST),("House_Wood_UF_Window",ROT_EAST),("House_Wood_UF_Corner",ROT_CNR_NE),("House_Wood_UF_Corner",ROT_CNR_SE)],
                                                                DIR_BOTTOM: [("Air",ROT_ANY)]}}

tiles_borders_rotation_invariant = ["Air", "House_Wood_Ceiling"]

tile_directions = {}
for name, rot_zero_dict in tile_directions_zero.items():
    if name in tiles_borders_rotation_invariant:
        tile_directions.update({(name, ROT_ANY): rot_zero_dict})
    else:
        tile_directions.update(create_tile_direction_dict(name, rot_zero_dict))

tile_weights = {    "House_Wood_Ceiling": 10,
                    "House_Wood_Stairs": 5,
                    "House_Wood_GF_Wall": 20,
                    "House_Wood_GF_Door": 1,
                    "House_Wood_GF_Window": 10,
                    "House_Wood_GF_Corner": 1,
                    "House_Wood_UF_Wall": 20,
                    "House_Wood_UF_Window": 10,
                    "House_Wood_UF_Corner": 1,
                    "Air": 1}

variation_weights = {   "House_Wood_Ceiling": {"House_Wood_Ceiling#0": 6, "House_Wood_Ceiling#1": 2, "House_Wood_Ceiling#2": 1, "House_Wood_Ceiling#3": 2},
                        "House_Wood_GF_Wall" : {"House_Wood_GF_Wall#0": 5, "House_Wood_GF_Wall#1": 1, "House_Wood_GF_Wall#2": 2, "House_Wood_GF_Wall#3": 2, "House_Wood_GF_Wall#4": 2},
                        "House_Wood_GF_Window" : {"House_Wood_GF_Window#0": 5, "House_Wood_GF_Window#1": 1, "House_Wood_GF_Window#2": 2, "House_Wood_GF_Window#3": 2, "House_Wood_GF_Window#4": 2},
                        "House_Wood_UF_Wall" : {"House_Wood_UF_Wall#0": 5, "House_Wood_UF_Wall#1": 2, "House_Wood_UF_Wall#2": 2, "House_Wood_UF_Wall#3": 2, "House_Wood_UF_Wall#4": 2, "House_Wood_UF_Wall#5": 5, "House_Wood_UF_Wall#6": 2, "House_Wood_UF_Wall#7": 2, "House_Wood_UF_Wall#8": 2, "House_Wood_UF_Wall#9": 2,},
                        "House_Wood_UF_Window" : {"House_Wood_UF_Window#0": 5, "House_Wood_UF_Window#2": 2, "House_Wood_UF_Window#3": 2, "House_Wood_UF_Window#4": 2},
                        "House_Wood_UF_Corner": {"House_Wood_UF_Corner#0": 5, "House_Wood_UF_Corner#1": 2, "House_Wood_UF_Corner#2": 2, "House_Wood_UF_Corner#3": 2, "House_Wood_UF_Corner#4": 2}}


tiles_possible_all = [  ("House_Wood_Ceiling", ROT_ANY),
                        ("House_Wood_Stairs", ROT_NORTH),
                        ("House_Wood_GF_Wall", ROT_NORTH), ("House_Wood_GF_Wall", ROT_EAST), ("House_Wood_GF_Wall", ROT_SOUTH), ("House_Wood_GF_Wall", ROT_WEST),
                        ("House_Wood_GF_Door", ROT_NORTH), ("House_Wood_GF_Door", ROT_EAST), ("House_Wood_GF_Door", ROT_SOUTH), ("House_Wood_GF_Door", ROT_WEST),
                        ("House_Wood_GF_Window", ROT_NORTH), ("House_Wood_GF_Window", ROT_EAST), ("House_Wood_GF_Window", ROT_SOUTH), ("House_Wood_GF_Window", ROT_WEST),
                        ("House_Wood_GF_Corner", ROT_CNR_NE), ("House_Wood_GF_Corner", ROT_CNR_SE), ("House_Wood_GF_Corner", ROT_CNR_SW), ("House_Wood_GF_Corner", ROT_CNR_NW),
                        ("House_Wood_UF_Wall", ROT_NORTH), ("House_Wood_UF_Wall", ROT_EAST), ("House_Wood_UF_Wall", ROT_SOUTH), ("House_Wood_UF_Wall", ROT_WEST),
                        ("House_Wood_UF_Window", ROT_NORTH), ("House_Wood_UF_Window", ROT_EAST), ("House_Wood_UF_Window", ROT_SOUTH), ("House_Wood_UF_Window", ROT_WEST),
                        ("House_Wood_UF_Corner", ROT_CNR_NE), ("House_Wood_UF_Corner", ROT_CNR_SE), ("House_Wood_UF_Corner", ROT_CNR_SW), ("House_Wood_UF_Corner", ROT_CNR_NW),
                        ("Air", ROT_ANY)]

tiles_possible_inner = [("House_Wood_Ceiling", ROT_ANY),
                        ("House_Wood_Stairs", ROT_NORTH),
                        ("House_Wood_UF_Wall", ROT_NORTH), ("House_Wood_UF_Wall", ROT_EAST), ("House_Wood_UF_Wall", ROT_SOUTH), ("House_Wood_UF_Wall", ROT_WEST),
                        ("House_Wood_UF_Window", ROT_NORTH), ("House_Wood_UF_Window", ROT_EAST), ("House_Wood_UF_Window", ROT_SOUTH), ("House_Wood_UF_Window", ROT_WEST),
                        ("House_Wood_UF_Corner", ROT_CNR_NE), ("House_Wood_UF_Corner", ROT_CNR_SE), ("House_Wood_UF_Corner", ROT_CNR_SW), ("House_Wood_UF_Corner", ROT_CNR_NW),
                        ("Air", ROT_ANY)]

tiles_possible_edge_north = [   ("House_Wood_GF_Wall", ROT_NORTH),  
                                ("House_Wood_GF_Window", ROT_NORTH),
                                ("House_Wood_GF_Door", ROT_NORTH), 
                                ("House_Wood_GF_Corner", ROT_CNR_NE),
                                ("House_Wood_GF_Corner", ROT_CNR_NW),
                                ("House_Wood_UF_Wall", ROT_NORTH),  
                                ("House_Wood_UF_Window", ROT_NORTH),
                                ("House_Wood_UF_Corner", ROT_CNR_NE),
                                ("House_Wood_UF_Corner", ROT_CNR_NW),
                                ("Air", ROT_ANY)]

tiles_possible_edge_east =  [   ("House_Wood_GF_Wall", ROT_EAST),  
                                ("House_Wood_GF_Window", ROT_EAST),
                                ("House_Wood_GF_Door", ROT_EAST), 
                                ("House_Wood_GF_Corner", ROT_CNR_NE), 
                                ("House_Wood_GF_Corner", ROT_CNR_SE),
                                ("House_Wood_UF_Wall", ROT_EAST),  
                                ("House_Wood_UF_Window", ROT_EAST), 
                                ("House_Wood_UF_Corner", ROT_CNR_NE), 
                                ("House_Wood_UF_Corner", ROT_CNR_SE),
                                ("Air", ROT_ANY)]

tiles_possible_edge_top = [ ("House_Wood_Ceiling", ROT_ANY),
                            ("House_Wood_Stairs", ROT_NORTH),
                            ("House_Wood_UF_Wall", ROT_NORTH), ("House_Wood_UF_Wall", ROT_EAST), ("House_Wood_UF_Wall", ROT_SOUTH), ("House_Wood_UF_Wall", ROT_WEST),
                            ("House_Wood_UF_Window", ROT_NORTH), ("House_Wood_UF_Window", ROT_EAST), ("House_Wood_UF_Window", ROT_SOUTH), ("House_Wood_UF_Window", ROT_WEST),
                            ("House_Wood_UF_Corner", ROT_CNR_NE), ("House_Wood_UF_Corner", ROT_CNR_SE), ("House_Wood_UF_Corner", ROT_CNR_SW), ("House_Wood_UF_Corner", ROT_CNR_NW),
                            ("Air", ROT_ANY)]

tiles_possible_edge_south = [   ("House_Wood_GF_Wall", ROT_SOUTH),  
                                ("House_Wood_GF_Window", ROT_SOUTH),
                                ("House_Wood_GF_Door", ROT_SOUTH), 
                                ("House_Wood_GF_Corner", ROT_CNR_SE), 
                                ("House_Wood_GF_Corner", ROT_CNR_SW),
                                ("House_Wood_UF_Wall", ROT_SOUTH),  
                                ("House_Wood_UF_Window", ROT_SOUTH), 
                                ("House_Wood_UF_Corner", ROT_CNR_SE), 
                                ("House_Wood_UF_Corner", ROT_CNR_SW),
                                ("Air", ROT_ANY)]

tiles_possible_edge_west =  [   ("House_Wood_GF_Wall", ROT_WEST),  
                                ("House_Wood_GF_Window", ROT_WEST),
                                ("House_Wood_GF_Door", ROT_WEST), 
                                ("House_Wood_GF_Corner", ROT_CNR_SW), 
                                ("House_Wood_GF_Corner", ROT_CNR_NW),
                                ("House_Wood_UF_Wall", ROT_WEST),  
                                ("House_Wood_UF_Window", ROT_WEST),
                                ("House_Wood_UF_Corner", ROT_CNR_SW), 
                                ("House_Wood_UF_Corner", ROT_CNR_NW),
                                ("Air", ROT_ANY)]

tiles_possible_edge_bottom = [  ("House_Wood_Ceiling", ROT_ANY),
                                ("House_Wood_Stairs", ROT_NORTH),
                                ("House_Wood_GF_Wall", ROT_NORTH), ("House_Wood_GF_Wall", ROT_EAST), ("House_Wood_GF_Wall", ROT_SOUTH), ("House_Wood_GF_Wall", ROT_WEST),
                                ("House_Wood_GF_Door", ROT_NORTH), ("House_Wood_GF_Door", ROT_EAST), ("House_Wood_GF_Door", ROT_SOUTH), ("House_Wood_GF_Door", ROT_WEST),
                                ("House_Wood_GF_Window", ROT_NORTH), ("House_Wood_GF_Window", ROT_EAST), ("House_Wood_GF_Window", ROT_SOUTH), ("House_Wood_GF_Window", ROT_WEST),
                                ("House_Wood_GF_Corner", ROT_CNR_NE), ("House_Wood_GF_Corner", ROT_CNR_SE), ("House_Wood_GF_Corner", ROT_CNR_SW), ("House_Wood_GF_Corner", ROT_CNR_NW),
                                ("Air", ROT_ANY)]


tile_rules = [  tiles_possible_all,
                tiles_possible_inner,
                tiles_possible_edge_north,
                tiles_possible_edge_east,
                tiles_possible_edge_top,
                tiles_possible_edge_south,
                tiles_possible_edge_west,
                tiles_possible_edge_bottom]
