import numpy as np

from Error import CustomError
from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from .plots import PlotType
import random
import numpy as np
from collections import deque

class RoadExtendorAgent(Agent):

    def __init__(self, blueprint, search_area, max_width, max_slope):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = max_width
        self.max_slope = max_slope

        self.min_coords = search_area[0]
        self.max_coords = search_area[1]

    def place(self, loc):
        super().place(loc)
        pass



class RoadConnectorAgent(Agent):
    def __init__(self, blueprint, max_width, max_slope):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = max_width
        self.max_slope = max_slope

        self.terrain_manipulator = TerrainManipulator(self.blueprint)

    def connect_to_road_network(self, loc, execute = False):
        path, dist = self.find_minimal_path(loc, self.blueprint.road_network)
        if dist == None:
            raise CustomError("No optimal path found!")
        self.place(path)

        if execute:
            self.terrain_manipulator.place_road_segment(path)
        pass
    
    def place(self, loc):
        super().place(loc)
        pass

    def find_minimal_path(self, rect_coords,
                           network: np.ndarray,
                           connectivity: int = 8) -> np.ndarray:
        build_map = self.blueprint.map < 1
        build_map &= self.blueprint.steepness_map <= self.max_slope
        build_map &= ~(self.blueprint.ground_water_map != 255)
        traversable = build_map
        if connectivity not in (4, 8):
            raise CustomError("connectivity must be 4 or 8")
        if network.ndim != 2 or traversable.ndim != 2:
            raise CustomError("network and traversable must be 2D arrays")
        if network.shape != traversable.shape:
            raise CustomError("network and traversable must have the same shape")

        h, w = network.shape

        coords = []
        for p in rect_coords:
            try:
                r, c = int(p[0]), int(p[1])
            except Exception:
                raise CustomError(f"Invalid coordinate format: {p}")
            if not (0 <= r < h and 0 <= c < w):
                raise CustomError(f"rect coord {(r, c)} out of bounds")
            coords.append((r, c))

        if not coords:
            raise CustomError("rect_coords must contain at least one coordinate")

        rect = np.zeros_like(network, dtype=bool)
        for r, c in coords:
            rect[r, c] = True

        blocked = rect | ~traversable

        if connectivity == 4:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                        (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Initialize BFS
        starts = set(coords)
        visited = np.zeros_like(network, dtype=bool)
        prev = {}
        queue = deque()
        for pt in starts:
            visited[pt] = True
            queue.append(pt)

        # BFS search
        goal = None
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
                    prev[(nr, nc)] = (r, c)
                    if network[nr, nc]:
                        goal = (nr, nc)
                        queue.clear()
                        break
                    if not blocked[nr, nc]:
                        visited[nr, nc] = True
                        queue.append((nr, nc))
            if goal:
                break

        # Reconstruct
        path_mask = np.zeros_like(network, dtype=bool)
        if goal:
            cur = goal
            path_mask[cur] = True
            while cur not in starts:
                cur = prev[cur]
                path_mask[cur] = True
        else:
            return None, None

        return np.argwhere(path_mask), len(np.argwhere(path_mask))

