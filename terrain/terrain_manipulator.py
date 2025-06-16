from gdpc import Editor, Block, geometry, vector_tools
from maps.blueprint import Blueprint
import numpy as np
from buildings.base_foundation import smooth_edges_gaussian

class TerrainManipulator:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint

    def place_plateau_at_town_center(self, step_size=32, gaussian = False, radius=1):
        _, pos = self.blueprint.get_town_center(step_size=step_size, gaussian=gaussian, radius=radius)

        area_height = np.zeros((step_size, step_size), dtype=int)
        for x in range(pos[0], pos[0] + step_size):
            for z in range(pos[1], pos[1] + step_size):
                area_height[x - pos[0],z - pos[1]] = self.blueprint.height_map[x, z]

        max_height = np.max(area_height) + 1
        for x in range(pos[0], pos[0] + step_size):
            for z in range(pos[1], pos[1] + step_size):
                for y in range(max_height - area_height[x - pos[0],z - pos[1]]):
                    self.blueprint.map_features.editor.placeBlock((self.blueprint.map_features.build_area.offset.x + x, self.blueprint.height_map[x,z] + y - 1, self.blueprint.map_features.build_area.offset.z + z), Block("cobblestone"))

        
    def place_base(self, loc, w, h):

        area_height = np.zeros((w, h), dtype=int)
        for x in range(loc[0], loc[0] + w):
            for z in range(loc[1], loc[1] + h):
                area_height[x - loc[0],z - loc[1]] = self.blueprint.height_map[x, z]

        max_height = np.max(area_height) + 1
        for x in range(loc[0], loc[0] + w):
            for z in range(loc[1], loc[1] + h):
                for y in range(max_height - area_height[x - loc[0],z - loc[1]]):
                    self.blueprint.map_features.editor.placeBlock((self.blueprint.map_features.build_area.offset.x + x, self.blueprint.height_map[x,z] + y - 1, self.blueprint.map_features.build_area.offset.z + z), Block("cobblestone"))
        
        area = vector_tools.Rect((loc[0],loc[1]), (w,h))
        smooth_edges_gaussian(self.blueprint, area, sigma=7, max_width=15, include_area=True)

        
    def place_road_segment(self, loc):
        for l in loc:
            self.blueprint.map_features.editor.placeBlock((self.blueprint.map_features.build_area.offset.x + int(l[0]), self.blueprint.height_map[int(l[0]), int(l[1])] - 1, self.blueprint.map_features.build_area.offset.z + int(l[1])), Block("cobblestone"))
