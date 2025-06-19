from ...base_foundation import place_rect_foundation, clean_up_foundation, place_border, smooth_edges_gaussian
from ...building_module import build_module_global
from maps.blueprint import Blueprint
from random import choice
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box
from pyglm.glm import ivec3, ivec2

TILE_SIZE = ivec3(7,7,7)
MODULES = ["Well_Small#0", "Well_Large#0"]

def build_well( blueprint: Blueprint, area: Rect,
                    foundation_block: Union[Block, Sequence[Block]] = Block("grass_block"), wood_type: str = "oak"):
    editor = blueprint.map_features.editor
    #smooth_edges_gaussian(blueprint, area, sigma=5, max_width=10, include_area=True)
    y = place_rect_foundation(editor, area, foundation_block)

    module = choice(MODULES)
    print(f"Building {module}.")
    rot = choice([0,1,2,3])

    build_area = editor.getBuildArea()
    build_module_global(editor, module, (build_area.offset.x + area.offset.x, y, build_area.offset.z + area.offset.y), TILE_SIZE, rot, wood_type)

    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area)
