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
    y = int(np.median(height_map))
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
    bordered_area = Rect(area.offset - 2, area.size+4)
    for x,z in bordered_area:
        if blueprint.map[x,z] <= 35:
            placeCuboid(editor, (build_area.offset.x + x, ground-1, build_area.offset.z + z), (build_area.offset.x + x, ground-10, build_area.offset.z + z), block)
            placeCuboid(editor, (build_area.offset.x + x, ground, build_area.offset.z + z), (build_area.offset.x + x, ground+5, build_area.offset.z + z), Block("air"))

def smooth_edges_gaussian(blueprint: Blueprint, area: Rect, add: bool = True, sigma: float = 1, max_width: int = 25, include_area: bool = False, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    editor = blueprint.map_features.editor
    editor.flushBuffer()
    build_area = editor.getBuildArea()
    world_slice = editor.loadWorldSlice()
    height_map = np.zeros((build_area.size.x, build_area.size.z))
    for x in range(height_map.shape[0]):
        for z in range(height_map.shape[1]):
            if blueprint.map[x,z] in [0,35] or (include_area and Rect(area.offset, area.size).contains((x,z))):
                height_map[x,z] = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x,z]-1
            else:
                if x == 0 and z == 0:
                    height_map[x,z] = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x,z]-1
                elif x == 0:
                    height_map[x,z] = height_map[x,z-1]
                elif z == 0:
                    height_map[x,z] = height_map[x-1,z]
                else:
                    height_map[x,z] = np.floor(0.5*(height_map[x-1,z] + height_map[x,z-1]))
    height_map_gaussian = gaussian_filter(height_map, sigma=sigma)

    smooth_area = Rect(area.offset-max_width, area.size + 2* max_width)
    
    i = 1 if add else 0

    for x,z in smooth_area:
        if build_area.contains((build_area.offset.x + x, 60, build_area.offset.z + z)) and world_slice.getBlock((x,height_map[x,z]-1,z)).id != "minecraft:water":
            if include_area:
                if blueprint.map[x,z] <= 15 or Rect(area.offset-1, area.size+2).contains((x,z)):
                    placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+i, build_area.offset.z + z), block)
                    placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1+i, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+20, build_area.offset.z + z), Block("air"))
            else:
                if blueprint.map[x,z] <= 15 and not Rect(area.offset-2, area.size+4).contains((x,z)):
                    placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+i, build_area.offset.z + z), block)
                    placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1+i, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+20, build_area.offset.z + z), Block("air"))
                elif blueprint.map[x,z] <= 15 and not Rect(area.offset-1, area.size+2).contains((x,z)):
                    if height_map_gaussian[x,z] < height_map[area.offset.x-1,area.offset.y-1]:
                        placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+i, build_area.offset.z + z), block)
                        placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1+i, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+20, build_area.offset.z + z), Block("air"))
            if blueprint.map[x,z] == 200 and not area.contains((x,z)):
                placeCuboid(editor, (build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+i, build_area.offset.z + z), Block("cobblestone"))
                placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x,z]+1+i, build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x,z]+5, build_area.offset.z + z), Block("air"))

    editor.flushBuffer()
