# MIT License
# Copyright (c) 2021 Paul-Erwan RIO

import os
from collections import deque

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
    # simple example input
    # input = ["11111", "19991", "19191", "19991", "11111"]
    # example input
    # input = [
    #     "5483143223",
    #     "2745854711",
    #     "5264556173",
    #     "6141336146",
    #     "6357385478",
    #     "4167524645",
    #     "2176841721",
    #     "6882881134",
    #     "4846848554",
    #     "5283751526",
    # ]
    processed = [[int(n) for n in line] for line in input]
    return processed


def dfs_update_octopus_flash(grid, plan_grid, i, j):
    # TODO: add a visualization effect (like the plan_grid where points glows
    # when they switch to one) to see the DFS propagation
    height = len(grid)
    width = len(grid[0])
    plan_grid[i][j] = 1
    for ni, nj in [
        (i + 1, j),
        (i + 1, j + 1),
        (i, j + 1),
        (i - 1, j + 1),
        (i - 1, j),
        (i - 1, j - 1),
        (i, j - 1),
        (i + 1, j - 1),
    ]:
        if 0 <= ni < height and 0 <= nj < width:
            grid[ni][nj] += 1
            if grid[ni][nj] > 9 and plan_grid[ni][nj] == 0:
                dfs_update_octopus_flash(grid, plan_grid, ni, nj)


def part_one(processed):
    """Solve puzzle's part one."""
    height = len(processed)
    width = len(processed[0])
    octopus_map = np.array(processed)
    plan_to_flash_map = np.zeros((height, width), dtype=int)
    increase_energy_level = np.ones((height, width), dtype=int)
    nb_step = 100
    nb_flashes = 0
    for _ in range(nb_step):
        octopus_map += increase_energy_level
        # update the energy values and mark the octopuses that will flash
        for i in range(height):
            for j in range(width):
                if octopus_map[i][j] > 9 and plan_to_flash_map[i][j] == 0:
                    dfs_update_octopus_flash(octopus_map, plan_to_flash_map, i, j)
        # consume flashing marks and reset energy level
        for i in range(height):
            for j in range(width):
                if plan_to_flash_map[i][j] == 1:
                    octopus_map[i][j] = 0
                    plan_to_flash_map[i][j] = 0
                    nb_flashes += 1
    output = nb_flashes
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    height = len(processed)
    width = len(processed[0])
    octopus_map = np.array(processed)
    plan_to_flash_map = np.zeros((height, width), dtype=int)
    increase_energy_level = np.ones((height, width), dtype=int)
    output = -1
    step = 0
    while True:
        step += 1
        octopus_map += increase_energy_level
        # update the energy values and mark the octopuses that will flash
        for i in range(height):
            for j in range(width):
                if octopus_map[i][j] > 9 and plan_to_flash_map[i][j] == 0:
                    dfs_update_octopus_flash(octopus_map, plan_to_flash_map, i, j)
        # consume flashing marks and reset energy level
        total_flash = 0
        for i in range(height):
            for j in range(width):
                if plan_to_flash_map[i][j] == 1:
                    octopus_map[i][j] = 0
                    plan_to_flash_map[i][j] = 0
                    total_flash += 1
        if total_flash == width * height:
            output = step
            break
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
