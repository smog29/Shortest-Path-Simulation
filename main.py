import pygame

import colors
from grid import Grid
from pathfinding import PathFinding


class MainWindow:
    def __init__(self):
        pygame.init()

        self.WIDTH = 1225
        self.HEIGHT = 945

        self.screen = None
        self.set_window()

        cell_size = 35

        self.space_clicked = False

        self.grid = Grid(int(self.WIDTH / cell_size), int(self.HEIGHT / cell_size), cell_size)
        self.pathfinding = PathFinding(self.grid, self)

    def set_window(self):
        background_colour = colors.WHITE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption('A* pathfinding')

        self.screen.fill(background_colour)

        pygame.display.flip()

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    self.left_mouse_clicked()
                elif pygame.mouse.get_pressed(num_buttons=3)[2]:
                    self.right_mouse_clicked()

                self.check_input()

            self.draw()

    def draw(self):
        self.grid.draw_cells(self.screen)
        self.grid.draw_grid(self.screen)
        pygame.display.flip()

    def check_input(self):
        keys = pygame.key.get_pressed()

        x, y = pygame.mouse.get_pos()
        cell = self.grid.get_cell(x, y)

        # restart
        if keys[pygame.K_r]:
            self.grid.restart()
            self.space_clicked = False

        if self.space_clicked:
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

        # target
        if keys[pygame.K_t] and (self.grid.target_node is None) and cell.is_empty():
            cell.value = Grid.TARGET
            self.grid.target_node = cell

        # start
        if keys[pygame.K_s] and (self.grid.start_node is None) and cell.is_empty():
            cell.value = Grid.START
            self.grid.start_node = cell

        # space
        if keys[pygame.K_SPACE]:
            self.space_clicked = True
            self.start_path_finding()

    def left_mouse_clicked(self):
        if not self.space_clicked:
            return

        x, y = pygame.mouse.get_pos()
        cell = self.grid.get_cell(x, y)
        if cell.is_barrier() or cell.is_start() or cell.is_target():
            return

        self.grid.target_node.value = Grid.EMPTY

        cell.value = Grid.TARGET
        self.grid.target_node = cell

        self.grid.clear_pathfinding()

        self.pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def right_mouse_clicked(self):
        if not self.space_clicked:
            return

        x, y = pygame.mouse.get_pos()
        cell = self.grid.get_cell(x, y)
        if cell.is_barrier() or cell.is_start() or cell.is_target():
            return

        self.grid.start_node.value = Grid.EMPTY

        cell.value = Grid.START
        self.grid.start_node = cell

        self.grid.clear_pathfinding()

        self.pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def start_path_finding(self):
        if (self.grid.start_node is None) or (self.grid.target_node is None):
            return

        self.pathfinding.find_path(self.grid.start_node, self.grid.target_node, True)


def main():
    window = MainWindow()
    window.start()


main()
