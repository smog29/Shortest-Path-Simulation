# !/usr/bin/env python3

__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"

from src.grid import Grid
from src.pathfinding import a_star_pathfinding
from src.pathfinding import dijkstra_pathfinding
import timeit


def a_star_path() -> None:
    """Runs a star algorithm without showing any steps"""
    a_star.find_path(grid.start_node, grid.target_node, False)


def dijkstra_path() -> None:
    """Runs dijkstra algorithm without showing any steps"""
    dijkstra.find_path(grid.start_node, grid.target_node, False)


if __name__ == "__main__":
    WIDTH = 1225
    HEIGHT = 945
    cell_size = 35

    grid = Grid(int(WIDTH / cell_size), int(HEIGHT / cell_size), cell_size)
    grid.cells[0][0].value = Grid.START
    grid.start_node = grid.cells[0][0]
    grid.cells[grid.width - 1][grid.height - 1].value = Grid.TARGET
    grid.target_node = grid.cells[grid.width - 1][grid.height - 1]

    a_star = a_star_pathfinding.AStarPathfinding(grid, None)
    print("A star time for finding 10 paths: ", timeit.timeit(a_star_path, number=10))

    dijkstra = dijkstra_pathfinding.DijkstraPathfinding(grid, None)
    print("Dijkstra time for finding 10 paths: ", timeit.timeit(dijkstra_path, number=10))
