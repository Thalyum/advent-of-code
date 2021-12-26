# MIT License
# Copyright (c) 2021 Paul-Erwan RIO

import os

from aocd.models import Puzzle


def load_inputs():
    date = os.path.basename(__file__).split('.')[0]
    aoc_year = int(date.split('-')[0])
    aoc_day = int(date.split('-')[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.split()

def part_one(input):
    measures = [int(n) for n in input]
    count = 0
    prev = measures[0]
    for measure in measures:
        if measure > prev:
            count += 1
        prev = measure
    print("part one: {}".format(count))

def part_two(input):
    measures = [int(n) for n in input]
    count = 0
    prev0 = measures[0]
    prev1 = measures[1]
    prev2 = measures[2]
    prev_sum = prev0 + prev1 + prev2
    for measure in measures[3:]:
        new_sum = prev1 + prev2 + measure
        if new_sum > prev_sum:
            count += 1
        prev_sum = new_sum
        prev0 = prev1
        prev1 = prev2
        prev2 = measure
    print("part two: {}".format(count))

if __name__ == "__main__":
    input = load_inputs()
    part_one(input)
    part_two(input)
