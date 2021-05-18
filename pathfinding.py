import sys

from grid import Grid, GridNode


class PathFinding:

    def __init__(self, grid: Grid, main_window):
        self.grid = grid
        self.main_window = main_window

        self.MOVE_STRAIGHT_COST = 10
        self.MOVE_DIAGONAL_COST = 14

        self.open_list = []
        self.closed_list = []

    def find_path(self, start_node: GridNode, end_node: GridNode, show_steps: bool):

        self.open_list = [start_node]
        self.closed_list = []

        # setting all g costs to infinite
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                current_node = self.grid.cells[x][y]
                current_node.g_cost = sys.maxsize
                current_node.calculate_f_cost()
                current_node.came_from_node = None

        start_node.g_cost = 0
        start_node.h_cost = self.calculate_distance_cost(start_node, end_node)
        start_node.calculate_f_cost()

        while len(self.open_list) > 0:
            # always checks the nodes with lowest f cost from the open list
            current_node = self.get_lowest_f_cost_node(self.open_list)

            if current_node == end_node:
                return self.calculate_path(end_node, show_steps)

            self.open_list.remove(current_node)
            self.closed_list.append(current_node)

            if current_node.value != Grid.START:
                current_node.value = Grid.CHECKED

            # checking neighbours of the current node
            for neighbour_node in self.get_neighbours(current_node):
                if neighbour_node in self.closed_list:
                    continue
                if neighbour_node.is_barrier():
                    self.closed_list.append(neighbour_node)
                    continue

                path_g_cost = current_node.g_cost + self.calculate_distance_cost(current_node, neighbour_node)

                if path_g_cost < neighbour_node.g_cost:
                    neighbour_node.came_from_node = current_node
                    neighbour_node.g_cost = path_g_cost
                    neighbour_node.h_cost = self.calculate_distance_cost(neighbour_node, end_node)
                    neighbour_node.calculate_f_cost()

                    if not (neighbour_node in self.open_list):
                        neighbour_node.value = Grid.OPEN
                        self.open_list.append(neighbour_node)

            if show_steps:
                self.main_window.draw()

        # if while exits the open list is out of nodes - no path exists
        return None

    def get_neighbours(self, current_node) -> list:
        neighbour_list = []

        # left side
        if current_node.x - 1 >= 0:
            # left
            neighbour_list.append(self.grid.cells[current_node.x - 1][current_node.y])

            # left down
            if current_node.y - 1 >= 0:
                neighbour_list.append(self.grid.cells[current_node.x - 1][current_node.y - 1])

            # left up
            if current_node.y + 1 < self.grid.height:
                neighbour_list.append(self.grid.cells[current_node.x - 1][current_node.y + 1])

        # right side
        if current_node.x + 1 < self.grid.width:
            # right
            neighbour_list.append(self.grid.cells[current_node.x + 1][current_node.y])

            # right down
            if current_node.y - 1 >= 0:
                neighbour_list.append(self.grid.cells[current_node.x + 1][current_node.y - 1])

            # right up
            if current_node.y + 1 < self.grid.height:
                neighbour_list.append(self.grid.cells[current_node.x + 1][current_node.y + 1])

        # down
        if current_node.y - 1 >= 0:
            neighbour_list.append(self.grid.cells[current_node.x][current_node.y - 1])

        # up
        if current_node.y + 1 < self.grid.height:
            neighbour_list.append(self.grid.cells[current_node.x][current_node.y + 1])

        return neighbour_list

    def calculate_path(self, end_node: GridNode, show_steps: bool) -> list:
        path = [end_node]
        end_node.value = Grid.TARGET
        current_node = end_node.came_from_node
        while current_node.came_from_node is not None:
            path.append(current_node)
            current_node.value = Grid.PATH
            current_node = current_node.came_from_node

            if show_steps:
                self.main_window.draw()

        path.append(current_node)

        # path.reverse()

        return path

    def calculate_distance_cost(self, grid_node_a: GridNode, grid_node_b: GridNode) -> int:
        x_distance = abs(grid_node_a.x - grid_node_b.x)
        y_distance = abs(grid_node_a.y - grid_node_b.y)

        distance = abs(x_distance - y_distance)

        return self.MOVE_DIAGONAL_COST * min(x_distance, y_distance) + self.MOVE_STRAIGHT_COST * distance

    def get_lowest_f_cost_node(self, node_list) -> GridNode:
        return min(node_list, key=lambda node: node.f_cost)
