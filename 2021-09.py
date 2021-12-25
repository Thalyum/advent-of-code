import copy
import os

import numpy as np
from aocd.models import Puzzle


def load_inputs():
    """Load AoC inputs for the correct year + day, based on the filename."""
    date = os.path.basename(__file__).split(".")[0]
    aoc_year = int(date.split("-")[0])
    aoc_day = int(date.split("-")[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.splitlines()


def process_input(input):
    """Puzzle-specific input processing."""
    # puzzle example
    # input = [
    #     "2199943210",
    #     "3987894921",
    #     "9856789892",
    #     "8767896789",
    #     "9899965678",
    #     "9999999999",
    #     "9999999999",
    #     "9999999999",
    #     "9999999999",
    #     "9999999999",
    # ]
    processed = []
    for line in input:
        pline = [int(c) for c in line]
        processed.append(pline)
    return np.array(processed)


def find_local_minima(array):
    """Find the local minima in a 2D array.

    Return the minima map"""
    size = len(array)
    print("{}x{}".format(size, size))
    minima_map = np.ones((size, size), dtype=int)
    for (row_index, row) in enumerate(processed):
        prev_val = float("+inf")
        for (col_index, value) in enumerate(row):
            # remove points that are ascending to the right
            if value >= prev_val:
                minima_map[row_index][col_index] &= 0
            prev_val = value
        prev_val = float("+inf")
        for (col_index, value) in enumerate(row[::-1]):
            # remove points that are ascending to the left
            if value >= prev_val:
                minima_map[row_index][size - 1 - col_index] &= 0
            prev_val = value
    for (col_index, col) in enumerate(processed.T):
        prev_val = float("+inf")
        for (row_index, value) in enumerate(col):
            # remove points that are ascending to the bottom
            if value >= prev_val:
                minima_map[row_index][col_index] &= 0
            prev_val = value
        prev_val = float("+inf")
        for (row_index, value) in enumerate(col[::-1]):
            # remove points that are ascending to the top
            if value >= prev_val:
                minima_map[size - 1 - row_index][col_index] &= 0
            prev_val = value
    return minima_map


def part_one(processed):
    """Solve puzzle's part one."""
    minima_map = find_local_minima(processed)
    # compute 'risk level'
    risk_level = 0
    for (row_index, row) in enumerate((minima_map)):
        for (col_index, minima) in enumerate(row):
            if minima:
                risk_level += 1 + processed[row_index][col_index]
    output = risk_level
    print("part one: {}".format(output))


# Seems like the perfect opportunity to try out the 'connected spaces'
# algorithm, available in "Programmation Efficace" book from
# 'Christoph Durr' and 'Jill-Jenn Vie'
def dfs_grid(grid, i, j, mark):
    grid[i][j] = mark
    size = len(grid)
    for ni, nj in [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]:
        if 0 <= ni < size and 0 <= nj < size:
            if grid[ni][nj] == -1:
                dfs_grid(grid, ni, nj, mark)


def part_two(processed):
    """Solve puzzle's part two."""
    size = len(processed)
    # create a basins map
    nb_basins = 0
    basins_map = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            if processed[i][j] != 9:
                basins_map[i][j] = -1
    for i in range(size):
        for j in range(size):
            if basins_map[i][j] == -1:
                nb_basins += 1
                dfs_grid(basins_map, i, j, nb_basins)
    # find the three largest basins
    max1 = 0
    max2 = 0
    max3 = 0
    # we do not want basins = 0 (there are the basins edge)
    for n in range(1, nb_basins + 1):
        new_basin_size = np.count_nonzero(basins_map == n)
        if new_basin_size >= max1:
            max3 = max2
            max2 = max1
            max1 = new_basin_size
        elif new_basin_size >= max2:
            max3 = max2
            max2 = new_basin_size
        elif new_basin_size >= max3:
            max3 = new_basin_size
    output = max1 * max2 * max3
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
