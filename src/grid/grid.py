__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"

import pygame
from src.gui import colors


class GridNode:

    def __init__(self, value: int, x: int, y: int):
        self.value = value
        self.x = x
        self.y = y
        self.came_from_node = None

        # A*
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

        # Dijkstra
        self.cost = 0

    def calculate_f_cost(self):
        """Calculates the sum of g cost and h cost"""
        self.f_cost = self.g_cost + self.h_cost

    def is_empty(self) -> bool:
        """Checks if a node is empty"""
        return self.value == Grid.EMPTY

    def is_barrier(self) -> bool:
        """Checks if a node is a barrier"""
        return self.value == Grid.BARRIER

    def is_target(self) -> bool:
        """Checks if a node is a target"""
        return self.value == Grid.TARGET

    def is_start(self) -> bool:
        """Checks if a node is a start"""
        return self.value == Grid.START

    def is_path(self) -> bool:
        """Checks if a node is a path"""
        return self.value == Grid.PATH

    def is_checked(self) -> bool:
        """Checks if a node is checked by a pathfinding algorithm"""
        return self.value == Grid.CHECKED

    def is_open(self) -> bool:
        """Checks if a node is open to be checked by a pathfinding algorithm"""
        return self.value == Grid.OPEN

    def __eq__(self, other):
        if isinstance(other, GridNode):
            return self.x == other.x and self.y == other.y

        return False


class Grid:
    EMPTY = 0
    BARRIER = 1
    TARGET = 2
    START = 3
    PATH = 4
    CHECKED = 5
    OPEN = 6

    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.target_node = None
        self.start_node = None

        self.cells = []

        self.node_colors = {
            Grid.EMPTY: colors.WHITE,
            Grid.BARRIER: colors.BLACK,
            Grid.TARGET: colors.RED,
            Grid.START: colors.GREEN,
            Grid.PATH: colors.PURPLE,
            Grid.CHECKED: colors.BLUE,
            Grid.OPEN: colors.ORANGE
        }

        for x in range(width):
            row = []
            for y in range(height):
                row.append(GridNode(0, x, y))
            self.cells.append(row)

    def draw_cells(self, screen):
        """Draws cells on the screen"""

        for cells_list in self.cells:
            for node in cells_list:
                rect = pygame.Rect(node.x * self.cell_size, node.y * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.node_colors[node.value], rect)

    def draw_grid(self, screen):
        """Draws grid lines on the screen"""

        for x in range(self.width):
            for y in range(self.height):
                # vertical lines
                pygame.draw.line(screen, colors.GREY, (x * self.cell_size, 0),
                                 (x * self.cell_size, self.cell_size * self.height))
                # horizontal lines
                pygame.draw.line(screen, colors.GREY, (0, y * self.cell_size),
                                 (self.cell_size * self.width, y * self.cell_size))

    def restart(self):
        """Sets all cells to empty and restarts target and start nodes"""

        self.target_node = None
        self.start_node = None

        for x in range(self.width):
            for y in range(self.height):
                self.cells[x][y].value = 0

    def clear_pathfinding(self):
        """Sets all cells marked by a pathfinding algorithm back to empty"""

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y].is_checked() or self.cells[x][y].is_path() or self.cells[x][y].is_open():
                    self.cells[x][y].value = Grid.EMPTY

    def get_cell_from_coordinates(self, x: float, y: float) -> GridNode:
        """Returns a cell from coordinates"""
        try:
            cell = self.cells[int(x / self.cell_size)][int(y / self.cell_size)]
        except IndexError:
            raise IndexError("Wrong Coordinates")
        else:
            return cell
