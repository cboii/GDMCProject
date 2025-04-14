from gdpc import Editor, Block
from gdpc.geometry import placeCuboid

from typing import Sequence, Union

def clearAreaAbove(editor: Editor, length: int, width: int, height: int):
    placeCuboid(editor, (0, 1, 0), (length, height, width), Block("air"))

def placeRectFoundation(editor: Editor, length: int, width: int,
                        block: Union[Block, Sequence[Block]]):
    placeCuboid(editor, (0, 0, 0), (length, -5, width), block)
    clearAreaAbove(editor, length, width, 10)