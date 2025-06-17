# Directions: North = 0, East = 1, Top = 2, South = 3, West = 4, Bottom = 5
# Rotations Facing:  North = 0, East = 1, South = 2, West = 3, Don't Care = 4 
from ...tile import create_tile_direction_dict
from ...tile import ROT_NORTH, ROT_EAST, ROT_SOUTH, ROT_WEST, ROT_ANY

from ...tile import DIR_NORTH, DIR_EAST, DIR_TOP, DIR_SOUTH, DIR_WEST, DIR_BOTTOM
from pyglm.glm import ivec3

TILE_SIZE = ivec3(11,20,7)

tile_quantity_limits = {}

tile_directions_zero = {    "Townhall_Front_Left":          {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Townhall_Middle_Left", ROT_NORTH)],
                                                                DIR_WEST: [("Townhall_Front_Right", ROT_NORTH)],
                                                                DIR_BOTTOM: []},
                            "Townhall_Front_Right":         {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("Townhall_Front_Left", ROT_NORTH)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Townhall_Middle_Right", ROT_NORTH)],
                                                                DIR_WEST: [("Air",ROT_ANY)],
                                                                DIR_BOTTOM: []},
                            "Townhall_Middle_Left":         {   DIR_NORTH: [("Townhall_Front_Left", ROT_NORTH), ("Townhall_Middle_Left", ROT_NORTH)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Townhall_Middle_Left", ROT_NORTH), ("Townhall_End_Left", ROT_NORTH)],
                                                                DIR_WEST: [("Townhall_Middle_Right", ROT_NORTH)],
                                                                DIR_BOTTOM: []},
                            "Townhall_Middle_Right":        {   DIR_NORTH: [("Townhall_Front_Right", ROT_NORTH), ("Townhall_Middle_Right", ROT_NORTH)],
                                                                DIR_EAST: [("Townhall_Middle_Left", ROT_NORTH)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Townhall_Middle_Right", ROT_NORTH), ("Townhall_End_Right", ROT_NORTH)],
                                                                DIR_WEST: [("Air",ROT_ANY)],
                                                                DIR_BOTTOM: []},
                            "Townhall_End_Left":            {   DIR_NORTH: [("Townhall_Middle_Left", ROT_NORTH)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Air",ROT_ANY)],
                                                                DIR_WEST: [("Townhall_End_Right", ROT_NORTH)],
                                                                DIR_BOTTOM: []},
                            "Townhall_End_Right":           {   DIR_NORTH: [("Townhall_Middle_Right", ROT_NORTH)],
                                                                DIR_EAST: [("Townhall_End_Left", ROT_NORTH)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Air",ROT_ANY)],
                                                                DIR_WEST: [("Air",ROT_ANY)],
                                                                DIR_BOTTOM: []},
                            "Air":                          {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Air",ROT_ANY)],
                                                                DIR_WEST: [("Air",ROT_ANY)],
                                                                DIR_BOTTOM: []}}

tiles_borders_rotation_invariant = ["Air"]

tile_directions = {}
for name, rot_zero_dict in tile_directions_zero.items():
    if name in tiles_borders_rotation_invariant:
        tile_directions.update({(name, ROT_ANY): rot_zero_dict})
    else:
        tile_directions.update(create_tile_direction_dict(name, rot_zero_dict))

tile_weights = {    "Townhall_Front_Left": 1,
                    "Townhall_Front_Right": 1,
                    "Townhall_Middle_Left": 50,
                    "Townhall_Middle_Right": 50,
                    "Townhall_End_Left" : 0.1,
                    "Townhall_End_Right" : 0.1,
                    "Air": 1}

variation_weights = {"Townhall_Middle_Left": {"Townhall_Middle_Left#0": 1, "Townhall_Middle_Left#1": 1, "Townhall_Middle_Left#2": 1},
                     "Townhall_Middle_Right": {"Townhall_Middle_Right#0": 1, "Townhall_Middle_Right#1": 1, "Townhall_Middle_Right#2": 1}}


tiles_possible_all = [  ("Townhall_Front_Left", ROT_NORTH), ("Townhall_Front_Left", ROT_EAST), ("Townhall_Front_Left", ROT_SOUTH), ("Townhall_Front_Left", ROT_WEST),
                        ("Townhall_Front_Right", ROT_NORTH), ("Townhall_Front_Right", ROT_EAST), ("Townhall_Front_Right", ROT_SOUTH), ("Townhall_Front_Right", ROT_WEST),
                        ("Townhall_Middle_Left", ROT_NORTH), ("Townhall_Middle_Left", ROT_EAST), ("Townhall_Middle_Left", ROT_SOUTH), ("Townhall_Middle_Left", ROT_WEST),
                        ("Townhall_Middle_Right", ROT_NORTH), ("Townhall_Middle_Right", ROT_EAST), ("Townhall_Middle_Right", ROT_SOUTH), ("Townhall_Middle_Right", ROT_WEST),
                        ("Townhall_End_Left", ROT_NORTH), ("Townhall_End_Left", ROT_EAST), ("Townhall_End_Left", ROT_SOUTH), ("Townhall_End_Left", ROT_WEST),
                        ("Townhall_End_Right", ROT_NORTH), ("Townhall_End_Right", ROT_EAST), ("Townhall_End_Right", ROT_SOUTH), ("Townhall_End_Right", ROT_WEST),
                        ("Air", ROT_ANY)]

tiles_possible_inner = tiles_possible_all

tiles_possible_edge_north = [   ("Townhall_Front_Left", ROT_NORTH), ("Townhall_Front_Left", ROT_WEST),
                                ("Townhall_Front_Right", ROT_NORTH), ("Townhall_Front_Right", ROT_EAST),
                                ("Townhall_Middle_Right", ROT_EAST), ("Townhall_Middle_Left", ROT_WEST),
                                ("Townhall_End_Right", ROT_EAST), ("Townhall_End_Left", ROT_WEST),
                                ("Townhall_End_Left", ROT_SOUTH), ("Townhall_End_Right", ROT_SOUTH),
                                ("Air", ROT_ANY)]

tiles_possible_edge_east =  [   ("Townhall_Front_Left", ROT_EAST), ("Townhall_Front_Left", ROT_NORTH),
                                ("Townhall_Front_Right", ROT_EAST), ("Townhall_Front_Right", ROT_SOUTH), 
                                ("Townhall_Middle_Right", ROT_SOUTH), ("Townhall_Middle_Left", ROT_NORTH),
                                ("Townhall_End_Left", ROT_WEST), ("Townhall_End_Left", ROT_NORTH),
                                ("Townhall_End_Right", ROT_WEST), ("Townhall_End_Right", ROT_SOUTH),
                                ("Air", ROT_ANY)]

tiles_possible_edge_top = tiles_possible_all

tiles_possible_edge_south = [   ("Townhall_Front_Left", ROT_SOUTH), ("Townhall_Front_Left", ROT_EAST),
                                ("Townhall_Front_Right", ROT_SOUTH), ("Townhall_Front_Right", ROT_WEST),
                                ("Townhall_Middle_Right", ROT_WEST), ("Townhall_Middle_Left", ROT_EAST),
                                ("Townhall_End_Right", ROT_WEST), ("Townhall_End_Left", ROT_EAST),
                                ("Townhall_End_Left", ROT_NORTH), ("Townhall_End_Right", ROT_NORTH),
                                ("Air", ROT_ANY)]


tiles_possible_edge_west =  [   ("Townhall_Front_Left", ROT_WEST), ("Townhall_Front_Left", ROT_SOUTH),
                                ("Townhall_Front_Right", ROT_WEST), ("Townhall_Front_Right", ROT_NORTH), 
                                ("Townhall_Middle_Right", ROT_NORTH), ("Townhall_Middle_Left", ROT_SOUTH),
                                ("Townhall_End_Left", ROT_EAST), ("Townhall_End_Left", ROT_SOUTH),
                                ("Townhall_End_Right", ROT_EAST), ("Townhall_End_Right", ROT_NORTH),
                                ("Air", ROT_ANY)]

tiles_possible_edge_bottom = tiles_possible_all


tile_rules = [  tiles_possible_all,
                tiles_possible_inner,
                tiles_possible_edge_north,
                tiles_possible_edge_east,
                tiles_possible_edge_top,
                tiles_possible_edge_south,
                tiles_possible_edge_west,
                tiles_possible_edge_bottom]
