from gdpc import Editor, Block
from gdpc.geometry import placeCuboid

def removeTrees(editor: Editor):
    buildArea = editor.getBuildArea()
    world_slice = editor.loadWorldSlice()
    heightmap = world_slice.heightmaps["MOTION_BLOCKING"]
    blocks_for_removal = ["minecraft:air", "minecraft:vine", "minecraft:red_mushroom_block",
                          "minecraft:mushroom_stem", "minecraft:brown_mushroom_block", "minecraft:bamboo"]

    for x in range (0, buildArea.end.x - buildArea.offset.x):
        for z in range (0, buildArea.end.z - buildArea.offset.z):
            i = 1
            block = world_slice.getBlock((x, heightmap[x,z] - i, z)).id
            
            while block.endswith("log") or block.endswith("leaves") or block in blocks_for_removal:
                i += 1
                
                block = world_slice.getBlock((x, heightmap[x,z] - i, z)).id
            if i > 1:
                placeCuboid(editor,
                           (buildArea.offset.x + x, heightmap[x,z] - 1, buildArea.offset.z + z),      
                           (buildArea.offset.x + x, heightmap[x,z] - (i-1), buildArea.offset.z + z),
                           Block("air"))