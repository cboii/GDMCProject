from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.vector_tools import Rect
import numpy as np
from typing import Sequence, Union

def place_rect_foundation(editor: Editor, area: Rect,
                        block: Union[Block, Sequence[Block]]) -> int:
    print("Building foundation.")
    world_slice = editor.loadWorldSlice(area)
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    min_y = np.min(height_map)
    placeCuboid(editor, (area.offset.x, min_y-1, area.offset.y), (area.offset.x+area.size.x-1, min_y-3, area.offset.y+area.size.y-1), block)
    placeCuboid(editor, (area.offset.x, min_y, area.offset.y), (area.offset.x+area.size.x-1, min_y+30, area.offset.y+area.size.y-1), Block("air"))
    return min_y

def clean_up_foundation(editor: Editor, area: Rect, ground: int, exceptions: list, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    print("Cleaning up foundation.")
    world_slice = editor.loadWorldSlice(area)
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    for x,z in np.argwhere(height_map <= ground+1):
        if height_map[x,z] == ground or (editor.getBlockGlobal((area.offset.x + x, ground, area.offset.y + z)).id in exceptions):
            editor.placeBlock((x,ground-1,z), block)
