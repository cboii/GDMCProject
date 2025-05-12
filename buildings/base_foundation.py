from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.vector_tools import Rect
import numpy as np
from typing import Sequence, Union

def placeRectFoundation(editor: Editor, area: Rect,
                        block: Union[Block, Sequence[Block]]) -> int:
    world_slice = editor.loadWorldSlice(area)
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    min_y = np.min(height_map)
    print(min_y)
    placeCuboid(editor, (area.offset.x, min_y-1, area.offset.y), (area.offset.x+area.size.x-1, min_y-3, area.offset.y+area.size.y-1), block)
    placeCuboid(editor, (area.offset.x, min_y, area.offset.y), (area.offset.x+area.size.x-1, min_y+20, area.offset.y+area.size.y-1), Block("air"))
    return min_y
