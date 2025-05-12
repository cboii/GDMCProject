from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.transform import rotatedBoxTransform
from gdpc.vector_tools import Box
from tile import TILE_SIZE
from random import choice
from pyglm.glm import ivec3
import numpy.typing as npt

def build_wooden_roof(editor: Editor, tile_array: npt.NDArray[any], wood_type: str):

    for i in range(tile_array.shape[0]):
        for j in range(tile_array.shape[2]):
            name, rotation = tile_array[i][-1][j].selected_module
            if name.endswith("Corner") and rotation == 3:
                nw_corner_tile = tile_array[i][-1][j]
                break

    for i in range(tile_array.shape[0]-1,-1,-1):
        for j in range(tile_array.shape[2]-1,-1,-1):
            name, rotation = tile_array[i][-1][j].selected_module
            if name.endswith("Corner") and rotation == 1:
                se_corner_tile = tile_array[i][-1][j]
                break

    nw_corner_coordinate = ivec3(nw_corner_tile.pos.x, nw_corner_tile.pos.y + TILE_SIZE.y-1, nw_corner_tile.pos.z) 
    se_corner_coordinate = ivec3(se_corner_tile.pos.x + TILE_SIZE.x, se_corner_tile.pos.y + TILE_SIZE.y-1, se_corner_tile.pos.z + TILE_SIZE.z)

    eastwest_length = se_corner_coordinate.x - nw_corner_coordinate.x
    northsouth_length = se_corner_coordinate.z - nw_corner_coordinate.z

    if eastwest_length > northsouth_length:
        roof_direction = "eastwest"
    elif northsouth_length > eastwest_length:
        roof_direction = "northsouth"
    else: 
        roof_direction = choice(["eastwest", "northsouth"])
    
    if roof_direction == "northsouth":
        length = northsouth_length
        width = eastwest_length
        roof_rotation = 0
    else:
        length = eastwest_length
        width = northsouth_length
        roof_rotation = 1

    target_box = Box(nw_corner_coordinate, (eastwest_length, width//2+1, northsouth_length))
    with editor.pushTransform(rotatedBoxTransform(target_box, roof_rotation)):
        generic_wooden_roof(editor, length, width, wood_type)
     

def generic_wooden_roof(editor: Editor, length: int, width: int, wood_type: str):
    stairs_name = f"{wood_type}_stairs"
    planks_name = f"{wood_type}_planks"
    slab_name = f"{wood_type}_slab"
    log_name = f"{wood_type}_log"
    
    east_block = Block(stairs_name, {"facing": "east"})
    west_block = Block(stairs_name, {"facing": "west"})

    east_flipped_block = Block(stairs_name, {"facing": "west", "half": "top"})
    west_flipped_block = Block(stairs_name, {"facing": "east", "half": "top"})

    for i in range(width//2 + 1):
        placeCuboid(editor, (-1+i, i, -1), (-1+i, i, length), east_block)
        placeCuboid(editor, (width-i, i, -1), (width-i, i, length), west_block)
        
        if i < width//2:
            if i % 2 == 1:
                placeCuboid(editor, (i, 1, 0), (i,1+i,0), Block(planks_name))
                placeCuboid(editor, (width-1-i, 1, 0), (width-1-i,1+i,0), Block(planks_name))
                placeCuboid(editor, (i, 1, length-1), (i,1+i,length-1), Block(planks_name))
                placeCuboid(editor, (width-1-i, 1, length-1), (width-1-i,1+i,length-1), Block(planks_name))
            else:
                placeCuboid(editor, (i, 1, 0), (i,1+i,0), Block(log_name))
                placeCuboid(editor, (width-1-i, 1, 0), (width-1-i,1+i,0), Block(log_name))
                placeCuboid(editor, (i, 1, length-1), (i,1+i,length-1), Block(log_name))
                placeCuboid(editor, (width-1-i, 1, length-1), (width-1-i,1+i,length-1), Block(log_name))
            
            editor.placeBlock((i, i, -1), east_flipped_block)
            editor.placeBlock((width-1-i, i, -1), west_flipped_block)
            editor.placeBlock((i, i, length-1+1), east_flipped_block)
            editor.placeBlock((width-1-i, i, length-1+1), west_flipped_block)
        elif width % 2 == 1:
            placeCuboid(editor, (width//2, i, -1), (width//2, i, length-1+1), Block(planks_name))
            placeCuboid(editor, (width//2, i+1, -1), (width//2, i+1, length-1+1), Block(slab_name))
            placeCuboid(editor, (width//2, 1, 0), (width//2, i, 0), Block(log_name))
            placeCuboid(editor, (width//2, 1, length-1), (width//2, i, length-1), Block(log_name))
    