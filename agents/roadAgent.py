import numpy as np

from terrain.terrain_manipulator import TerrainManipulator
from .agentClass import Agent
from .plots import PlotType
import random
import numpy as np
from collections import deque

class RoadExtendorAgent(Agent):

    def __init__(self, blueprint, step_size = 32):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = 3
        self.max_slope = 1

        self.step_size = step_size
        area, begin = self.blueprint.get_town_center(step_size=step_size)
        end = [begin[0] + step_size - 1, begin[1] + step_size - 1]
        self.min_coords = begin
        self.max_coords = end


    def evaluate_location_fitness(self, loc):
        pass

    def place(self, loc):
        super().place(loc)
        pass



class RoadConnectorAgent(Agent):
    def __init__(self, blueprint):
        super().__init__(blueprint)
        self.type = PlotType.ROAD
        self.max_width = 3
        self.max_slope = 1

        self.terrain_manipulator = TerrainManipulator(self.blueprint)

    def connect_to_road_network(self, loc, execute = False):
        build_map = self.blueprint.map < 1
        build_map &= self.blueprint.steepness_map < 2
        path, dist = self.find_minimal_path_with_path(loc, self.blueprint.road_network, build_map)
        self.place(path)

        if execute:
            self.terrain_manipulator.place_road_segment(path)
        pass
    
    def place(self, loc):
        super().place(loc)
        pass

    def evaluate_location_fitness(self, loc):
        pass

    def find_minimal_path_with_path(self, rect_coords,
                           network: np.ndarray,
                           traversable: np.ndarray,
                           connectivity: int = 4) -> np.ndarray:
        
        if connectivity not in (4, 8):
            raise ValueError("connectivity must be 4 or 8")
        if network.ndim != 2 or traversable.ndim != 2:
            raise ValueError("network and traversable must be 2D arrays")
        if network.shape != traversable.shape:
            raise ValueError("network and traversable must have the same shape")

        h, w = network.shape

        coords = []
        for p in rect_coords:
            try:
                r, c = int(p[0]), int(p[1])
            except Exception:
                raise ValueError(f"Invalid coordinate format: {p}")
            if not (0 <= r < h and 0 <= c < w):
                raise ValueError(f"rect coord {(r, c)} out of bounds")
            coords.append((r, c))

        if not coords:
            raise ValueError("rect_coords must contain at least one coordinate")

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

        return np.argwhere(path_mask), len(np.argwhere(path_mask))

