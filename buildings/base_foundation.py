from maps.blueprint import Blueprint
from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.vector_tools import Rect
import numpy as np
from typing import Sequence, Union
from pyglm.glm import ivec3, ivec2
from random import choices
from scipy.ndimage import gaussian_filter

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
    y = int(np.max(height_map))
    placeCuboid(editor, (build_area.offset.x + area.offset.x, y-2, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, y-5, build_area.offset.z + area.offset.y+area.size.y-1), Block("dirt"))
    placeCuboid(editor, (build_area.offset.x + area.offset.x, y-1, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, y-1, build_area.offset.z + area.offset.y+area.size.y-1), block)
    placeCuboid(editor, (build_area.offset.x + area.offset.x, y, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, y+30, build_area.offset.z + area.offset.y+area.size.y-1), Block("air"))
    return y

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

def place_border(blueprint: Blueprint, area: Rect, ground: int, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    editor = blueprint.map_features.editor
    build_area = editor.getBuildArea()
    bordered_area = Rect(area.offset - 1, area.size+2)
    for x,z in bordered_area:
        if blueprint.map[x,z] == 35:
            placeCuboid(editor, (build_area.offset.x + x, ground-1, build_area.offset.z + z), (build_area.offset.x + x, ground-10, build_area.offset.z + z), block)

def smooth_edges_gaussian(blueprint: Blueprint, area: Rect, sigma: float, max_width: int = 7, include_area: bool = False, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    editor = blueprint.map_features.editor
    editor.flushBuffer()
    build_area = editor.getBuildArea()
    world_slice = editor.loadWorldSlice()
    height_map = np.zeros((build_area.size.x, build_area.size.z))
    for x in range(height_map.shape[0]):
        for z in range(height_map.shape[1]):
            if blueprint.map[x,z] in [0,35] or (include_area and Rect(area.offset, area.size).contains((x,z))):
                height_map[x,z] = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x,z]
            else:
                if x == 0 and z == 0:
                    height_map[x,z] = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x,z]
                elif x == 0:
                    height_map[x,z] = height_map[x,z-1]
                elif z == 0:
                    height_map[x,z] = height_map[x-1,z]
                else:
                    height_map[x,z] = np.floor(0.5*(height_map[x-1,z] + height_map[x,z-1]))
    height_map_gaussian = gaussian_filter(height_map, sigma=sigma)

    smooth_area = Rect(area.offset-max_width, area.size + 2* max_width)
 
    for x,z in smooth_area:
        if build_area.contains((build_area.offset.x + x, 60, build_area.offset.z + z)) and world_slice.getBlock((x,height_map[x,z]-1,z)).id != "minecraft:water":
            if include_area:
                if blueprint.map[x,z] in [0,35] or Rect(area.offset-1, area.size+2).contains((x,z)):
                    placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z], build_area.offset.z + z), block)
                    placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+5, build_area.offset.z + z), Block("air"))
            else:
                if blueprint.map[x,z] in [0] and not Rect(area.offset, area.size).contains((x,z)):
                    placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z], build_area.offset.z + z), block)
                    placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+5, build_area.offset.z + z), Block("air"))
            if blueprint.map[x,z] == 200:
                placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z], build_area.offset.z + z), Block("cobblestone"))
                placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+5, build_area.offset.z + z), Block("air"))

    editor.flushBuffer()

"""
def smooth_edges(blueprint: Blueprint, area: Rect, border_blocks: list[ivec3], max_width: int = 5, max_height: int = 10,block: Union[Block, Sequence[Block]] = Block("grass_block")):
    world_slice = blueprint.map_features.editor.loadWorldSlice()
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    
    for coords in border_blocks:
        on_x_edge = 0
        on_z_edge = 0
        if coords.x < area.offset.x:
            smooth_step(blueprint, coords, max_width, max_height, (-1,0), height_map, block)
            on_x_edge = -1
        elif coords.x >= area.end.x:
            smooth_step(blueprint, coords, max_width, max_height, (1,0), height_map, block)
            on_x_edge = 1
        if coords.z < area.offset.y:
            smooth_step(blueprint, coords, max_width, max_height, (0,-1), height_map, block)
            on_z_edge = -1
        elif coords.z >= area.end.y:
            smooth_step(blueprint, coords, max_width, max_height, (0,1), height_map, block)
            on_z_edge = 1
        
        if on_x_edge != 0 and on_z_edge != 0:
            smooth_step(blueprint, coords, max_width, max_height, (on_x_edge,on_z_edge), height_map, block)

def smooth_step(blueprint: Blueprint, coords: ivec3, max_width: int, max_height: int, direction: tuple[int,int], height_map, block: Union[Block, Sequence[Block]]):
    editor = blueprint.map_features.editor
    build_area = editor.getBuildArea()
    print(f"in smooth_step, coords: {(build_area.offset.x + coords.x, coords.y, build_area.offset.z + coords.z)}, direction: {direction}")
    if max_width == 0 or max_height == 0:
        print("Return max w h")
        return
    if blueprint.map[coords.x,coords.z] not in [0,35]:
        print("Return obstacle")
        return
    if not editor.getBuildArea().contains((build_area.offset.x + coords.x, coords.y, build_area.offset.z + coords.z)):
        print("Return contains")
        return
    if coords.y - max_height > height_map[coords.x, coords.z]:
        print("Return height")
        return
    
    placeCuboid(editor, (build_area.offset.x + coords.x, coords.y, build_area.offset.z + coords.z), (build_area.offset.x + coords.x, coords.y-max_height, build_area.offset.z + coords.z), block)
    if editor.getBuildArea().contains((build_area.offset.x + coords.x + direction[0], coords.y, build_area.offset.z + coords.z + direction[1])):
        step_weights = [2/(max_height/max_width),(max_height/max_width), 0.1*(max_height/max_width)]
        step_down = 1
        if direction[0] != 0 and direction[1] != 0:
        
            if coords.y - height_map[coords.x + direction[0], coords.z + direction[1]] + 2 > 0:
                step_down_corner = choices([1,2],step_weights[1:])[0]
                smooth_step(blueprint, ivec3(coords.x + direction[0], coords.y-step_down_corner, coords.z + direction[1]), max_width-1, max_height-step_down_corner, direction, height_map, block)

            step_down = choices([0,1,2],step_weights)[0]
            smooth_step(blueprint, ivec3(coords.x + direction[0], coords.y-step_down, coords.z + 0), max_width-1, max_height-step_down, (direction[0], 0), height_map, block)
            step_down = choices([0,1,2],step_weights)[0]
            smooth_step(blueprint, ivec3(coords.x + 0, coords.y-step_down, coords.z + direction[1]), max_width-1, max_height-step_down, (0, direction[1]), height_map, block)
        else:
            if coords.y - height_map[coords.x + direction[0], coords.z + direction[1]] + 2 > 0:
                step_down = choices([0,1,2],step_weights)[0]
                smooth_step(blueprint, ivec3(coords.x + direction[0], coords.y-step_down, coords.z + direction[1]), max_width-1, max_height-step_down, direction, height_map, block)
"""

