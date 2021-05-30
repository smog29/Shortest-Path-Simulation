# !/usr/bin/env python3

__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"

import pygame

from src.gui import colors
from src.grid import Grid
from src import pathfinding
from src.input import InputManager


class MainWindow:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.WIDTH = 1225
        self.HEIGHT = 945

        self.screen = None
        self.current_algorithm = "AStar"
        self.set_window()

        self.font = pygame.font.Font("freesansbold.ttf", 20)

        cell_size = 35

        self.should_draw_text = True

        self.grid = Grid(int(self.WIDTH / cell_size), int(self.HEIGHT / cell_size), cell_size)
        self.a_star_pathfinding = pathfinding.AStarPathfinding(self.grid, self)
        self.dijkstra_pathfinding = pathfinding.DijkstraPathfinding(self.grid, self)

        self.input = InputManager(self.grid, self)

    def set_window(self):
        """Sets and creates window"""

        background_colour = colors.WHITE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Pathfinding")

        self.screen.fill(background_colour)

        pygame.display.flip()

    def start(self):
        """Starts main game loop"""

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.input.left_mouse_clicked()
                elif pygame.mouse.get_pressed(num_buttons=3)[2]:
                    self.input.right_mouse_clicked()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.change_algorithm()

            self.input.check_input()

            self.draw()

    def draw(self):
        """Draws cells and grid lines on the screen"""
        self.grid.draw_cells(self.screen)
        self.grid.draw_grid(self.screen)

        if self.should_draw_text:
            self.draw_text()

        pygame.display.flip()

    def draw_text(self):
        """Views chosen algorithm on the screen"""
        text = self.font.render(self.current_algorithm, True, colors.TEXT_COLOR)
        self.screen.blit(text, (10, 10))

    def change_algorithm(self):
        self.should_draw_text = True
        if self.current_algorithm == "AStar":
            self.current_algorithm = "Dijkstra"

            if self.input.space_clicked:
                self.grid.clear_pathfinding()
                self.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
        else:
            self.current_algorithm = "AStar"

            if self.input.space_clicked:
                self.grid.clear_pathfinding()
                self.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def start_path_finding(self):
        """Starts pathfinding with showing steps"""
        if self.current_algorithm == "AStar":
            self.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, True)
        else:
            self.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, True)


if __name__ == "__main__":
    window = MainWindow()
    window.start()
