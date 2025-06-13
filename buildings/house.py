from .buildingModules.House.tile_rules import tile_rules, tile_directions, tile_weights, variation_weights, tile_quantity_limits, TILE_SIZE
from .base_foundation import place_rect_foundation, clean_up_foundation
from .plot_builder import PlotBuilder
from .build_roof import build_wooden_roof
from .tile import Tile
from .building_module import BuildingModule
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box
from random import choice

def build_wooden_house( editor: Editor, area: Rect, entrance_rotation: int,
                        foundation_block: Union[Block, Sequence[Block]] = Block("stone_bricks"), wood_type: str = "oak"):
    print("Building a house.")
    y = place_rect_foundation(editor, area, foundation_block)
    print(f"y: {y}")
    house_area = Box((area.offset.x+1, y, area.offset.y+1),(area.size.x-2, y+TILE_SIZE.y*3, area.size.y-2))
    
    pb = PlotBuilder(house_area, 2, TILE_SIZE, tile_rules, tile_directions, tile_quantity_limits, tile_weights)
    pb.create_tile_array()
    tile_array_shape = pb.tile_array.shape
    match entrance_rotation:
        case 0:
            entrance_pos = (choice(list(range(1,tile_array_shape[0]-1))),0,0)
        case 1:
            entrance_pos = (tile_array_shape[0]-1, 0, choice(list(range(1,tile_array_shape[2]-1))))
        case 2:
            entrance_pos = (choice(list(range(1,tile_array_shape[0]-1))),0,tile_array_shape[2]-1)
        case 3:
            entrance_pos = (0, 0, choice(list(range(1,tile_array_shape[2]-1))))
    pb.wfc(entrance_pos, ("House_Wood_GF_Door", entrance_rotation))
    pb.build(editor, variation_weights, wood_type)
    
    build_wooden_roof(editor, pb.tile_array, TILE_SIZE, wood_type)

    editor.flushBuffer()
    clean_up_foundation(editor, area, y, [])
    editor.flushBuffer()
