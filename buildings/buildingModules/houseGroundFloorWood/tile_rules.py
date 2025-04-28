# Directions: North = 0, East = 1, Bottom = 2, South = 3, West = 4, Top = 5
# Rotations Facing:  North = 0, East = 1, South = 2, West = 3, Don't Care = 4 

def create_tile_direction_dict(module_name: str, rot_zero_dict: dict):
    output = {(module_name, 0): rot_zero_dict}
    for i in range(1,4):
        rot_i_dict = {}
        for j in range(6):
            if j in [2,5]:
                rot_i_dict[j] = [(name,(rot+i)%4) for name,rot in rot_zero_dict[j]]
            else:
                direction_list = [0,1,3,4]
                direction = direction_list.index(j)
                new_direction = (direction+i)%4
                dict_key = direction_list[new_direction]

                rot_i_dict[dict_key] = [(name, 4) if rot == 4 else (name,(rot+i)%4) for name,rot in rot_zero_dict[j]]

        output.update({(module_name,i): dict(sorted(rot_i_dict.items()))})
    return output
            


tile_directions_zero = {    "HouseGroundFloorWood_Ceiling": {   0: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0), ("HouseGroundFloorWood_Ceiling",4), ("HouseGroundFloorWood_Stairs",4)],
                                                                1: [("HouseGroundFloorWood_Wall",1),("HouseGroundFloorWood_Window",1), ("HouseGroundFloorWood_Ceiling",4), ("HouseGroundFloorWood_Stairs",4)],
                                                                2: [],
                                                                3: [("HouseGroundFloorWood_Wall",2),("HouseGroundFloorWood_Window",2), ("HouseGroundFloorWood_Ceiling",4), ("HouseGroundFloorWood_Stairs",4)],
                                                                4: [("HouseGroundFloorWood_Wall",3),("HouseGroundFloorWood_Window",3), ("HouseGroundFloorWood_Ceiling",4), ("HouseGroundFloorWood_Stairs",4)],
                                                                5: []},
                            "HouseGroundFloorWood_Stairs":  {   0: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0), ("HouseGroundFloorWood_Ceiling",4)],
                                                                1: [("HouseGroundFloorWood_Wall",1),("HouseGroundFloorWood_Window",1), ("HouseGroundFloorWood_Ceiling",4)],
                                                                2: [],
                                                                3: [("HouseGroundFloorWood_Wall",2),("HouseGroundFloorWood_Window",2), ("HouseGroundFloorWood_Ceiling",4)],
                                                                4: [("HouseGroundFloorWood_Wall",3),("HouseGroundFloorWood_Window",3), ("HouseGroundFloorWood_Ceiling",4)],
                                                                5: []},
                            "HouseGroundFloorWood_Wall":    {   0: [("Air",4)],
                                                                1: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",0)],
                                                                2: [],
                                                                3: [("HouseGroundFloorWood_Ceiling",4), ("HouseGroundFloorWood_Stairs",4),("HouseGroundFloorWood_Wall",2),("HouseGroundFloorWood_Window",2)],
                                                                4: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",3)],
                                                                5: []},                    
                            "HouseGroundFloorWood_Door":    {   0: [("Air",4)],
                                                                1: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",0)],
                                                                2: [],
                                                                3: [("HouseGroundFloorWood_Ceiling",4),("HouseGroundFloorWood_Wall",2),("HouseGroundFloorWood_Window",2)],
                                                                4: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",3)],
                                                                5: []},
                            "HouseGroundFloorWood_Window":  {   0: [("Air",4)],
                                                                1: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",0)],
                                                                2: [],
                                                                3: [("HouseGroundFloorWood_Ceiling",4), ("HouseGroundFloorWood_Stairs",4),("HouseGroundFloorWood_Wall",2),("HouseGroundFloorWood_Window",2)],
                                                                4: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",3)],
                                                                5: []},
                            "HouseGroundFloorWood_Corner":  {   0: [("Air",4)],
                                                                1: [("Air",4)],
                                                                2: [],
                                                                3: [("HouseGroundFloorWood_Wall",1),("HouseGroundFloorWood_Window",1),("HouseGroundFloorWood_Corner",1)],
                                                                4: [("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",3)],
                                                                5: []},
                            "Air":                          {   0: [("Air",4), ("HouseGroundFloorWood_Wall",2),("HouseGroundFloorWood_Window",2),("HouseGroundFloorWood_Corner",1),("HouseGroundFloorWood_Corner",2)],
                                                                1: [("Air",4), ("HouseGroundFloorWood_Wall",3),("HouseGroundFloorWood_Window",3),("HouseGroundFloorWood_Corner",2),("HouseGroundFloorWood_Corner",3)],
                                                                2: [],
                                                                3: [("Air",4), ("HouseGroundFloorWood_Wall",0),("HouseGroundFloorWood_Window",0),("HouseGroundFloorWood_Corner",0),("HouseGroundFloorWood_Corner",3)],
                                                                4: [("Air",4), ("HouseGroundFloorWood_Wall",1),("HouseGroundFloorWood_Window",1),("HouseGroundFloorWood_Corner",0),("HouseGroundFloorWood_Corner",1)],
                                                                5: []}}

