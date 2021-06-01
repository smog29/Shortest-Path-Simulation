__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"

from src.grid import Grid
import pygame


class InputManager:

    def __init__(self, grid: Grid, main_window):
        self.grid = grid
        self.main_window = main_window

        self.space_clicked = False

    def check_input(self) -> None:
        """Checks input from keyboard"""
        keys = pygame.key.get_pressed()

        # restart
        if keys[pygame.K_r]:
            self.grid.restart()
            self.space_clicked = False
            self.should_draw_text = True

        if self.space_clicked:
            return

        x, y = pygame.mouse.get_pos()

        try:
            cell = self.grid.get_cell_from_coordinates(x, y)
        except IndexError:
            return

        # barrier
        if keys[pygame.K_b] and cell.is_empty():
            cell.value = Grid.BARRIER

        # empty
        if keys[pygame.K_e]:
            if cell.is_start():
                self.grid.start_node = None

            if cell.is_target():
                self.grid.target_node = None

            cell.value = Grid.EMPTY

        # space
        if keys[pygame.K_SPACE]:
            if (self.grid.start_node is None) or (self.grid.target_node is None):
                return

            self.space_clicked = True
            self.should_draw_text = False
            self.main_window.start_path_finding()

    def left_mouse_clicked(self) -> None:
        """Handles left mouse btn clicked"""

        x, y = pygame.mouse.get_pos()
        try:
            cell = self.grid.get_cell_from_coordinates(x, y)
        except IndexError:
            return

        if not self.space_clicked:
            if (self.grid.target_node is None) and cell.is_empty():
                cell.value = Grid.TARGET
                self.grid.target_node = cell
            return

        if cell.is_barrier() or cell.is_start() or cell.is_target():
            return

        self.should_draw_text = False

        self.grid.target_node.value = Grid.EMPTY

        cell.value = Grid.TARGET
        self.grid.target_node = cell

        self.grid.clear_pathfinding()

        if self.main_window.current_algorithm == "AStar":
            self.main_window.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
        else:
            self.main_window.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def right_mouse_clicked(self) -> None:
        """Handles right mouse btn clicked"""

        x, y = pygame.mouse.get_pos()
        try:
            cell = self.grid.get_cell_from_coordinates(x, y)
        except IndexError:
            return

        if not self.space_clicked:
            if (self.grid.start_node is None) and cell.is_empty():
                cell.value = Grid.START
                self.grid.start_node = cell
            return

        if cell.is_barrier() or cell.is_start() or cell.is_target():
            return

        self.should_draw_text = False

        self.grid.start_node.value = Grid.EMPTY

        cell.value = Grid.START
        self.grid.start_node = cell

        self.grid.clear_pathfinding()

        if self.main_window.current_algorithm == "AStar":
            self.main_window.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
        else:
            self.main_window.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
