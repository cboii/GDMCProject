from .tile_rules import tile_rules, tile_directions, tile_weights, variation_weights, tile_quantity_limits, TILE_SIZE
from ...base_foundation import place_rect_foundation, clean_up_foundation, place_border, smooth_edges_gaussian
from ...plot_utils import get_entrance_direction_big_buildings, get_entrance_pos_fixed
from ...plot_builder import PlotBuilder
from maps.blueprint import Blueprint
from typing import Union, Sequence
from gdpc import Block
from gdpc.vector_tools import Rect, Box
from pyglm.glm import ivec3

def build_church(   blueprint: Blueprint, area: Rect,
                    foundation_block: Union[Block, Sequence[Block]] = Block("stone_bricks"), wood_type: str = "oak"):
    print("Building a church.")
    editor = blueprint.map_features.editor
    y = place_rect_foundation(blueprint, area, foundation_block)
    entrance_rotation = get_entrance_direction_big_buildings(area, blueprint.road_network, 13)
    if entrance_rotation % 2 != 0:
        tile_size = ivec3(TILE_SIZE.z, TILE_SIZE.y, TILE_SIZE.x)
    else:
        tile_size = TILE_SIZE
    house_area = Box((area.offset.x, y, area.offset.y),(area.size.x, y+tile_size.y*1, area.size.y))
    
    pb = PlotBuilder(house_area, 1, tile_size, tile_rules, tile_directions, tile_quantity_limits, tile_weights)
    pb.create_tile_array()
    entrance_pos = get_entrance_pos_fixed(pb.tile_array, entrance_rotation, [0,0,0,0])
    pb.wfc(entrance_pos, ("Church_Tower", entrance_rotation))
    pb.build(editor, variation_weights, wood_type)

    clean_up_foundation(blueprint, area, y, exceptions=[])
    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area, sigma=3)