tiles_borders_rotation_invariant = ["Air", "HouseGroundFloorWood_Ceiling", "HouseGroundFloorWood_Stairs"]

tile_directions = {}
for name, rot_zero_dict in tile_directions_zero.items():
    if name in tiles_borders_rotation_invariant:
        tile_directions.update({(name, 4): rot_zero_dict})
    else:
        tile_directions.update(create_tile_direction_dict(name, rot_zero_dict))
print(tile_directions)

tile_weights = {    "HouseGroundFloorWood_Ceiling": 7,
                    "HouseGroundFloorWood_Stairs": 1,
                    "HouseGroundFloorWood_Wall": 10,
                    "HouseGroundFloorWood_Door": 1,
                    "HouseGroundFloorWood_Window": 7,
                    "HouseGroundFloorWood_Corner": 1,
                    "Air": 1}

variation_weights = {   "HouseGroundFloorWood_Ceiling": {"HouseGroundFloorWood_Ceiling#0": 6, "HouseGroundFloorWood_Ceiling#1": 2, "HouseGroundFloorWood_Ceiling#2": 1, "HouseGroundFloorWood_Ceiling#3": 2},
                        "HouseGroundFloorWood_Wall" : {"HouseGroundFloorWood_Wall#0": 5, "HouseGroundFloorWood_Wall#1": 1, "HouseGroundFloorWood_Wall#2": 2, "HouseGroundFloorWood_Wall#3": 2, "HouseGroundFloorWood_Wall#4": 2},
                        "HouseGroundFloorWood_Window" : {"HouseGroundFloorWood_Window#0": 5, "HouseGroundFloorWood_Window#1": 1, "HouseGroundFloorWood_Window#2": 2, "HouseGroundFloorWood_Window#3": 2, "HouseGroundFloorWood_Window#4": 2}}


tiles_possible_all = [  ("HouseGroundFloorWood_Ceiling", 4),
                        ("HouseGroundFloorWood_Stairs", 4),
                        ("HouseGroundFloorWood_Wall", 0), ("HouseGroundFloorWood_Wall", 1), ("HouseGroundFloorWood_Wall", 2), ("HouseGroundFloorWood_Wall", 3),
                        ("HouseGroundFloorWood_Door", 0), ("HouseGroundFloorWood_Door", 1), ("HouseGroundFloorWood_Door", 2), ("HouseGroundFloorWood_Door", 3),
                        ("HouseGroundFloorWood_Window", 0), ("HouseGroundFloorWood_Window", 1), ("HouseGroundFloorWood_Window", 2), ("HouseGroundFloorWood_Window", 3),
                        ("HouseGroundFloorWood_Corner", 0), ("HouseGroundFloorWood_Corner", 1), ("HouseGroundFloorWood_Corner", 2), ("HouseGroundFloorWood_Corner", 3),
                        ("Air", 4)]

tiles_possible_inner = [("HouseGroundFloorWood_Ceiling", 4),
                        ("HouseGroundFloorWood_Stairs", 4),
                        ("HouseGroundFloorWood_Wall", 0), ("HouseGroundFloorWood_Wall", 1), ("HouseGroundFloorWood_Wall", 2), ("HouseGroundFloorWood_Wall", 3),
                        ("HouseGroundFloorWood_Door", 0), ("HouseGroundFloorWood_Door", 1), ("HouseGroundFloorWood_Door", 2), ("HouseGroundFloorWood_Door", 3),
                        ("HouseGroundFloorWood_Window", 0), ("HouseGroundFloorWood_Window", 1), ("HouseGroundFloorWood_Window", 2), ("HouseGroundFloorWood_Window", 3),
                        ("HouseGroundFloorWood_Corner", 0), ("HouseGroundFloorWood_Corner", 1), ("HouseGroundFloorWood_Corner", 2), ("HouseGroundFloorWood_Corner", 3),
                        ("Air", 4)]

