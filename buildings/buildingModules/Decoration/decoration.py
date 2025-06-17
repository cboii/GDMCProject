from .tile_sizes import tile_sizes
from ...base_foundation import place_rect_foundation, clean_up_foundation, place_border, smooth_edges_gaussian
from ...building_module import build_module
from maps.blueprint import Blueprint
from random import choice
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box
from pyglm.glm import ivec3, ivec2

def build_decoration( blueprint: Blueprint, area: Rect,
                    foundation_block: Union[Block, Sequence[Block]] = Block("grass_block"), wood_type: str = "oak"):
    editor = blueprint.map_features.editor
    #smooth_edges_gaussian(blueprint, area, sigma=5, max_width=10, include_area=True)
    y = place_rect_foundation(editor, area, foundation_block)

    possible_modules = []
    for b, ts in tile_sizes.items():
        if area.size == ivec2(ts.x, ts.z) or area.size == ivec2(ts.z, ts.x):
            possible_modules.append(b)
    module = choice(possible_modules)
    print(f"Building {module}.")
    tile_size = tile_sizes[module]
    if tile_size.x == tile_size.z:
        rot = choice([0,1,2,3])
    elif tile_size.x == area.size.x:
        rot = choice([0,2])
    else:
        rot = choice([1,3])

    build_module(editor, module, (area.offset.x, y, area.offset.y), tile_size, rot, wood_type)

    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area, sigma=7)
    editor.flushBuffer()
