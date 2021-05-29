
__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"


import sys

from src.grid import Grid, GridNode


class DijkstraPathfinding:

    def __init__(self, grid: Grid, main_window):
        self.grid = grid
        self.main_window = main_window

        self.MOVE_STRAIGHT_COST = 10
        self.MOVE_DIAGONAL_COST = 14

        self.open_list = []
        self.closed_list = []

    def find_path(self, start_node: GridNode, end_node: GridNode, show_steps: bool):
        """Finds shortest path between two nodes on a grid"""

        self.open_list = [start_node]
        self.closed_list = []

        # setting all costs to infinite
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                current_node = self.grid.cells[x][y]
                current_node.cost = sys.maxsize
                current_node.came_from_node = None

        start_node.cost = 0

        while len(self.open_list) > 0:
            current_node = self.get_lowest_cost_node(self.open_list)

            if current_node == end_node:
                self.calculate_path(current_node, show_steps)
                return

            self.open_list.remove(current_node)
            self.closed_list.append(current_node)

            if current_node.value != Grid.START:
                current_node.value = Grid.CHECKED

            # checking neighbours of the current node
            for neighbour in self.get_neighbours(current_node):
                neighbour_node = neighbour[0]
                move_cost = neighbour[1]

                if neighbour_node in self.closed_list:
                    continue
                if neighbour_node.is_barrier():
                    self.closed_list.append(neighbour_node)
                    continue

                path_cost = current_node.cost + move_cost

                if path_cost < neighbour_node.cost:
                    neighbour_node.cost = path_cost
                    neighbour_node.came_from_node = current_node

                    if not (neighbour_node in self.open_list):
                        neighbour_node.value = Grid.OPEN
                        self.open_list.append(neighbour_node)

            if show_steps:
                self.main_window.draw()

        return

    def get_neighbours(self, current_node: GridNode) -> list:
        """Returns a list of neighbour nodes and their entering cost from a given node"""

        neighbour_list = []

        # left side
        if current_node.x - 1 >= 0:
            # left
            neighbour_list.append([self.grid.cells[current_node.x - 1][current_node.y], self.MOVE_STRAIGHT_COST])

            # left down
            if current_node.y - 1 >= 0:
                neighbour_list.append([self.grid.cells[current_node.x - 1][current_node.y - 1],
                                       self.MOVE_DIAGONAL_COST])

                # left up
            if current_node.y + 1 < self.grid.height:
                neighbour_list.append([self.grid.cells[current_node.x - 1][current_node.y + 1],
                                       self.MOVE_DIAGONAL_COST])

        # right side
        if current_node.x + 1 < self.grid.width:
            # right
            neighbour_list.append([self.grid.cells[current_node.x + 1][current_node.y],
                                   self.MOVE_STRAIGHT_COST])

            # right down
            if current_node.y - 1 >= 0:
                neighbour_list.append([self.grid.cells[current_node.x + 1][current_node.y - 1],
                                       self.MOVE_DIAGONAL_COST])

                # right up
            if current_node.y + 1 < self.grid.height:
                neighbour_list.append([self.grid.cells[current_node.x + 1][current_node.y + 1],
                                       self.MOVE_DIAGONAL_COST])

        # down
        if current_node.y - 1 >= 0:
            neighbour_list.append([self.grid.cells[current_node.x][current_node.y - 1],
                                   self.MOVE_STRAIGHT_COST])

        # up
        if current_node.y + 1 < self.grid.height:
            neighbour_list.append([self.grid.cells[current_node.x][current_node.y + 1], self.MOVE_STRAIGHT_COST])

        return neighbour_list

    def calculate_path(self, end_node: GridNode, show_steps: bool):
        """Marks the path by checking previous nodes that the ending node came from"""

        end_node.value = Grid.TARGET
        current_node = end_node.came_from_node
        while current_node.came_from_node is not None:
            current_node.value = Grid.PATH
            current_node = current_node.came_from_node

            if show_steps:
                self.main_window.draw()

    def get_lowest_cost_node(self, node_list) -> GridNode:
        """Returns a node with lowest f cost"""

        return min(node_list, key=lambda node: node.cost)
