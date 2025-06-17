from gdpc.editor import Editor
from gdpc.geometry import placeCuboid
from gdpc.block import Block

editor = Editor(buffering=True)
build_area = editor.getBuildArea()
placeCuboid(editor, build_area.offset, build_area.offset + build_area.size, Block('air'))