from gdpc import Editor, Block
from gdpc.transform import rotatedBoxTransform
from gdpc.vector_tools import Box
from pyglm.glm import ivec3
import pickle
from pathlib import Path
from random import choice

ROTATION_CORNER_NE = 0
ROTATION_CORNER_SE = 1
ROTATION_CORNER_SW = 2
ROTATION_CORNER_NW = 3

ROTATION_N = 0
ROTATION_E = 1
ROTATION_S = 2
ROTATION_W = 3

FLOWER_VARIATIONS = ["dandelion", "poppy", "blue_orchid", "allium", 
                     "azure_bluet", "red_tulip", "orange_tulip", 
                     "white_tulip", "pink_tulip", "oxeye_daisy", 
                     "cornflower", "lily_of_the_valley"]

class BuildingModule:
    def __init__(self, name: str, blocks: dict = {}):
        self.name = name
        self.blocks = blocks

    def place_module(self, editor: Editor, start: ivec3, tile_size: ivec3, rotation: int):
        self.randomize_flowers()
        build_area = editor.getBuildArea()
        target_box = Box((build_area.offset.x + start.x, start.y, build_area.offset.z + start.z), tile_size)
        with editor.pushTransform(rotatedBoxTransform(target_box, rotation)):
            for coords, block in self.blocks.items():
                editor.placeBlock(coords, block)
            
    def place_module_global(self, editor: Editor, start: ivec3, tile_size: ivec3, rotation: int):
        self.randomize_flowers()
        target_box = Box(start, tile_size)
        with editor.pushTransform(rotatedBoxTransform(target_box, rotation)):
            for coords, block in self.blocks.items():
                editor.placeBlock(coords, block)

    def change_wood_type(self, type: str):
        for block in self.blocks.values():
            block.id = block.id.replace(":oak", f":{type}")
            block.id = block.id.replace(":stripped_oak", f":stripped_{type}")

    def randomize_flowers(self):
        for block in self.blocks.values():
            if block.id == "minecraft:dandelion":
                flower = choice(FLOWER_VARIATIONS)
                block.id = block.id.replace("dandelion", flower)
    

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
    module_class = name.split('_')[0]
    script_location = Path(__file__).absolute().parent
    file_location = script_location / f"buildingModules/{module_class}/tiles/{name}.pkl"
    with open(file_location, 'rb') as f:
        module = pickle.load(f)
    return module

def build_module(editor: Editor, name: str, start: ivec3, tile_size: ivec3, rotation: int, wood_type: str="oak"):
    module = get_module_from_pkl(name)
    module.change_wood_type(wood_type)
    module.place_module(editor, start, tile_size, rotation)

def build_module_global(editor: Editor, name: str, start: ivec3, tile_size: ivec3, rotation: int, wood_type: str="oak"):
    module = get_module_from_pkl(name)
    module.change_wood_type(wood_type)
    module.place_module_global(editor, start, tile_size, rotation)

def main():
    editor = Editor(buffering=True)
    
    name = "Decoration_Flowerbed#1"
    scan_module(editor, name)
    build_module_global(editor, name, (-78, -60, 32), (7,7,7), 0, "oak")
    
    #build_module_global(editor, "Misc_Smithy#0", (-94, -60, 11), (13,16,5), 0, "oak")
    #editor.flushBuffer()

if __name__ == "__main__":
    main()
