# MIT License
# Copyright (c) 2021 Paul-Erwan RIO

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
    processed = [int(n) for n in input[0].split(",")]
    return processed


def part_one(processed):
    """Solve puzzle's part one."""
    # the answer is the median value
    target = int(np.median(processed))
    fuel = [abs(n - target) for n in processed]
    output = sum(fuel)
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    # the answer is the mean value
    target = int(np.mean(processed))
    fuel = [int((abs(n - target) * (abs(n - target) + 1)) / 2) for n in processed]
    output = sum(fuel)
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
