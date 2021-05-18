import pygame
import colors


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

        for x in range(width):
            row = []
            for y in range(height):
                row.append(GridNode(0, self, x, y))
            self.cells.append(row)

    def draw_cells(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x][y]

                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                   self.cell_size, self.cell_size)

                if cell.is_empty():
                    pygame.draw.rect(screen, colors.WHITE, rect)
                if cell.is_barrier():
                    pygame.draw.rect(screen, colors.BLACK, rect)
                if cell.is_target():
                    pygame.draw.rect(screen, colors.RED, rect)
                if cell.is_start():
                    pygame.draw.rect(screen, colors.GREEN, rect)
                if cell.is_path():
                    pygame.draw.rect(screen, colors.PURPLE, rect)
                if cell.is_checked():
                    pygame.draw.rect(screen, colors.BLUE, rect)
                if cell.is_open():
                    pygame.draw.rect(screen, colors.ORANGE, rect)

    def draw_grid(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                # vertical lines
                pygame.draw.line(screen, colors.GREY, (x * self.cell_size, 0),
                                 (x * self.cell_size, self.cell_size * self.height))
                # horizontal lines
                pygame.draw.line(screen, colors.GREY, (0, y * self.cell_size),
                                 (self.cell_size * self.width, y * self.cell_size))

    def restart(self):
        self.target_node = None
        self.start_node = None

        for x in range(self.width):
            for y in range(self.height):
                self.cells[x][y].value = 0

    def clear_pathfinding(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y].is_checked() or self.cells[x][y].is_path() or self.cells[x][y].is_open():
                    self.cells[x][y].value = Grid.EMPTY

    def get_cell(self, x: float, y: float):
        return self.cells[int(x / self.cell_size)][int(y / self.cell_size)]


class GridNode:

    def __init__(self, value: int, grid: Grid, x: int, y: int):
        self.value = value
        self.grid = grid
        self.x = x
        self.y = y
        self.came_from_node = None

        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

    def calculate_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def is_empty(self) -> bool:
        return self.value == Grid.EMPTY

    def is_barrier(self) -> bool:
        return self.value == Grid.BARRIER

    def is_target(self) -> bool:
        return self.value == Grid.TARGET

    def is_start(self) -> bool:
        return self.value == Grid.START

    def is_path(self) -> bool:
        return self.value == Grid.PATH

    def is_checked(self) -> bool:
        return self.value == Grid.CHECKED

    def is_open(self) -> bool:
        return self.value == Grid.OPEN

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, GridNode):
            return self.x == other.x and self.y == other.y

        return False
