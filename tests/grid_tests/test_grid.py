# !/usr/bin/env python3

__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"

from src.grid import Grid

import unittest
from unittest import TestCase


class GridTest(TestCase):
    def setUp(self) -> None:
        self.grid = Grid(2, 2, 2)

    def test_grid_restart(self):
        self.grid.cells[0][0].value = Grid.BARRIER
        self.grid.restart()

        value = self.grid.cells[0][0].value
        self.assertEqual(value, Grid.EMPTY)

    def test_grid_clear_pathfinding(self):
        self.grid.cells[0][0].value = Grid.PATH
        self.grid.cells[0][1].value = Grid.BARRIER
        self.grid.clear_pathfinding()

        path_node_value = self.grid.cells[0][0].value
        barrier_node_value = self.grid.cells[0][1].value

        with self.subTest():
            self.assertEqual(path_node_value, Grid.EMPTY)

        with self.subTest():
            self.assertEqual(barrier_node_value, Grid.BARRIER)

    def test_grid_raise_exception_on_wrong_coordinates(self):
        with self.assertRaises(IndexError) as ie:
            self.grid.get_cell_from_coordinates(100, 0)

        self.assertEqual("Wrong Coordinates", str(ie.exception))


if __name__ == "__main__":
    unittest.main()
