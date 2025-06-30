from maps.blueprint import Blueprint
from agents.plots import PlotType

from gdpc.editor_tools import placeSign, placeLectern
from gdpc.minecraft_tools import bookData
from gdpc.vector_tools import Rect
from pyglm.glm import ivec3
import numpy as np
from random import choice


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

def find_lecterns_in_plot(blueprint: Blueprint, plot_area: Rect) -> list[ivec3]:

    match blueprint.map[plot_area.offset.x, plot_area.offset.y]:
        case 175:
            possible_heights =  [1,6,11]
        case 255:
            possible_heights = [4]
        case _:
            return None
    
    editor = blueprint.map_features.editor
    build_area = editor.getBuildArea()
    lectern_coords = []
    lectern_facing = []
    for x,z in plot_area:
        for y in possible_heights:
            block = editor.getBlockGlobal((build_area.offset.x + x, blueprint.plot_heights[x,z]+1+y, build_area.offset.z + z))
            if block.id == "minecraft:lectern":
                lectern_coords.append(ivec3(build_area.offset.x + x,blueprint.plot_heights[x,z]+1+y,build_area.offset.z + z))
                lectern_facing.append(block.states["facing"])
                
    return lectern_coords, lectern_facing

def find_wall_signs_in_plot(blueprint: Blueprint, plot_area: Rect) -> tuple[list[ivec3],list[ivec3],list[str]]:

    match blueprint.map[plot_area.offset.x, plot_area.offset.y]:
        case 255:
            possible_heights =  [1]
        case _:
            return None
    
    editor = blueprint.map_features.editor
    build_area = editor.getBuildArea()
    sign_coords = []
    sign_facing = []
    wood_type = []
    for x,z in plot_area:
        for y in possible_heights:
            block = editor.getBlockGlobal((build_area.offset.x + x, blueprint.plot_heights[x,z]+1+y, build_area.offset.z + z))
            if block.id.endswith("wall_sign"):
                sign_coords.append(ivec3(build_area.offset.x + x,blueprint.plot_heights[x,z]+1+y,build_area.offset.z + z))
                sign_facing.append(block.states["facing"])
                wood_type.append(block.id.split(":")[1].split("_")[0])
                
    return sign_coords, sign_facing, wood_type

def add_narrative(blueprint: Blueprint, story: dict):

    for i in range(len(story["houses_and_families"])):
        name = story["houses_and_families"][i]["family_name"]
        number = story["houses_and_families"][i]["house_number"]
        area = story["houses_and_families"][i]["location"]
        add_information_to_house(blueprint, area, number, name)
    
    add_chronicles_to_townhall(blueprint,story)


def add_information_to_house(blueprint: Blueprint, area: Rect, n: int, name: str):
    sign_coords, sign_facing, wood_type = find_wall_signs_in_plot(blueprint, area)
    editor = blueprint.map_features.editor
    placeSign(editor, sign_coords[0], wood_type[0], True, sign_facing[0], 0, 
              "===============", str(n), name, "===============", frontIsGlowing=True)
    
def add_chronicles_to_townhall(blueprint: Blueprint, story: dict):
    editor = blueprint.map_features.editor
    lectern_coords, lectern_facing = find_lecterns_in_plot_type(blueprint, PlotType.TOWNHALL)

    town_book = create_city_chronicles(blueprint, story)
    placeLectern(editor, lectern_coords[0], lectern_facing[0], town_book)

    for i in range(min(len(lectern_coords)-1, len(story["houses_and_families"]))):
        coords = lectern_coords[i+1]
        facing = lectern_facing[i+1]
        book = create_family_book(story["houses_and_families"][i])
        placeLectern(editor, coords, facing, book)

def create_city_chronicles(story):
    title = choice(["Our Village", "Our Town", "Town Chronicles"])
    text = story["settlement_story"]
    return bookData(text, title)

def create_family_book(story: dict) -> str:
    name = story["family_name"]
    house_number = story["house_number"]
    background = story["background"]

    titles = ["The Story of House [NAME]", "The [NAME]-Chronicles", "Family [NAME]", "House [NAME]", "About Family [NAME]", "Our History", "Who We are"]
    title = choice(titles).replace("[NAME]", f"{name}")
    authors = ["House [NAME]", "Family [NAME]", "The [NAME]s"]
    author = choice(authors).replace("[NAME]", f"{name}")
    title_color = choice(["§1", "§2", "§3", "§4", "§5", "§6", "§7", "§8", "§9", "§a", "§b", "§c", "§d"])
    text = f"§l================\n§r {title_color}{title} \n§r House Number {house_number}\n §r §l================\f §r {background}"
    return bookData(text, title, author)
