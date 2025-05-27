# Directions: North = 0, East = 1, Top = 2, South = 3, West = 4, Bottom = 5
# Rotations Facing:  North = 0, East = 1, South = 2, West = 3, Don't Care = 4 
from tile import create_tile_direction_dict
from pyglm.glm import ivec3

TILE_SIZE = ivec3(13,23,7)

tile_quantity_limits = {}

tile_directions_zero = {    "Church_Tower":                 {   0: [("Air",4)],
                                                                1: [("Air",4)],
                                                                2: [],
                                                                3: [("Church_Middle", 0), ("Church_Altar", 0)],
                                                                4: [("Air",4)],
                                                                5: []},
                            "Church_Middle":                {   0: [("Church_Middle", 0)],
                                                                1: [("Air",4)],
                                                                2: [],
                                                                3: [("Church_Middle", 0), ("Church_Altar", 0)],
                                                                4: [("Air",4)],
                                                                5: []},
                            "Church_Altar":                 {   0: [("Church_Middle", 0)],
                                                                1: [("Air",4)],
                                                                2: [],
                                                                3: [("Air",4)],
                                                                4: [("Air",4)],
                                                                5: []},
                            "Air":                          {   0: [("Air",4), ],
                                                                1: [("Air",4), ],
                                                                2: [],
                                                                3: [],
                                                                4: [],
                                                                5: []}}

tiles_borders_rotation_invariant = ["Air"]

tile_directions = {}
for name, rot_zero_dict in tile_directions_zero.items():
    if name in tiles_borders_rotation_invariant:
        tile_directions.update({(name, 4): rot_zero_dict})
    else:
        tile_directions.update(create_tile_direction_dict(name, rot_zero_dict))

tile_weights = {    "Church_Tower": 1,
                    "Church_Middle": 10,
                    "Church_Altar" : 1,
                    "Air": 1}

variation_weights = {}


tiles_possible_all = [  ("Church_Tower", 0), ("Church_Tower", 1), ("Church_Tower", 2), ("Church_Tower", 3),
                        ("Church_Middle", 0), ("Church_Middle", 1), ("Church_Middle", 2), ("Church_Middle", 3),
                        ("Church_Altar", 0), ("Church_Altar", 1), ("Church_Altar", 2), ("Church_Altar", 3),
                        ("Air", 4)]

tiles_possible_inner = tiles_possible_all
tiles_possible_edge_north = [   ("Church_Tower", 0), ("Church_Tower", 1), ("Church_Tower", 3),
                                ("Church_Middle", 1), ("Church_Middle", 3),
                                ("Church_Altar", 1), ("Church_Altar", 2), ("Church_Altar", 3),
                                ("Air", 4)]

tiles_possible_edge_east =  [   ("Church_Tower", 0), ("Church_Tower", 1), ("Church_Tower", 2),
                                ("Church_Middle", 0), ("Church_Middle", 2),
                                ("Church_Altar", 0), ("Church_Altar", 2), ("Church_Altar", 3),
                                ("Air", 4)]

tiles_possible_edge_top = tiles_possible_all

tiles_possible_edge_south = [   ("Church_Tower", 1), ("Church_Tower", 2), ("Church_Tower", 3),
                                ("Church_Middle", 1), ("Church_Middle", 3),
                                ("Church_Altar", 0), ("Church_Altar", 1), ("Church_Altar", 3),
                                ("Air", 4)]


tiles_possible_edge_west =  [   ("Church_Tower", 0), ("Church_Tower", 2), ("Church_Tower", 3),
                                ("Church_Middle", 0), ("Church_Middle", 2),
                                ("Church_Altar", 0), ("Church_Altar", 1), ("Church_Altar", 2),
                                ("Air", 4)]

tiles_possible_edge_bottom = tiles_possible_all


tile_rules = [  tiles_possible_all,
                tiles_possible_inner,
                tiles_possible_edge_north,
                tiles_possible_edge_east,
                tiles_possible_edge_top,
                tiles_possible_edge_south,
                tiles_possible_edge_west,
                tiles_possible_edge_bottom]
