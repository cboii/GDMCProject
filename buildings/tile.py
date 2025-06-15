import random
from pyglm.glm import ivec3
from gdpc import Editor
from .building_module import *

ROT_NORTH = 0
ROT_EAST = 1
ROT_SOUTH = 2
ROT_WEST = 3
ROT_ANY = 4

ROT_CNR_NE = 0
ROT_CNR_SE = 1
ROT_CNR_SW = 2
ROT_CNR_NW = 3

DIR_NORTH = 0
DIR_EAST = 1
DIR_TOP = 2
DIR_SOUTH = 3
DIR_WEST = 4
DIR_BOTTOM = 5

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

class Tile:
    
    def __init__(self, grid_pos: ivec3, pos: ivec3, size: ivec3):
        self.possible_modules = {}
        self.entropy = 0
        self.neighbors = {}
        self.selected_module = None
        self.pos = ivec3(pos)
        self.grid_pos = ivec3(grid_pos)
        self.updated = False
        self.size = ivec3(size)

    def add_possible_modules(self, modules: dict):
        self.possible_modules.update(modules)
        self.entropy = len(self.possible_modules)

    def set_possible_modules(self, modules: dict):
        self.possible_modules = modules
        self.entropy = len(self.possible_modules)

    def get_possible_modules(self):
        return self.possible_modules

    def set_neighbor(self, direction: int, neighbor):
        self.neighbors[direction] = neighbor

    def get_neighbors(self):
        return self.neighbors
    
    def update(self, tile_quantity_limits: dict):
        if self.entropy == 0 or self.updated:
            return
        
        #print(f"Updating tile {tuple(self.grid_pos)}.")
        possible_modules_neighbors = {}
        for dir, neighbor in self.neighbors.items():
            if (neighbor.updated or neighbor.entropy == 0) and list(neighbor.possible_modules.keys())[0] != ["Air"]:
                possible_modules_neighbors[dir] = neighbor.possible_modules

        possible_for_tile_per_neighbor = []
        for dir, p_modules in possible_modules_neighbors.items():
            possible_for_tile_in_neighbor = set()
            for modules in p_modules.values():
                possible_for_tile_in_neighbor.update(modules[(dir+3)%6])
            possible_for_tile_per_neighbor.append(list(possible_for_tile_in_neighbor))
        #print(possible_for_tile_per_neighbor)
        possible_for_tile = set(possible_for_tile_per_neighbor[0]).intersection(*possible_for_tile_per_neighbor)
        #print(f"Ppt: {possible_for_tile}")
        

        previously_possible = self.possible_modules
        still_possible = {}
        for tile in previously_possible.keys():
            if tile in possible_for_tile:
                if tile not in tile_quantity_limits.keys() or tile_quantity_limits[tile] > 0:
                    still_possible[tile] = previously_possible[tile]

        self.possible_modules = still_possible
        self.entropy = len(self.possible_modules)
        print(list(self.possible_modules.keys())[0][0])
        if self.entropy == 1 and list(self.possible_modules.keys())[0][0] == "Air":
            self.entropy = 100
        self.updated = True
        #print(f"After update possible tiles: {list(self.possible_modules.keys())}")
        if len(previously_possible)-len(still_possible) > 0:
            for nb in self.neighbors.values():
                    nb.update(tile_quantity_limits)

    def select(self, tile_quantity_limits: dict, tile_weights: dict):
        print(f"Selecting tile {tuple(self.grid_pos)}.")
        module_list = list(self.possible_modules.keys())

        if self.entropy == 1:
            self.selected_module = module_list[0]
        elif self.entropy > 1: 
            weights = [tile_weights[module[0]] for module in module_list]
            self.selected_module = random.choices(list(self.possible_modules.keys()), weights=weights, k=1)[0]
            self.possible_modules = {self.selected_module: self.possible_modules[self.selected_module]}
        else:
            print("Entropy = 0")
        print(f"Selected Module {self.selected_module}")
        if self.selected_module in tile_quantity_limits.keys(): 
            tile_quantity_limits[self.selected_module] -= 1
        self.entropy = 0
        for dir, nb in self.neighbors.items():
            nb.update(tile_quantity_limits)

    def build(self, editor: Editor, variation_weights: dict, wood_type: str="oak"):
        build_area = editor.getBuildArea()
        pos_global = ivec3(build_area.offset.x + self.pos.x, self.pos.y, build_area.offset.z + self.pos.z)
        print(f"Pos Global: {pos_global}")
        module, rotation = self.selected_module
        if module in variation_weights.keys():
            if rotation == 4:
                rotation = random.randint(0,3)
            module_name = random.choices(list(variation_weights[module].keys()), list(variation_weights[module].values()), k=1)[0]
        elif module == "Air":
            module_name = "Air"
        else:
            module_name = f"{module}#0"
        build_module_global(editor, module_name, pos_global, self.size, rotation, wood_type)