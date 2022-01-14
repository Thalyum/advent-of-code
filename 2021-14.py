# MIT License
# Copyright (c) 2021 Paul-Erwan RIO

import copy
import os
from collections import Counter, deque

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
    template = input[0]
    pair_list = []
    for pair in input[2:]:
        pair_list.append(pair.split(" -> "))
    return (template, pair_list)


def compute_next_template(template, pair_list):
    next_template = []
    first_char = template[0]
    for c in range(len(template) - 1):
        second_char = template[c + 1]
        next_template.append(first_char)
        for pair in pair_list:
            if first_char == pair[0][0] and second_char == pair[0][1]:
                next_template.append(pair[1])
        first_char = second_char
    next_template.append(second_char)
    return next_template


def part_one(processed):
    """Solve puzzle's part one."""
    (template, pair_list) = processed
    for _ in range(10):
        template = compute_next_template(template, pair_list)
    count = Counter(template).most_common()
    output = count[0][1] - count[-1][1]
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    (template, pair_list) = processed
    for _ in range(40):
        template = compute_next_template(template, pair_list)
    count = Counter(template).most_common()
    output = count[0][1] - count[-1][1]
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
