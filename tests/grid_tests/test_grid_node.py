# !/usr/bin/env python3

__author__ = "Jakub Swistak"
__copyright__ = "Copyright (c) Jakub Swistak"
__email__ = "kuba175174@gmail.com"
__version__ = "1.0"

from src.grid import GridNode, Grid

import unittest
from unittest import TestCase


class GridNodeTest(TestCase):
    def setUp(self) -> None:
        self.grid_node = GridNode(0, 0, 0)

    def test_calculate_f_cost(self):
        self.grid_node.h_cost = 2
        self.grid_node.g_cost = 2
        self.grid_node.calculate_f_cost()

        f_cost = self.grid_node.f_cost
        self.assertEqual(f_cost, 4)

    def test_grid_node_is_empty(self):
        self.grid_node.value = Grid.EMPTY

        self.assertTrue(self.grid_node.is_empty())

    def test_grid_node_is_barrier(self):
        self.grid_node.value = Grid.BARRIER

        self.assertTrue(self.grid_node.is_barrier())

    def test_grid_node_is_target(self):
        self.grid_node.value = Grid.TARGET

        self.assertTrue(self.grid_node.is_target())

    def test_grid_node_is_start(self):
        self.grid_node.value = Grid.START

        self.assertTrue(self.grid_node.is_start())

    def test_grid_node_is_path(self):
        self.grid_node.value = Grid.PATH

        self.assertTrue(self.grid_node.is_path())

    def test_grid_node_is_checked(self):
        self.grid_node.value = Grid.CHECKED

        self.assertTrue(self.grid_node.is_checked())

    def test_grid_node_is_open(self):
        self.grid_node.value = Grid.OPEN

        self.assertTrue(self.grid_node.is_open())

    def test_grid_node_equals(self):
        self.grid_node.x = 4
        self.grid_node.y = 5
        node = GridNode(0, 4, 5)

        self.assertTrue(self.grid_node == node)

if __name__ == "__main__":
    unittest.main()
