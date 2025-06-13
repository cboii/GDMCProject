from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.vector_tools import Rect
import numpy as np
from typing import Sequence, Union

def place_rect_foundation(editor: Editor, area: Rect,
                        block: Union[Block, Sequence[Block]]) -> int:
    print("Building foundation.")
    editor.flushBuffer()
    build_area = editor.getBuildArea()
    ws_rect = Rect((build_area.offset.x + area.offset.x, build_area.offset.z + area.offset.y), area.size)
    print(ws_rect)
    world_slice = editor.loadWorldSlice(ws_rect)
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    print(height_map)
    min_y = np.min(height_map)
    placeCuboid(editor, (build_area.offset.x + area.offset.x, min_y-1, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, min_y-3, build_area.offset.z + area.offset.y+area.size.y-1), block)
    placeCuboid(editor, (build_area.offset.x + area.offset.x, min_y, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, min_y+30, build_area.offset.z + area.offset.y+area.size.y-1), Block("air"))
    return min_y

def clean_up_foundation(editor: Editor, area: Rect, ground: int, exceptions: list, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    print("Cleaning up foundation.")
    editor.flushBuffer()
    build_area = editor.getBuildArea()
    ws_rect = Rect((build_area.offset.x + area.offset.x, build_area.offset.z + area.offset.y), area.size)
    world_slice = editor.loadWorldSlice(ws_rect)
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    for x,z in np.argwhere(height_map <= ground+1):
        if height_map[x,z] == ground or (editor.getBlockGlobal((build_area.offset.x + area.offset.x + x, ground, build_area.offset.z + area.offset.y + z)).id in exceptions):
            editor.placeBlock((build_area.offset.x + area.offset.x + x,ground-1,build_area.offset.z + area.offset.y + z), block)
