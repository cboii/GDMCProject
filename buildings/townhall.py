from .buildingModules.TownHall.tile_rules import tile_rules, tile_directions, tile_weights, variation_weights, tile_quantity_limits, TILE_SIZE
from .base_foundation import place_rect_foundation, clean_up_foundation
from .plot_builder import PlotBuilder
from .tile import Tile
from .building_module import BuildingModule
from typing import Union, Sequence
from gdpc import Editor, Block
from gdpc.vector_tools import Rect, Box
from pyglm.glm import ivec3

def build_townhall( editor: Editor, area: Rect, entrance_pos: tuple, entrance_rotation: int,
                    foundation_block: Union[Block, Sequence[Block]] = Block("gravel"), wood_type: str = "oak"):
    print("Building a town hall.")
    y = place_rect_foundation(editor, area, foundation_block)
    if entrance_rotation % 2 != 0:
        tile_size = ivec3(TILE_SIZE.z, TILE_SIZE.y, TILE_SIZE.x)
    else:
        tile_size = TILE_SIZE
    house_area = Box((area.offset.x, y, area.offset.y),(area.size.x, y+tile_size.y*1, area.size.y))
    
    pb = PlotBuilder(house_area, 1, tile_size, tile_rules, tile_directions, tile_quantity_limits, tile_weights)
    pb.create_tile_array()
    pb.wfc(entrance_pos, ("TownHall_Front_Right", entrance_rotation))
    pb.build(editor, variation_weights, wood_type)

    editor.flushBuffer()
    #clean_up_foundation(editor, area, y, exceptions=[])
    #editor.flushBuffer()

