from grid.grid import Grid
from pathfinding import astarpathfinding, dijkstra_pathfinding
import timeit


def a_star_path():
    a_star.find_path(grid.start_node, grid.target_node, False)


def dijkstra_path():
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

    a_star = astarpathfinding.AStarPathfinding(grid, None)
    print(timeit.timeit(a_star_path, number=10))

    dijkstra = dijkstra_pathfinding.DijkstraPathfinding(grid, None)
    print(timeit.timeit(dijkstra_path, number=10))
