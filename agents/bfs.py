from collections import deque
import heapq
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
            dr = [-1, -1, -1, 0, 0, 1, 1, 1]
            dc = [-1, 0, 1, -1, 1, -1, 0, 1]

        terminate = False
        while queue and not terminate:
            value, (current_node, current_path) = heapq.heappop(queue)
            r, c = current_node

            for i in range(len(dr)):
                neighbor_r, neighbor_c = r + dr[i], c + dc[i]
                neighbor_node = (neighbor_r, neighbor_c)
                if neighbor_node in visited:
                    continue
                elif 0 <= neighbor_r < rows and 0 <= neighbor_c < cols and neighbor_node not in end and mask[neighbor_node] <= 1001:
                    visited.add(neighbor_node)
                    heapq.heappush(queue, (value + mask[neighbor_node] + 1, (neighbor_node, current_path + [neighbor_node])))
                elif neighbor_node in end and 0 <= neighbor_r < rows and 0 <= neighbor_c < cols:
                    visited.add(neighbor_node)
                    paths.append(current_path + [neighbor_node])
                    values.append(value + mask[neighbor_node] + 1)
                    terminate = True


        try:
            min_value_path_index = np.argmin(values)
        except Exception:
            return None
        return paths[min_value_path_index]