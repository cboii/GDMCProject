from collections import deque
import heapq
import itertools
import numpy as np
from Error import CustomError
from  maps.blueprint import Blueprint


class BFS:
    @staticmethod
    def find_minimal_path_to_network_numeric(mask, start, end, connectivity=8, use_start=False):
        if connectivity not in [4, 8]:
            raise ValueError("Connectivity must be 4 or 8.")

        rows, cols = mask.shape
        queue = []
        visited = set()
        paths = []
        values = []
        counter = itertools.count()
        for coord in start:
            x_cord = int(coord[0])
            y_cord = int(coord[1])
            coord = (x_cord, y_cord)
            if use_start:
                heapq.heappush(queue, (0, next(counter), (coord, [coord])))
            else:
                heapq.heappush(queue, (0, next(counter), (coord, [])))

        if connectivity == 4:
            dr = [-1, 1, 0, 0]
            dc = [0, 0, -1, 1]
        else:
            dr = [0, 0, 1, -1, -1, -1, 1, 1]
            dc = [1, -1, 0, 0, -1, 1, -1, 1]

        terminate = False
        while queue and not terminate:
            value, c, (current_node, current_path) = heapq.heappop(queue)
            r, c = current_node
            if current_node in end:
                paths.append(current_path)
                values.append(value)
                terminate = True
                break
            if current_node in visited:
                    continue
            visited.add(current_node)
            # print(current_node)
            for i in range(len(dr)):
                neighbor_r, neighbor_c = r + dr[i], c + dc[i]
                neighbor_node = (neighbor_r, neighbor_c)
                if neighbor_node in visited:
                    continue
                if 0 <= neighbor_r < rows and 0 <= neighbor_c < cols and mask[neighbor_node] <= 1001:
                    heapq.heappush(queue, (value + mask[neighbor_node] + 1, next(counter), (neighbor_node, current_path + [neighbor_node])))
        try:
            min_value_path_index = np.argmin(values)
        except Exception:
            return None
        return paths[min_value_path_index]