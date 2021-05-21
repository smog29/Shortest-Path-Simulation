import pygame

from colors import colors
from grid.grid import Grid
from pathfinding import astarpathfinding, dijkstra_pathfinding


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

        self.space_clicked = False
        self.should_draw_text = True

        self.grid = Grid(int(self.WIDTH / cell_size), int(self.HEIGHT / cell_size), cell_size)
        self.a_star_pathfinding = astarpathfinding.AStarPathfinding(self.grid, self)
        self.dijkstra_pathfinding = dijkstra_pathfinding.DijkstraPathfinding(self.grid, self)

    def set_window(self):
        background_colour = colors.WHITE
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Shortest Path")

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.change_algorithm()

                self.check_input()

            self.draw()

    def draw(self):
        self.grid.draw_cells(self.screen)
        self.grid.draw_grid(self.screen)

        if self.should_draw_text:
            self.draw_text()

        pygame.display.flip()

    def draw_text(self):
        text = self.font.render(self.current_algorithm, True, colors.TEXT_COLOR)
        self.screen.blit(text, (10, 10))

    def change_algorithm(self):
        self.should_draw_text = True
        if self.current_algorithm == "AStar":
            self.current_algorithm = "Dijkstra"

            if self.space_clicked:
                self.grid.clear_pathfinding()
                self.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
        else:
            self.current_algorithm = "AStar"

            if self.space_clicked:
                self.grid.clear_pathfinding()
                self.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def check_input(self):
        keys = pygame.key.get_pressed()

        # restart
        if keys[pygame.K_r]:
            self.grid.restart()
            self.space_clicked = False
            self.should_draw_text = True

        if self.space_clicked:
            return

        x, y = pygame.mouse.get_pos()
        cell = self.grid.get_cell(x, y)

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
            self.start_path_finding()

    def left_mouse_clicked(self):
        x, y = pygame.mouse.get_pos()
        cell = self.grid.get_cell(x, y)

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

        if self.current_algorithm == "AStar":
            self.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
        else:
            self.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def right_mouse_clicked(self):
        x, y = pygame.mouse.get_pos()
        cell = self.grid.get_cell(x, y)

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

        if self.current_algorithm == "AStar":
            self.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)
        else:
            self.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, False)

    def start_path_finding(self):
        if self.current_algorithm == "AStar":
            self.a_star_pathfinding.find_path(self.grid.start_node, self.grid.target_node, True)
        else:
            self.dijkstra_pathfinding.find_path(self.grid.start_node, self.grid.target_node, True)


if __name__ == "__main__":
    window = MainWindow()
    window.start()
