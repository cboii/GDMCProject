from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.transform import rotatedBoxTransform
from gdpc.vector_tools import Box
from random import choice
from pyglm.glm import ivec3
import numpy.typing as npt

def build_wooden_roof(editor: Editor, tile_array: npt.NDArray[any], tile_size: ivec3, wood_type: str):
    nw_corner_coordinate, se_corner_coordinate = find_corner_coordinates(editor, tile_array, tile_size)
    
    rot, length, width, x_length, z_length = get_roof_rotation(nw_corner_coordinate, se_corner_coordinate)
    

    target_box = Box(nw_corner_coordinate, (x_length, width//2+1, z_length))
    with editor.pushTransform(rotatedBoxTransform(target_box, rot)):
        generic_wooden_roof(editor, length, width, wood_type)

def build_brick_roof(editor: Editor, tile_array: npt.NDArray[any], tile_size: ivec3, wood_type: str):
    nw_corner_coordinate, se_corner_coordinate = find_corner_coordinates(editor, tile_array, tile_size)
    
    rot, length, width, x_length, z_length = get_roof_rotation(nw_corner_coordinate, se_corner_coordinate)
    

    target_box = Box(nw_corner_coordinate, (x_length, width//2+1, z_length))
    with editor.pushTransform(rotatedBoxTransform(target_box, rot)):
        generic_brick_roof(editor, length, width, wood_type)
        
def find_corner_coordinates(editor: Editor, tile_array: npt.NDArray[any], tile_size: ivec3):
    build_area = editor.getBuildArea()

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

    nw_corner_coordinate = ivec3(build_area.offset.x + nw_corner_tile.pos.x, nw_corner_tile.pos.y + tile_size.y-1, build_area.offset.z + nw_corner_tile.pos.z) 
    se_corner_coordinate = ivec3(build_area.offset.x + se_corner_tile.pos.x + tile_size.x, se_corner_tile.pos.y + tile_size.y-1, build_area.offset.z + se_corner_tile.pos.z + tile_size.z)
    
    return nw_corner_coordinate, se_corner_coordinate

def get_roof_rotation(nw_corner: ivec3, se_corner: ivec3):
    x_length = se_corner.x - nw_corner.x
    z_length = se_corner.z - nw_corner.z

    if x_length > z_length:
        roof_direction = "eastwest"
    elif z_length > x_length:
        roof_direction = "northsouth"
    else: 
        roof_direction = choice(["eastwest", "northsouth"])
    
    if roof_direction == "northsouth":
        length = z_length
        width = x_length
        return 0, length, width, x_length, z_length
    else:
        length = x_length
        width = z_length
        return 1, length, width, x_length, z_length


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
            placeCuboid(editor, (width//2, 1, 0), (width//2, i, 0), Block(planks_name))
            placeCuboid(editor, (width//2, 1, length-1), (width//2, i, length-1), Block(planks_name))

def generic_brick_roof(editor: Editor, length: int, width: int, wood_type: str):
    stairs_name = f"{wood_type}_stairs"
    planks_name = f"{wood_type}_planks"
    slab_name = f"{wood_type}_slab"
    log_name = f"{wood_type}_log"
    
    east_block = Block("brick_stairs", {"facing": "east"})
    west_block = Block("brick_stairs", {"facing": "west"})

    east_flipped_block = Block("brick_stairs", {"facing": "west", "half": "top"})
    west_flipped_block = Block("brick_stairs", {"facing": "east", "half": "top"})

    for i in range(width//2 + 1):
        placeCuboid(editor, (-1+i, i, -1), (-1+i, i, length), east_block)
        placeCuboid(editor, (width-i, i, -1), (width-i, i, length), west_block)
        
        if i < width//2:
            if i % 2 == 1:
                placeCuboid(editor, (i, 1, 0), (i,1+i,0), Block("white_concrete"))
                placeCuboid(editor, (width-1-i, 1, 0), (width-1-i,1+i,0), Block("white_concrete"))
                placeCuboid(editor, (i, 1, length-1), (i,1+i,length-1), Block("white_concrete"))
                placeCuboid(editor, (width-1-i, 1, length-1), (width-1-i,1+i,length-1), Block("white_concrete"))
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
            placeCuboid(editor, (width//2, i, -1), (width//2, i, length-1+1), Block("bricks"))
            placeCuboid(editor, (width//2, i+1, -1), (width//2, i+1, length-1+1), Block("brick_slab"))
            placeCuboid(editor, (width//2, 1, 0), (width//2, i, 0), Block("white_concrete"))
            placeCuboid(editor, (width//2, 1, length-1), (width//2, i, length-1), Block("white_concrete"))
    