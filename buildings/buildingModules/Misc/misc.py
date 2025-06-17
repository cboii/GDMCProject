from ...base_foundation import place_rect_foundation, clean_up_foundation, place_border, smooth_edges_gaussian
from ...building_module import build_module_global
from ...plot_utils import get_entrance_direction_big_buildings
from maps.blueprint import Blueprint
from random import choice
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box
from pyglm.glm import ivec3, ivec2

tile_sizes = {"Smithy": ivec3(12,10,9)}

def build_misc( blueprint: Blueprint, name: str, area: Rect,
                    foundation_block: Union[Block, Sequence[Block]] = Block("grass_block"), wood_type: str = "oak"):
    editor = blueprint.map_features.editor
    #smooth_edges_gaussian(blueprint, area, sigma=5, max_width=10, include_area=True)
    y = place_rect_foundation(editor, area, foundation_block)
    tile_size = tile_sizes[name]
    print(f"Building {name}.")
    module = f"Misc_{name}#0"
    entrance_rotation = get_entrance_direction_big_buildings(area, blueprint.road_network, 12)
    if entrance_rotation % 2 != 0:
        tile_size = ivec3(tile_size.z, tile_size.y, tile_size.x)
    else:
        tile_size = tile_size

    build_area = editor.getBuildArea()
    build_module_global(editor, module, (build_area.offset.x + area.offset.x, y, build_area.offset.z + area.offset.y), tile_size, entrance_rotation, wood_type)

    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area)
    editor.flushBuffer()