from buildingModules.House.tile_rules import tile_rules, tile_directions, tile_weights, variation_weights
from base_foundation import placeRectFoundation
from wave_function_collapse import create_tile_array, wave_function_collapse
from build_roof import build_wooden_roof
from tile import *
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box

def build_wooden_house(editor: Editor, area: Rect, floors: int = 2, foundation_block: Union[Block, Sequence[Block]] = Block("stone_bricks"), wood_type: str = "oak"):
    y = placeRectFoundation(editor, area, foundation_block)
    house_area = Box((area.offset.x+1, y, area.offset.y+1),(area.offset.x+area.size.x-2, y+TILE_SIZE.y*(floors+1), area.offset.y+area.size.y-2))
    
    tile_array = create_tile_array(house_area, floors, tile_rules, tile_directions)
    tile_array = wave_function_collapse(tile_array, tile_weights, (1,0,0), ("House_Wood_GF_Door",0))
    
    for x in range(len(tile_array)):
        for y in range(len(tile_array[0])):
            for z in range(len(tile_array[0,0])):
                print(f"Pos: {tile_array[x,y,z].grid_pos}, Module: {tile_array[x,y,z].selected_module}")
                tile_array[x,y,z].build(editor,variation_weights)
    
    build_wooden_roof(editor, tile_array, wood_type)

    editor.flushBuffer()

editor = Editor(buffering=True)
area = Rect((0,0), (19, 15))
build_wooden_house(editor, area, floors=2)