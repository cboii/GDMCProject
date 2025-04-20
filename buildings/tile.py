from random import choice
from pyglm.glm import ivec3
from gdpc import Editor
from building_module import *


NORTH = 0
EAST = 1
TOP = 2
SOUTH = 3
WEST = 4
BOTTOM = 5

class Tile:
    
    def __init__(self, grid_pos: ivec3, pos: ivec3):
        self.possible_modules = {}
        self.entropy = 0
        self.neighbors = {}
        self.selected_module = None
        self.pos = pos
        self.grid_pos = grid_pos
        self.updated = False

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
    
    def update(self):
        print(f"Updating tile {self.grid_pos}. Entropy {self.entropy}. Possible Modules {list(self.possible_modules.keys())}.")
        if self.entropy == 0 or self.updated:
            return
        
        possible_modules_neighbors = {}
        for dir, neighbor in self.neighbors.items():
            if (neighbor.updated or neighbor.entropy == 0) and neighbor.possible_modules.keys() != ["Air"]:
                possible_modules_neighbors[dir] = neighbor.possible_modules

        possible_for_tile_per_neighbor = []
        for dir, p_modules in possible_modules_neighbors.items():
            possible_for_tile_in_neighbor = set()
            for modules in p_modules.values():
                possible_for_tile_in_neighbor.update(modules[(dir+3)%6])
            possible_for_tile_per_neighbor.append(list(possible_for_tile_in_neighbor))
        print(possible_for_tile_per_neighbor)

        possible_for_tile = set(possible_for_tile_per_neighbor[0]).intersection(*possible_for_tile_per_neighbor)
        
        print(possible_for_tile)

        previously_possible = self.possible_modules
        still_possible = {}
        for tile in previously_possible.keys():
            if tile in possible_for_tile:
                still_possible[tile] = previously_possible[tile]

        self.possible_modules = still_possible
        self.entropy = len(self.possible_modules)
        print(f"After Update possible modules {list(self.possible_modules.keys())}")
        self.updated = True
        if len(previously_possible)-len(still_possible) > 0:
            for nb in self.neighbors.values():
                    nb.update()

    def select(self):
        if self.entropy == 1:
            self.selected_module = list(self.possible_modules.keys())[0]
        elif self.entropy > 1: 
            self.selected_module = choice(list(self.possible_modules.keys()))
            self.possible_modules = {self.selected_module: self.possible_modules[self.selected_module]}
        else:
            print("Entropy = 0")
        print(f"Selected Module {self.selected_module}")
        self.entropy = 0
        for dir, nb in self.neighbors.items():
            nb.update()

    def build(self, editor: Editor):
        build_module_global(editor, self.selected_module, self.pos)