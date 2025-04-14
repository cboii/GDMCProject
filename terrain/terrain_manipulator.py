from gdpc import Editor, Block
from maps.buildMaps import BuildMap
import numpy as np

class TerrainManipulator:
    def __init__(self, editor: Editor, build_map: BuildMap):
        self.editor = editor
        self.build_map = build_map

    def place_plateau_at_town_center(self, step_size=32, gaussian = False):
        _, pos = self.build_map.get_town_center(step_size=step_size, gaussian=gaussian)

        for x in range(pos[0], pos[0] + step_size):
            for z in range(pos[1], pos[1] + step_size):
                for y in range(5):
                    self.editor.placeBlock((self.build_map.map_features.build_area.offset.x + x, self.build_map.height_map[x,z] + y - 1, self.build_map.map_features.build_area.offset.z + z), Block("cobblestone"))