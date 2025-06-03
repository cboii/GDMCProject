from buildingModules.Farm.tile_rules import tile_rules, tile_directions, tile_weights, variation_weights, tile_quantity_limits, TILE_SIZE
from base_foundation import place_rect_foundation, clean_up_foundation
from plot_builder import PlotBuilder
from build_roof import build_wooden_roof
from tile import Tile
from building_module import BuildingModule
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box

def build_farm( editor: Editor, area: Rect, entrance_pos: tuple, entrance_rotation: int,
                foundation_block: Union[Block, Sequence[Block]] = Block("oak_planks"), wood_type: str = "oak"):
    print("Building a farm.")
    y = place_rect_foundation(editor, area, foundation_block)
    house_area = Box((area.offset.x+1, y, area.offset.y+1),(area.size.x-2, y+TILE_SIZE.y*2, area.size.y-2))
    
    pb = PlotBuilder(house_area, 1, TILE_SIZE, tile_rules, tile_directions, tile_quantity_limits, tile_weights)
    pb.create_tile_array()
    pb.wfc(entrance_pos, ("Farm_Wood_Door", entrance_rotation))
    pb.build(editor, variation_weights, wood_type)
    
    build_wooden_roof(editor, pb.tile_array, wood_type)
    editor.flushBuffer()
    clean_up_foundation(editor, area, y, exceptions=["minecraft:spruce_trapdoor"])
    editor.flushBuffer()
