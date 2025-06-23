from ...base_foundation import place_rect_foundation, place_border, smooth_edges_gaussian
from ...building_module import build_module_global
from maps.blueprint import Blueprint
from typing import Union, Sequence
from gdpc import Block
from gdpc.vector_tools import Rect
from pyglm.glm import ivec3
from random import choice

tile_sizes = {"3x3": ivec3(3,15,3),
              "5x5": ivec3(5,15,5),
              "10x10": ivec3(10,15,10),
              "12x12": ivec3(12,15,12)}

variations = {"3x3": 3,
              "5x5": 1,
              "10x10": 1,
              "12x12": 1}

def build_tree( blueprint: Blueprint, name: str, area: Rect,
                    foundation_block: Union[Block, Sequence[Block]] = Block("grass_block"), wood_type: str = "oak"):
    editor = blueprint.map_features.editor
    #smooth_edges_gaussian(blueprint, area, sigma=5, max_width=10, include_area=True)
    y = place_rect_foundation(blueprint, area, foundation_block)
    tile_size = tile_sizes[name]
    print(f"Building Tree {name}.")
    variation = choice(list(range(variations[name])))
    module = f"Tree_Custom_{name}#{variation}"
    entrance_rotation = choice([0,1,2,3])

    build_area = editor.getBuildArea()
    build_module_global(editor, module, (build_area.offset.x + area.offset.x, y, build_area.offset.z + area.offset.y), tile_size, entrance_rotation, wood_type)

    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area)