from buildingModules.Church.tile_rules import tile_rules, tile_directions, tile_weights, variation_weights, tile_quantity_limits, TILE_SIZE
from base_foundation import place_rect_foundation, clean_up_foundation
from plot_builder import PlotBuilder
from tile import Tile
from building_module import BuildingModule
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box

def build_church(   editor: Editor, area: Rect, entrance_pos: tuple, entrance_rotation: int,
                    foundation_block: Union[Block, Sequence[Block]] = Block("stone_bricks"), wood_type: str = "oak"):
    print("Building a church.")
    y = place_rect_foundation(editor, area, foundation_block)
    house_area = Box((area.offset.x, y, area.offset.y),(area.size.x, y+TILE_SIZE.y*1, area.size.y))
    
    pb = PlotBuilder(house_area, 1, TILE_SIZE, tile_rules, tile_directions, tile_quantity_limits, tile_weights)
    pb.create_tile_array()
    pb.wfc(entrance_pos, ("Church_Tower", entrance_rotation))
    pb.build(editor, variation_weights, wood_type)

    editor.flushBuffer()
    clean_up_foundation(editor, area, y, exceptions=[])
    editor.flushBuffer()

editor = Editor(buffering=True)
place_rect_foundation(editor, Rect((0,0), (50, 50)) ,Block("grass_block"))
area = Rect((0,0), (15, 28))
build_church(editor, area, (0,0,0), 0, wood_type="spruce")