from gdpc import Editor, Block
from gdpc.vector_tools import Vec3iLike
from gdpc.transform import Transform
import pickle
from pathlib import Path

class BuildingModule:
    def __init__(self, name: str, blocks: dict = {}):
        self.name = name
        self.blocks = blocks

    def place_module(self, editor: Editor, start: Vec3iLike):
        build_area = editor.getBuildArea()

        with editor.pushTransform(Transform(translation=build_area.offset+start)):
            for coords, block in self.blocks.items():
                editor.placeBlock(coords, block)
            
    def place_module_global(self, editor: Editor, start: Vec3iLike):
        with editor.pushTransform(Transform(translation=start)):
            for coords, block in self.blocks.items():
                editor.placeBlock(coords, block)
    

def scan_module(editor: Editor, name: str):
     
    build_area = editor.getBuildArea()

    module = BuildingModule(name)

    for x,y,z in build_area:
        module.blocks[(x-build_area.offset.x,y-build_area.offset.y,z-build_area.offset.z)] = editor.loadWorldSlice().getBlockGlobal((x,y,z))

    script_location = Path(__file__).absolute().parent
    file_location = script_location / f"buildingModules/{name}.pkl"
    
    with open(file_location, 'wb') as f:
        pickle.dump(module, f)

def build_module(editor: Editor, name: str, start: Vec3iLike):
   
    script_location = Path(__file__).absolute().parent
    file_location = script_location / f"buildingModules/{name}.pkl"
    with open(file_location, 'rb') as f:
        module = pickle.load(f)

    module.place_module(editor, start)

def build_module_global(editor: Editor, name: str, start: Vec3iLike):
   
    script_location = Path(__file__).absolute().parent
    file_location = script_location / f"buildingModules/{name}.pkl"
    with open(file_location, 'rb') as f:
        module = pickle.load(f)

    module.place_module_global(editor, start)

def main():
    editor = Editor()
    name = "HouseGroundFloorWoodStairs"
    scan_module(editor, name)
    build_module(editor, name, (-17,-60,-39))

if __name__ == "__main__":
    main()
