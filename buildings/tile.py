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
    
    def update(self, from_direction: int):

        if self.entropy == 0:
            return

        neighbor = self.neighbors[from_direction]
        previously_possible = self.possible_modules
        still_possible = {}

        for n_tile, n_directions in neighbor.possible_modules.items():
            for tile, directions in previously_possible.items():
                if directions[from_direction] == n_directions[(from_direction+3) % 6]:
                    still_possible[tile] = directions

        self.possible_modules = still_possible
        self.entropy = len(self.possible_modules)

        if len(previously_possible)-len(still_possible) > 0:
            for dir, nb in self.neighbors.items():
                if dir != from_direction:
                    nb.update((dir+3) % 6)

    def select(self):
        if self.entropy == 1:
            self.selected_module = list(self.possible_modules.keys())[0]
        elif self.entropy > 1: 
            self.selected_module = choice(list(self.possible_modules.keys()))
            self.possible_modules = {self.selected_module: self.possible_modules[self.selected_module]}
        else:
            print("Entropy = 0")
        
        self.entropy = 0
        for dir, nb in self.neighbors.items():
            nb.update((dir+3) % 6)

    def build(self, editor: Editor):
        build_module_global(editor, self.selected_module, self.pos)