# Directions: North = 0, East = 1, Top = 2, South = 3, West = 4, Bottom = 5
# Rotations Facing:  North = 0, East = 1, South = 2, West = 3, Don't Care = 4 
from ...tile import create_tile_direction_dict
from ...tile import ROT_NORTH, ROT_EAST, ROT_SOUTH, ROT_WEST, ROT_ANY
from ...tile import DIR_NORTH, DIR_EAST, DIR_TOP, DIR_SOUTH, DIR_WEST, DIR_BOTTOM
from pyglm.glm import ivec3

TILE_SIZE = ivec3(13,16,5)

tile_quantity_limits = {}

tile_directions_zero = {    "Inn_Front":                 {   DIR_NORTH: [("Air",ROT_ANY)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Inn_Middle", ROT_NORTH), ("Inn_End", ROT_NORTH)],
                                                                DIR_WEST: [("Air",ROT_ANY)],
                                                                DIR_BOTTOM: []},
                            "Inn_Middle":                {   DIR_NORTH: [("Inn_Middle", ROT_NORTH)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
                                                                DIR_TOP: [],
                                                                DIR_SOUTH: [("Inn_Middle", ROT_NORTH), ("Inn_End", ROT_NORTH)],
                                                                DIR_WEST: [("Air",ROT_ANY)],
                                                                DIR_BOTTOM: []},
                            "Inn_End":                 {   DIR_NORTH: [("Inn_Middle", ROT_NORTH)],
                                                                DIR_EAST: [("Air",ROT_ANY)],
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

tile_weights = {    "Inn_Front": 1,
                    "Inn_Middle": 50,
                    "Inn_End" : 1,
                    "Air": 1}

variation_weights = {}


tiles_possible_all = [  ("Inn_Front", ROT_NORTH), ("Inn_Front", ROT_EAST), ("Inn_Front", ROT_SOUTH), ("Inn_Front", ROT_WEST),
                        ("Inn_Middle", ROT_NORTH), ("Inn_Middle", ROT_EAST), ("Inn_Middle", ROT_SOUTH), ("Inn_Middle", ROT_WEST),
                        ("Inn_End", ROT_NORTH), ("Inn_End", ROT_EAST), ("Inn_End", ROT_SOUTH), ("Inn_End", ROT_WEST),
                        ("Air", ROT_ANY)]

tiles_possible_inner = tiles_possible_all
tiles_possible_edge_north = [   ("Inn_Front", ROT_NORTH), ("Inn_Front", ROT_EAST), ("Inn_Front", ROT_WEST),
                                ("Inn_Middle", ROT_EAST), ("Inn_Middle", ROT_WEST),
                                ("Inn_End", ROT_EAST), ("Inn_End", ROT_SOUTH), ("Inn_End", ROT_WEST),
                                ("Air", ROT_ANY)]

tiles_possible_edge_east =  [   ("Inn_Front", ROT_NORTH), ("Inn_Front", ROT_EAST), ("Inn_Front", ROT_SOUTH),
                                ("Inn_Middle", ROT_NORTH), ("Inn_Middle", ROT_SOUTH),
                                ("Inn_End", ROT_NORTH), ("Inn_End", ROT_SOUTH), ("Inn_End", ROT_WEST),
                                ("Air", ROT_ANY)]

tiles_possible_edge_top = tiles_possible_all

tiles_possible_edge_south = [   ("Inn_Front", ROT_EAST), ("Inn_Front", ROT_SOUTH), ("Inn_Front", ROT_WEST),
                                ("Inn_Middle", ROT_EAST), ("Inn_Middle", ROT_WEST),
                                ("Inn_End", ROT_NORTH), ("Inn_End", ROT_EAST), ("Inn_End", ROT_WEST),
                                ("Air", ROT_ANY)]


tiles_possible_edge_west =  [   ("Inn_Front", ROT_NORTH), ("Inn_Front", ROT_SOUTH), ("Inn_Front", ROT_WEST),
                                ("Inn_Middle", ROT_NORTH), ("Inn_Middle", ROT_SOUTH),
                                ("Inn_End", ROT_NORTH), ("Inn_End", ROT_EAST), ("Inn_End", ROT_SOUTH),
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
