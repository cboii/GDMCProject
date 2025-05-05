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
            


tile_directions_zero = {    "House_Wood_Ceiling":           {   0: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0), ("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0), ("House_Wood_Ceiling",4), ("House_Wood_Stairs",0)],
                                                                1: [("House_Wood_GF_Wall",1),("House_Wood_GF_Window",1), ("House_Wood_UF_Wall",1),("House_Wood_UF_Window",1), ("House_Wood_Ceiling",4), ("House_Wood_Stairs",0)],
                                                                2: [("House_Wood_Ceiling",4)],
                                                                3: [("House_Wood_GF_Wall",2),("House_Wood_GF_Window",2), ("House_Wood_UF_Wall",2),("House_Wood_UF_Window",2), ("House_Wood_Ceiling",4), ("House_Wood_Stairs",0)],
                                                                4: [("House_Wood_GF_Wall",3),("House_Wood_GF_Window",3), ("House_Wood_UF_Wall",3),("House_Wood_UF_Window",3), ("House_Wood_Ceiling",4), ("House_Wood_Stairs",0)],
                                                                5: [("House_Wood_Ceiling",4)]},
                            "House_Wood_Stairs":            {   0: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0), ("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0), ("House_Wood_Ceiling",4)],
                                                                1: [("House_Wood_GF_Wall",1),("House_Wood_GF_Window",1), ("House_Wood_UF_Wall",1),("House_Wood_UF_Window",1), ("House_Wood_Ceiling",4)],
                                                                2: [("House_Wood_Stairs",0)],
                                                                3: [("House_Wood_GF_Wall",2),("House_Wood_GF_Window",2), ("House_Wood_UF_Wall",2),("House_Wood_UF_Window",2), ("House_Wood_Ceiling",4)],
                                                                4: [("House_Wood_GF_Wall",3),("House_Wood_GF_Window",3), ("House_Wood_UF_Wall",3),("House_Wood_UF_Window",3), ("House_Wood_Ceiling",4)],
                                                                5: [("House_Wood_Stairs",0)]},
                            "House_Wood_GF_Wall":           {   0: [("Air",4)],
                                                                1: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",0)],
                                                                2: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0)],
                                                                3: [("House_Wood_Ceiling",4), ("House_Wood_Stairs",0),("House_Wood_GF_Wall",2),("House_Wood_GF_Window",2)],
                                                                4: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",3)],
                                                                5: []},                    
                            "House_Wood_GF_Door":           {   0: [("Air",4)],
                                                                1: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",0)],
                                                                2: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0)],
                                                                3: [("House_Wood_Ceiling",4),("House_Wood_GF_Wall",2),("House_Wood_GF_Window",2)],
                                                                4: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",3)],
                                                                5: []},
                            "House_Wood_GF_Window":         {   0: [("Air",4)],
                                                                1: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",0)],
                                                                2: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0)],
                                                                3: [("House_Wood_Ceiling",4), ("House_Wood_Stairs",0),("House_Wood_GF_Wall",2),("House_Wood_GF_Window",2)],
                                                                4: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",3)],
                                                                5: []},
                            "House_Wood_GF_Corner":         {   0: [("Air",4)],
                                                                1: [("Air",4)],
                                                                2: [("House_Wood_UF_Corner",0)],
                                                                3: [("House_Wood_GF_Wall",1),("House_Wood_GF_Window",1),("House_Wood_GF_Corner",1)],
                                                                4: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",3)],
                                                                5: []},
                            "House_Wood_UF_Wall":           {   0: [("Air",4)],
                                                                1: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0),("House_Wood_UF_Corner",0)],
                                                                2: [],
                                                                3: [("House_Wood_Ceiling",4), ("House_Wood_Stairs",0),("House_Wood_UF_Wall",2),("House_Wood_UF_Window",2)],
                                                                4: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0),("House_Wood_UF_Corner",3)],
                                                                5: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0)]},                    
                            "House_Wood_UF_Window":         {   0: [("Air",4)],
                                                                1: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0),("House_Wood_UF_Corner",0)],
                                                                2: [],
                                                                3: [("House_Wood_Ceiling",4), ("House_Wood_Stairs",0),("House_Wood_UF_Wall",2),("House_Wood_UF_Window",2)],
                                                                4: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0),("House_Wood_UF_Corner",3)],
                                                                5: [("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0)]},
                            "House_Wood_UF_Corner":         {   0: [("Air",4)],
                                                                1: [("Air",4)],
                                                                2: [],
                                                                3: [("House_Wood_UF_Wall",1),("House_Wood_UF_Window",1),("House_Wood_UF_Corner",1)],
                                                                4: [("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0),("House_Wood_UF_Corner",3)],
                                                                5: [("House_Wood_GF_Corner",0)]},
                            "Air":                          {   0: [("Air",4), ("House_Wood_GF_Wall",2),("House_Wood_GF_Window",2),("House_Wood_GF_Corner",1),("House_Wood_GF_Corner",2),("House_Wood_UF_Wall",2),("House_Wood_UF_Window",2),("House_Wood_UF_Corner",1),("House_Wood_UF_Corner",2)],
                                                                1: [("Air",4), ("House_Wood_GF_Wall",3),("House_Wood_GF_Window",3),("House_Wood_GF_Corner",2),("House_Wood_GF_Corner",3),("House_Wood_UF_Wall",3),("House_Wood_UF_Window",3),("House_Wood_UF_Corner",2),("House_Wood_UF_Corner",3)],
                                                                2: [("Air",4)],
                                                                3: [("Air",4), ("House_Wood_GF_Wall",0),("House_Wood_GF_Window",0),("House_Wood_GF_Corner",0),("House_Wood_GF_Corner",3),("House_Wood_UF_Wall",0),("House_Wood_UF_Window",0),("House_Wood_UF_Corner",0),("House_Wood_UF_Corner",3)],
                                                                4: [("Air",4), ("House_Wood_GF_Wall",1),("House_Wood_GF_Window",1),("House_Wood_GF_Corner",0),("House_Wood_GF_Corner",1),("House_Wood_UF_Wall",1),("House_Wood_UF_Window",1),("House_Wood_UF_Corner",0),("House_Wood_UF_Corner",1)],
                                                                5: [("Air",4)]}}

tiles_borders_rotation_invariant = ["Air", "House_Wood_Ceiling"]

tile_directions = {}
for name, rot_zero_dict in tile_directions_zero.items():
    if name in tiles_borders_rotation_invariant:
        tile_directions.update({(name, 4): rot_zero_dict})
    else:
        tile_directions.update(create_tile_direction_dict(name, rot_zero_dict))

tile_weights = {    "House_Wood_Ceiling": 7,
                    "House_Wood_Stairs": 1,
                    "House_Wood_GF_Wall": 10,
                    "House_Wood_GF_Door": 1,
                    "House_Wood_GF_Window": 7,
                    "House_Wood_GF_Corner": 1,
                    "House_Wood_UF_Wall": 10,
                    "House_Wood_UF_Window": 7,
                    "House_Wood_UF_Corner": 1,
                    "Air": 1}

variation_weights = {   "House_Wood_Ceiling": {"House_Wood_Ceiling#0": 6, "House_Wood_Ceiling#1": 2, "House_Wood_Ceiling#2": 1, "House_Wood_Ceiling#3": 2},
                        "House_Wood_GF_Wall" : {"House_Wood_GF_Wall#0": 5, "House_Wood_GF_Wall#1": 1, "House_Wood_GF_Wall#2": 2, "House_Wood_GF_Wall#3": 2, "House_Wood_GF_Wall#4": 2},
                        "House_Wood_GF_Window" : {"House_Wood_GF_Window#0": 5, "House_Wood_GF_Window#1": 1, "House_Wood_GF_Window#2": 2, "House_Wood_GF_Window#3": 2, "House_Wood_GF_Window#4": 2},
                        "House_Wood_UF_Wall" : {"House_Wood_UF_Wall#0": 5, "House_Wood_UF_Wall#1": 1, "House_Wood_UF_Wall#2": 2, "House_Wood_UF_Wall#3": 2, "House_Wood_UF_Wall#4": 2, "House_Wood_UF_Wall#5": 5, "House_Wood_UF_Wall#6": 2, "House_Wood_UF_Wall#7": 2, "House_Wood_UF_Wall#8": 2, "House_Wood_UF_Wall#9": 2,},
                        "House_Wood_UF_Window" : {"House_Wood_UF_Window#0": 5, "House_Wood_UF_Window#1": 1, "House_Wood_UF_Window#2": 2, "House_Wood_UF_Window#3": 2, "House_Wood_UF_Window#4": 2},
                        "House_Wood_UF_Corner": {"House_Wood_UF_Corner#0": 5, "House_Wood_UF_Corner#1": 2, "House_Wood_UF_Corner#2": 2, "House_Wood_UF_Corner#3": 2, "House_Wood_UF_Corner#4": 2}}


tiles_possible_all = [  ("House_Wood_Ceiling", 4),
                        ("House_Wood_Stairs", 0),
                        ("House_Wood_GF_Wall", 0), ("House_Wood_GF_Wall", 1), ("House_Wood_GF_Wall", 2), ("House_Wood_GF_Wall", 3),
                        ("House_Wood_GF_Door", 0), ("House_Wood_GF_Door", 1), ("House_Wood_GF_Door", 2), ("House_Wood_GF_Door", 3),
                        ("House_Wood_GF_Window", 0), ("House_Wood_GF_Window", 1), ("House_Wood_GF_Window", 2), ("House_Wood_GF_Window", 3),
                        ("House_Wood_GF_Corner", 0), ("House_Wood_GF_Corner", 1), ("House_Wood_GF_Corner", 2), ("House_Wood_GF_Corner", 3),
                        ("House_Wood_UF_Wall", 0), ("House_Wood_UF_Wall", 1), ("House_Wood_UF_Wall", 2), ("House_Wood_UF_Wall", 3),
                        ("House_Wood_UF_Window", 0), ("House_Wood_UF_Window", 1), ("House_Wood_UF_Window", 2), ("House_Wood_UF_Window", 3),
                        ("House_Wood_UF_Corner", 0), ("House_Wood_UF_Corner", 1), ("House_Wood_UF_Corner", 2), ("House_Wood_UF_Corner", 3),
                        ("Air", 4)]

tiles_possible_inner = [("House_Wood_Ceiling", 4),
                        ("House_Wood_Stairs", 0),
                        ("House_Wood_UF_Wall", 0), ("House_Wood_UF_Wall", 1), ("House_Wood_UF_Wall", 2), ("House_Wood_UF_Wall", 3),
                        ("House_Wood_UF_Window", 0), ("House_Wood_UF_Window", 1), ("House_Wood_UF_Window", 2), ("House_Wood_UF_Window", 3),
                        ("House_Wood_UF_Corner", 0), ("House_Wood_UF_Corner", 1), ("House_Wood_UF_Corner", 2), ("House_Wood_UF_Corner", 3),
                        ("Air", 4)]

tiles_possible_edge_north = [   ("House_Wood_GF_Wall", 0),  
                                ("House_Wood_GF_Window", 0),
                                ("House_Wood_GF_Door", 0), 
                                ("House_Wood_GF_Corner", 0),
                                ("House_Wood_GF_Corner", 3),
                                ("House_Wood_UF_Wall", 0),  
                                ("House_Wood_UF_Window", 0),
                                ("House_Wood_UF_Corner", 0),
                                ("House_Wood_UF_Corner", 3),
                                ("Air", 4)]

tiles_possible_edge_east =  [   ("House_Wood_GF_Wall", 1),  
                                ("House_Wood_GF_Window", 1),
                                ("House_Wood_GF_Door", 1), 
                                ("House_Wood_GF_Corner", 0), 
                                ("House_Wood_GF_Corner", 1),
                                ("House_Wood_UF_Wall", 1),  
                                ("House_Wood_UF_Window", 1), 
                                ("House_Wood_UF_Corner", 0), 
                                ("House_Wood_UF_Corner", 1),
                                ("Air", 4)]

tiles_possible_edge_top = [ ("House_Wood_Ceiling", 4),
                            ("House_Wood_Stairs", 0),
                            ("House_Wood_UF_Wall", 0), ("House_Wood_UF_Wall", 1), ("House_Wood_UF_Wall", 2), ("House_Wood_UF_Wall", 3),
                            ("House_Wood_UF_Window", 0), ("House_Wood_UF_Window", 1), ("House_Wood_UF_Window", 2), ("House_Wood_UF_Window", 3),
                            ("House_Wood_UF_Corner", 0), ("House_Wood_UF_Corner", 1), ("House_Wood_UF_Corner", 2), ("House_Wood_UF_Corner", 3),
                            ("Air", 4)]

tiles_possible_edge_south = [   ("House_Wood_GF_Wall", 2),  
                                ("House_Wood_GF_Window", 2),
                                ("House_Wood_GF_Door", 2), 
                                ("House_Wood_GF_Corner", 1), 
                                ("House_Wood_GF_Corner", 2),
                                ("House_Wood_UF_Wall", 2),  
                                ("House_Wood_UF_Window", 2), 
                                ("House_Wood_UF_Corner", 1), 
                                ("House_Wood_UF_Corner", 2),
                                ("Air", 4)]

tiles_possible_edge_west =  [   ("House_Wood_GF_Wall", 3),  
                                ("House_Wood_GF_Window", 3),
                                ("House_Wood_GF_Door", 3), 
                                ("House_Wood_GF_Corner", 2), 
                                ("House_Wood_GF_Corner", 3),
                                ("House_Wood_UF_Wall", 3),  
                                ("House_Wood_UF_Window", 3),
                                ("House_Wood_UF_Corner", 2), 
                                ("House_Wood_UF_Corner", 3),
                                ("Air", 4)]

tiles_possible_edge_bottom = [  ("House_Wood_Ceiling", 4),
                                ("House_Wood_Stairs", 0),
                                ("House_Wood_GF_Wall", 0), ("House_Wood_GF_Wall", 1), ("House_Wood_GF_Wall", 2), ("House_Wood_GF_Wall", 3),
                                ("House_Wood_GF_Door", 0), ("House_Wood_GF_Door", 1), ("House_Wood_GF_Door", 2), ("House_Wood_GF_Door", 3),
                                ("House_Wood_GF_Window", 0), ("House_Wood_GF_Window", 1), ("House_Wood_GF_Window", 2), ("House_Wood_GF_Window", 3),
                                ("House_Wood_GF_Corner", 0), ("House_Wood_GF_Corner", 1), ("House_Wood_GF_Corner", 2), ("House_Wood_GF_Corner", 3),
                                ("Air", 4)]


tile_rules = [  tiles_possible_all,
                tiles_possible_inner,
                tiles_possible_edge_north,
                tiles_possible_edge_east,
                tiles_possible_edge_top,
                tiles_possible_edge_south,
                tiles_possible_edge_west,
                tiles_possible_edge_bottom]
