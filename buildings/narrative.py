from maps.blueprint import Blueprint
from agents.plots import PlotType

from gdpc.vector_tools import Box
from pyglm.glm import ivec3
import numpy as np


def find_lecterns_in_plot_type(blueprint: Blueprint, plot_type: PlotType) -> list[ivec3]:
    match plot_type:
        case PlotType.TOWNHALL:
            possible_heights =  [1,6,11]
            blueprint_map = blueprint.town_hall
        case PlotType.HOUSE:
            possible_heights = [4]
            blueprint_map = blueprint.houses
        case _:
            return None
    
    editor = blueprint.map_features.editor
    build_area = editor.getBuildArea()
    search_coords = np.argwhere(blueprint_map)
    lectern_coords = []
    lectern_facing = []
    for x,z in search_coords:
        for y in possible_heights:
            block = editor.getBlockGlobal((build_area.offset.x + x, blueprint.plot_heights[x,z]+1+y, build_area.offset.z + z))
            if block.id == "minecraft:lectern":
                lectern_coords.append(ivec3(build_area.offset.x + x,blueprint.plot_heights[x,z]+1+y,build_area.offset.z + z))
                lectern_facing.append(block.states["facing"])
                
    return lectern_coords, lectern_facing
                

