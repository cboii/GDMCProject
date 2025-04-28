from gdpc import Editor, Block
from gdpc.transform import rotatedBoxTransform
from gdpc.vector_tools import Box
from pyglm.glm import ivec3
import pickle
from pathlib import Path

TILE_SIZE = ivec3(3,4,3)

ROTATION_CORNER_NE = 0
ROTATION_CORNER_SE = 1
ROTATION_CORNER_SW = 2
ROTATION_CORNER_NW = 3

ROTATION_N = 0
ROTATION_E = 1
ROTATION_S = 2
ROTATION_W = 3

class BuildingModule:
    def __init__(self, name: str, blocks: dict = {}):
        self.name = name
        self.blocks = blocks

    def place_module(self, editor: Editor, start: ivec3, rotation: int):
        build_area = editor.getBuildArea()
        target_box = Box(start+build_area.offset, TILE_SIZE)
        with editor.pushTransform(rotatedBoxTransform(target_box, rotation)):
            for coords, block in self.blocks.items():
                editor.placeBlock(coords, block)
            
    def place_module_global(self, editor: Editor, start: ivec3, rotation: int):
        target_box = Box(start, TILE_SIZE)
        with editor.pushTransform(rotatedBoxTransform(target_box, rotation)):
            for coords, block in self.blocks.items():
                editor.placeBlock(coords, block)
    

def scan_module(editor: Editor, name: str):
     
    build_area = editor.getBuildArea()

    module = BuildingModule(name)

    for x,y,z in build_area:
        module.blocks[(x-build_area.offset.x,y-build_area.offset.y,z-build_area.offset.z)] = editor.loadWorldSlice().getBlockGlobal((x,y,z))

    module_class = name.split('_')[0]
    script_location = Path(__file__).absolute().parent
    file_location = script_location / f"buildingModules/{module_class}/tiles/{name}.pkl"
    
    with open(file_location, 'wb') as f:
        pickle.dump(module, f)

def get_module_from_pkl(name: str):
    print(name)
    module_class = name.split('_')[0]
    script_location = Path(__file__).absolute().parent
    file_location = script_location / f"buildingModules/{module_class}/tiles/{name}.pkl"
    with open(file_location, 'rb') as f:
        module = pickle.load(f)
    return module

def build_module(editor: Editor, name: str, start: ivec3, rotation: int):
    module = get_module_from_pkl(name)

    module.place_module(editor, start, rotation)

def build_module_global(editor: Editor, name: str, start: ivec3, rotation: int):
    module = get_module_from_pkl(name)

    module.place_module_global(editor, start, rotation)

def main():
    editor = Editor()
    name = "HouseGroundFloorWood_Ceiling#3"
    scan_module(editor, name)
    build_module_global(editor, name, (-17,-60,-39), 0)

if __name__ == "__main__":
    main()
