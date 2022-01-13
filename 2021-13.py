# MIT License
# Copyright (c) 2021 Paul-Erwan RIO

import copy
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
    array = []
    instructions = []
    # input = [
    #     "2,0",
    #     "0,0",
    #     "2,2",
    #     "fold along x=1"
    # ]
    for line in input:
        if 'fold' in line:
            instructions.append(line.removeprefix("fold along "))
        elif not line:
            continue
        else:
            coord = [int(a) for a in line.split(",")]
            coord_dict = {'x': coord[0], 'y': coord[1]}
            array.append(coord_dict)
    return (array, instructions)


def part_one(array, instructions):
    """Solve puzzle's part one."""
    dimension = instructions[0].split("=")[0]
    if dimension == 'x':
        other_dimension = 'y'
    else:
        other_dimension = 'x'
    line_number = int(instructions[0].split("=")[1])
    new_array = []
    for coord in array:
        if coord[dimension] == line_number:
            # discard this point, it is on the folding line
            continue
        elif coord[dimension] <= line_number:
            # keep the point as is
            if coord not in new_array:
                # check if the point is not already there
                new_coord = copy.deepcopy(coord)
                new_array.append(new_coord)
        else:
            # keep the symmetric
            new_coord = {other_dimension: coord[other_dimension]}
            new_coord[dimension] = (2 * line_number) - coord[dimension]
            if new_coord not in new_array:
                new_array.append(new_coord)
    output = len(new_array)
    print("part one: {}".format(output))


def part_two(array, instructions):
    """Solve puzzle's part two."""
    for instruction in instructions:
        dimension = instruction.split("=")[0]
        if dimension == 'x':
            other_dimension = 'y'
        else:
            other_dimension = 'x'
        line_number = int(instruction.split("=")[1])
        new_array = []
        for coord in array:
            if coord[dimension] == line_number:
                # discard this point, it is on the folding line
                continue
            elif coord[dimension] <= line_number:
                # keep the point as is
                if coord not in new_array:
                    # check if the point is not already there
                    new_coord = copy.deepcopy(coord)
                    new_array.append(new_coord)
            else:
                # keep the symmetric
                new_coord = {other_dimension: coord[other_dimension]}
                new_coord[dimension] = (2 * line_number) - coord[dimension]
                if new_coord not in new_array:
                    new_array.append(new_coord)
        array = new_array
    # print the code
    # dirty code
    tmp = np.zeros((10,50), dtype=int)
    for coord in array:
        tmp[coord['y']][coord['x']] = 1
    for row in tmp:
        for column in row:
            if column:
                print("*", end="")
            else:
                print(" ", end="")
        print("")
    output = "N/A"
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    (array, instructions) = process_input(input)
    part_one(array, instructions)
    part_two(array, instructions)
