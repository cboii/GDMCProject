from collections import deque
import heapq
import numpy as np
from Error import CustomError
from  maps.blueprint import Blueprint


class BFS:
    @staticmethod
    def find_minimal_path_to_network_boolean(traversable, rect_coords, 
                           network: np.ndarray,
                           connectivity: int = 8) -> np.ndarray:
        if connectivity not in [4, 8]:
            raise ValueError("Connectivity must be 4 or 8.")

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
            return None

        return np.argwhere(path_mask)
    
    @staticmethod
    def is_valid(mask, r, c):
        rows, cols = mask.shape
        return 0 <= r < rows and 0 <= c < cols and mask[r, c]

    @staticmethod
    def find_minimal_path_to_point(mask, start, end, connectivity=8):
        if connectivity not in [4, 8]:
            raise ValueError("Connectivity must be 4 or 8.")

        rows, cols = mask.shape
        queue = deque([(start, [start])])
        visited = set([start])

        if connectivity == 4:
            dr = [-1, 1, 0, 0]
            dc = [0, 0, -1, 1]
        else:
            dr = [-1, -1, -1, 0, 0, 1, 1, 1]
            dc = [-1, 0, 1, -1, 1, -1, 0, 1]

        while queue:
            current_node, current_path = queue.popleft()

            if current_node == end:
                return current_path

            r, c = current_node

            for i in range(len(dr)):
                neighbor_r, neighbor_c = r + dr[i], c + dc[i]
                neighbor_node = (neighbor_r, neighbor_c)

                if neighbor_node in visited:
                    continue

                if BFS.is_valid(mask, neighbor_r, neighbor_c) and neighbor_node not in visited:
                    visited.add(neighbor_node)
                    queue.append((neighbor_node, current_path + [neighbor_node]))

        return None
    
    @staticmethod
    def find_minimal_path_to_network_numeric(mask, start, end, connectivity=8, use_start=False):
        if connectivity not in [4, 8]:
            raise ValueError("Connectivity must be 4 or 8.")

        rows, cols = mask.shape
        queue = []
        visited = set()
        paths = []
        values = []
        for coord in start:
            x_cord = int(coord[0])
            y_cord = int(coord[1])
            coord = (x_cord, y_cord)
            if use_start:
                heapq.heappush(queue, (0, (coord, [coord])))
            else:
                heapq.heappush(queue, (0, (coord, [])))
            visited.add(coord)

        if connectivity == 4:
            dr = [-1, 1, 0, 0]
            dc = [0, 0, -1, 1]
        else:
            dr = [0, 1, -1, 0, -1, -1, 1, 1]
            dc = [1, 0, 0, -1, -1, 1, -1, 1]

        terminate = False
        while queue and not terminate:
            value, (current_node, current_path) = heapq.heappop(queue)
            r, c = current_node

            for i in range(len(dr)):
                neighbor_r, neighbor_c = r + dr[i], c + dc[i]
                neighbor_node = (neighbor_r, neighbor_c)
                if neighbor_node in visited:
                    continue
                elif 0 <= neighbor_r < rows and 0 <= neighbor_c < cols and neighbor_node not in end and mask[neighbor_node] <= 1000:
                    visited.add(neighbor_node)
                    heapq.heappush(queue, (value + mask[neighbor_node], (neighbor_node, current_path + [neighbor_node])))
                elif neighbor_node in end and 0 <= neighbor_r < rows and 0 <= neighbor_c < cols:
                    visited.add(neighbor_node)
                    paths.append(current_path + [neighbor_node])
                    values.append(value + mask[neighbor_node])
                    terminate = True


        try:
            min_value_path_index = np.argmin(values)
        except Exception:
            return None
        return paths[min_value_path_index]