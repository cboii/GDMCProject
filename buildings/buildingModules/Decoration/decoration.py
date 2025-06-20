from ...base_foundation import place_rect_foundation, place_border, smooth_edges_gaussian
from ...building_module import build_module_global
from maps.blueprint import Blueprint
from random import choice
from typing import Union, Sequence
from gdpc import  Block
from gdpc.vector_tools import Rect
from pyglm.glm import ivec3

TILE_SIZE = ivec3(5,3,4)
MODULES = ["Decoration_Bench#0", "Decoration_Campfire#0", "Decoration_Flowerbed#0", "Decoration_Flowerbed#1"]

def build_decoration( blueprint: Blueprint, area: Rect,
                    foundation_block: Union[Block, Sequence[Block]] = Block("grass_block"), wood_type: str = "oak"):
    editor = blueprint.map_features.editor
    y = place_rect_foundation(blueprint, area, foundation_block)

    module = choice(MODULES)
    print(f"Building {module}.")
    if TILE_SIZE.x == area.size.x:
        rot = choice([0,2])
        tile_size = TILE_SIZE
    else:
        rot = choice([1,3])
        tile_size = ivec3(TILE_SIZE.z, TILE_SIZE.y, TILE_SIZE.x)

    build_area = editor.getBuildArea()
    build_module_global(editor, module, (build_area.offset.x + area.offset.x, y, build_area.offset.z + area.offset.y), tile_size, rot, wood_type)

    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area)
