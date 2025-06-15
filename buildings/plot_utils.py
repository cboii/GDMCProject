import numpy as np
from scipy import spatial
from gdpc.vector_tools import Rect
from pyglm.glm import ivec2
from random import choice

def find_nearest_road_block(road_map, point: ivec2) -> ivec2:
    road_coords = np.argwhere(road_map)
    _, index = spatial.KDTree(road_coords).query(list(point))
    return ivec2(road_coords[index][0], road_coords[index][1])

def get_entrance_direction(area: Rect, road_map) -> int:
    nearest_rb = find_nearest_road_block(road_map, area.center)
    if nearest_rb.y <= area.offset.y:
        if area.offset.y - nearest_rb.y < area.offset.x - nearest_rb.x:
            return 3
        elif area.offset.y - nearest_rb.y < nearest_rb.x - area.end.x:
            return 1
        else:
            return 0
    elif nearest_rb.y >= area.end.y:
        if nearest_rb.y - area.end.y < area.offset.x - nearest_rb.x:
            return 3
        elif nearest_rb.y - area.end.y < nearest_rb.x - area.end.x:
            return 1
        else:
            return 2
    else:
        if area.offset.x >= nearest_rb.x:
            return 3
        elif area.end.x <= nearest_rb.x:
            return 1

def get_entrance_direction_big_buildings(area: Rect, road_map, face_width: int) -> int:
    if area.size.x == face_width:
        face_side_horizontal = True
    else:
        face_side_horizontal = False

    nearest_rb = find_nearest_road_block(road_map, area.center)
    if face_side_horizontal:
        if area.center.y >= nearest_rb.y:
            return 0
        else:
            return 2
    else:
        if area.center.x >= nearest_rb.x:
            return 3
        else:
            return 1

def get_entrance_pos(tile_array: np.ndarray, entrance_rot: int):
    tile_array_shape = tile_array.shape
    match entrance_rot:
        case 0:
            entrance_pos = (choice(list(range(1,tile_array_shape[0]-1))),0,0)
        case 1:
            entrance_pos = (tile_array_shape[0]-1, 0, choice(list(range(1,tile_array_shape[2]-1))))
        case 2:
            entrance_pos = (choice(list(range(1,tile_array_shape[0]-1))),0,tile_array_shape[2]-1)
        case 3:
            entrance_pos = (0, 0, choice(list(range(1,tile_array_shape[2]-1))))
    return entrance_pos

def get_entrance_pos_fixed(tile_array: np.ndarray, entrance_rot: int, positions_on_entrance_axis: list):
    tile_array_shape = tile_array.shape
    match entrance_rot:
        case 0:
            entrance_pos = (positions_on_entrance_axis[0],0,0)
        case 1:
            entrance_pos = (tile_array_shape[0]-1, 0, positions_on_entrance_axis[1])
        case 2:
            entrance_pos = (positions_on_entrance_axis[2],0,tile_array_shape[2]-1)
        case 3:
            entrance_pos = (0, 0, positions_on_entrance_axis[3])
    return entrance_pos