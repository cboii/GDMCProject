import numpy as np
from scipy import spatial
from gdpc.vector_tools import Rect
from pyglm.glm import ivec2

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