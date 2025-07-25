from maps.blueprint import Blueprint
from gdpc import Editor, Block
from gdpc.geometry import placeCuboid
from gdpc.vector_tools import Rect
import numpy as np
from typing import Sequence, Union
from pyglm.glm import ivec3, ivec2
from random import choice, random
from scipy.ndimage import gaussian_filter

def place_rect_foundation(blueprint: Blueprint, area: Rect,
                        block: Union[Block, Sequence[Block]]) -> int:
    print("Building foundation.")
    editor = blueprint.map_features.editor
    editor.flushBuffer()
    build_area = editor.getBuildArea()
    ws_rect = Rect((build_area.offset.x + area.offset.x, build_area.offset.z + area.offset.y), area.size)
    world_slice = editor.loadWorldSlice(ws_rect)
    height_map = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    y = int(np.median(height_map))
    placeCuboid(editor, (build_area.offset.x + area.offset.x, y-2, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, y-5, build_area.offset.z + area.offset.y+area.size.y-1), Block("dirt"))
    placeCuboid(editor, (build_area.offset.x + area.offset.x, y-1, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, y-1, build_area.offset.z + area.offset.y+area.size.y-1), block)
    placeCuboid(editor, (build_area.offset.x + area.offset.x, y, build_area.offset.z + area.offset.y), (build_area.offset.x + area.offset.x+area.size.x-1, y+30, build_area.offset.z + area.offset.y+area.size.y-1), Block("air"))
    blueprint.set_plot_height(area, y-1)
    return y

def clean_up_foundation(blueprint: Blueprint, area: Rect, ground: int, exceptions: list, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    print("Cleaning up foundation.")
    editor = blueprint.map_features.editor
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

def smooth_edges_gaussian(blueprint: Blueprint, area: Rect, add: bool = True, sigma: float = 1, max_width: int = 15, include_area: bool = False, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    editor = blueprint.map_features.editor
    # editor.flushBuffer()
    build_area = editor.getBuildArea()
    world_slice = editor.loadWorldSlice()
    smooth_area_start = ivec2(max(0, area.offset.x - max_width), max(0, area.offset.y - max_width))
    smooth_area_end = ivec2(min(build_area.size.x, area.last.x + max_width), min(build_area.size.z, area.last.y+max_width))
    smooth_area = Rect(smooth_area_start, smooth_area_end-smooth_area_start)
    height_map = np.zeros((smooth_area.size.x, smooth_area.size.y))
    for x in range(0, smooth_area.size.x):
        x_map = smooth_area.offset.x + x
        for z in range(0, smooth_area.size.y):
            z_map = smooth_area.offset.y + z
            if blueprint.map[x_map,z_map] in [0, 15, 35, 200] or (include_area and area.contains((x_map,z_map))):
                height_map[x,z] = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x_map,z_map]-1
            elif not area.contains((x_map,z_map)):
                height_map[x,z] = blueprint.plot_heights[x_map, z_map]
            else:
                if x == 0 and z == 0:
                    height_map[x,z] = world_slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][x_map,z_map]-1
                elif x == 0:
                    height_map[x,z] = height_map[x,z-1]
                elif z == 0:
                    height_map[x,z] = height_map[x-1,z]
                else:
                    height_map[x,z] = np.floor(0.5*(height_map[x-1,z] + height_map[x,z-1]))
    height_map_gaussian = gaussian_filter(height_map, sigma=sigma)
    
    i = 1 if add else 0
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    for x,z in smooth_area:
        if build_area.contains((build_area.offset.x + x, 60, build_area.offset.z + z)) and blueprint.ground_water_map[x,z] != 0:
            if include_area:
                if blueprint.map[x,z] <= 15 or Rect(area.offset-2, area.size+4).contains((x,z)):
                    place_smoothed_blocks(editor, build_area, x, z, smooth_area.offset, height_map, height_map_gaussian, add, block)
            else:
                if blueprint.map[x,z] <= 15:
                    place_smoothed_blocks(editor, build_area, x, z, smooth_area.offset, height_map, height_map_gaussian, add, block)
                elif blueprint.map[x,z] == 35:
                    inner_ring = False
                    for i,j in directions:
                        if blueprint.map[x+i,z+j] > 35 and blueprint.map[x+i,z+j] != 200:
                            inner_ring = True
                            break
                    if not inner_ring:
                        place_smoothed_blocks(editor, build_area, x, z, smooth_area.offset, height_map, height_map_gaussian, add, block)
            if blueprint.map[x,z] == 200:
                road_blocks = 3*[Block("cobblestone")] + [Block("gravel"), Block("andesite"), Block("stone")]
                place_smoothed_blocks(editor, build_area, x, z, smooth_area.offset, height_map, height_map_gaussian, add, choice(road_blocks))

def place_smoothed_blocks(editor: Editor, build_area, x: int, z: int, area_start: ivec2, height_map, height_map_gaussian, add: bool, block: Union[Block, Sequence[Block]] = Block("grass_block")):
    
    x_map = x - area_start.x
    z_map = z - area_start.y
    i = 1 if add else 0
    if abs(height_map[x_map,z_map] - height_map_gaussian[x_map,z_map]) > 4:
        return
    placeCuboid(editor, (build_area.offset.x + x, height_map[x_map,z_map], build_area.offset.z + z), (build_area.offset.x + x, height_map_gaussian[x_map,z_map]+i, build_area.offset.z + z), block)
    if height_map[x_map,z_map] > height_map_gaussian[x_map,z_map]+i:
        placeCuboid(editor, (build_area.offset.x + x, height_map_gaussian[x_map,z_map]+1+i, build_area.offset.z + z), (build_area.offset.x + x, height_map[x_map,z_map], build_area.offset.z + z), Block("air"))

def place_foliage(blueprint: Blueprint, area: Rect, prob: float = 0.1):
    foliage = 50*[Block("short_grass")] + [Block("red_tulip"), Block("orange_tulip"), Block("white_tulip"), Block("pink_tulip"), Block("dandelion"), Block("poppy"),
                                           Block("blue_orchid"), Block("azure_bluet"), Block("cornflower"), Block("oxeye_daisy"), Block("lily_of_the_valley"),
                                           Block("rose_bush"), Block("lilac"), Block("peony"), Block("sunflower"), Block("tall_grass")]
    editor = blueprint.map_features.editor
    world_slice = blueprint.map_features.world_slice
    build_area = blueprint.map_features.build_area
    height_map = blueprint.height_map
    for x,z in np.argwhere(blueprint.map == 0):
        if random() > prob or not area.contains((x,z)) or not world_slice.getBlock((x,height_map[x,z]-1,z)).id == "minecraft:grass_block":
            continue
        else:
            editor.placeBlock((build_area.offset.x + x, height_map[x,z], build_area.offset.z + z), choice(foliage))