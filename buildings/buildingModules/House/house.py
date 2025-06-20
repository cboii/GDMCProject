from .tile_rules import tile_rules, tile_directions, tile_weights, variation_weights, tile_quantity_limits, TILE_SIZE
from ...base_foundation import place_rect_foundation, clean_up_foundation, place_border, smooth_edges_gaussian
from ...plot_builder import PlotBuilder
from ...build_roof import build_wooden_roof, build_brick_roof
from ...plot_utils import get_entrance_direction, get_entrance_pos
from maps.blueprint import Blueprint
from typing import Union, Sequence
from gdpc import Block
from gdpc.vector_tools import Rect, Box
from random import choice

def build_wooden_house( blueprint: Blueprint, area: Rect, 
                        foundation_block: Union[Block, Sequence[Block]] = Block("stone_bricks"), wood_type: str = "oak"):
    print("Building a house.")
    editor = blueprint.map_features.editor
    #smooth_edges_gaussian(blueprint, area, sigma=5, max_width=10, include_area=True)
    y = place_rect_foundation(blueprint, area, foundation_block)
    house_area = Box((area.offset.x+1, y, area.offset.y+1),(area.size.x-2, y+TILE_SIZE.y*3, area.size.y-2))
    
    pb = PlotBuilder(house_area, 2, TILE_SIZE, tile_rules, tile_directions, tile_quantity_limits, tile_weights)
    pb.create_tile_array()

    entrance_rot = get_entrance_direction(area, blueprint.road_network)
    entrance_pos = get_entrance_pos(pb.tile_array, entrance_rot)
    pb.wfc(entrance_pos, ("House_Wood_GF_Door", entrance_rot))
    pb.build(editor, variation_weights, wood_type)

    roof_type = choice([0,1])
    match roof_type:
        case 0:
            build_wooden_roof(editor, pb.tile_array, TILE_SIZE, wood_type)
        case 1:
            build_brick_roof(editor, pb.tile_array, TILE_SIZE, wood_type)

    clean_up_foundation(blueprint, area, y, [])
    place_border(blueprint, area, y)
    smooth_edges_gaussian(blueprint, area)