tiles_possible_edge_north = [   ("HouseGroundFloorWood_Wall", 0),  
                                ("HouseGroundFloorWood_Window", 0),
                                ("HouseGroundFloorWood_Door", 0), 
                                ("HouseGroundFloorWood_Corner", 0),
                                ("HouseGroundFloorWood_Corner", 3),
                                ("Air", 4)]

tiles_possible_edge_east =  [   ("HouseGroundFloorWood_Wall", 1),  
                                ("HouseGroundFloorWood_Window", 1),
                                ("HouseGroundFloorWood_Door", 1), 
                                ("HouseGroundFloorWood_Corner", 0), 
                                ("HouseGroundFloorWood_Corner", 1),
                                ("Air", 4)]

tiles_possible_edge_top = [ ("HouseGroundFloorWood_Ceiling", 4),
                            ("HouseGroundFloorWood_Stairs", 4),
                            ("HouseGroundFloorWood_Wall", 0), ("HouseGroundFloorWood_Wall", 1), ("HouseGroundFloorWood_Wall", 2), ("HouseGroundFloorWood_Wall", 3),
                            ("HouseGroundFloorWood_Door", 0), ("HouseGroundFloorWood_Door", 1), ("HouseGroundFloorWood_Door", 2), ("HouseGroundFloorWood_Door", 3),
                            ("HouseGroundFloorWood_Window", 0), ("HouseGroundFloorWood_Window", 1), ("HouseGroundFloorWood_Window", 2), ("HouseGroundFloorWood_Window", 3),
                            ("HouseGroundFloorWood_Corner", 0), ("HouseGroundFloorWood_Corner", 1), ("HouseGroundFloorWood_Corner", 2), ("HouseGroundFloorWood_Corner", 3),
                            ("Air", 4)]

tiles_possible_edge_south = [   ("HouseGroundFloorWood_Wall", 2),  
                                ("HouseGroundFloorWood_Window", 2),
                                ("HouseGroundFloorWood_Door", 2), 
                                ("HouseGroundFloorWood_Corner", 1), 
                                ("HouseGroundFloorWood_Corner", 2),
                                ("Air", 4)]

tiles_possible_edge_west =  [   ("HouseGroundFloorWood_Wall", 3),  
                                ("HouseGroundFloorWood_Window", 3),
                                ("HouseGroundFloorWood_Door", 3), 
                                ("HouseGroundFloorWood_Corner", 2), 
                                ("HouseGroundFloorWood_Corner", 3),
                                ("Air", 4)]

tiles_possible_edge_bottom = [  ("HouseGroundFloorWood_Ceiling", 4),
                                ("HouseGroundFloorWood_Stairs", 4),
                                ("HouseGroundFloorWood_Wall", 0), ("HouseGroundFloorWood_Wall", 1), ("HouseGroundFloorWood_Wall", 2), ("HouseGroundFloorWood_Wall", 3),
                                ("HouseGroundFloorWood_Door", 0), ("HouseGroundFloorWood_Door", 1), ("HouseGroundFloorWood_Door", 2), ("HouseGroundFloorWood_Door", 3),
                                ("HouseGroundFloorWood_Window", 0), ("HouseGroundFloorWood_Window", 1), ("HouseGroundFloorWood_Window", 2), ("HouseGroundFloorWood_Window", 3),
                                ("HouseGroundFloorWood_Corner", 0), ("HouseGroundFloorWood_Corner", 1), ("HouseGroundFloorWood_Corner", 2), ("HouseGroundFloorWood_Corner", 3),
                                ("Air", 4)]


tile_rules = [  tiles_possible_all,
                tiles_possible_inner,
                tiles_possible_edge_north,
                tiles_possible_edge_east,
                tiles_possible_edge_top,
                tiles_possible_edge_south,
                tiles_possible_edge_west,
                tiles_possible_edge_bottom]
