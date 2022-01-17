# MIT License
# Copyright (c) 2021 Paul-Erwan RIO

import copy
import os
from collections import Counter, defaultdict

import numpy as np
from aocd.models import Puzzle

last_letter = ""


def load_inputs():
    """Load AoC inputs for the correct year + day, based on the filename."""
    date = os.path.basename(__file__).split(".")[0]
    aoc_year = int(date.split("-")[0])
    aoc_day = int(date.split("-")[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.splitlines()


def process_input(input):
    """Puzzle-specific input processing."""
    global last_letter
    state = {}
    template = input[0]
    last_letter = template[-1]
    pair_list = []
    for pair in input[2:]:
        pair_list.append(pair.split(" -> "))
    # init state from template
    for c in range(len(template) - 1):
        couple = template[c : c + 2]
        if couple not in state:
            state[couple] = {"current": 1, "next": 0, "op": []}
    # init state from pair list
    for p in pair_list:
        couple = p[0]
        middle = p[1]
        if couple not in state:
            state[couple] = {"current": 0, "next": 0, "op": []}
        first_new_couple = couple[0] + middle
        second_new_couple = middle + couple[1]
        if first_new_couple not in state:
            state[first_new_couple] = {"current": 0, "next": 0, "op": []}
        if second_new_couple not in state:
            state[second_new_couple] = {"current": 0, "next": 0, "op": []}
        state[couple]["op"].append(first_new_couple)
        state[couple]["op"].append(second_new_couple)
    return state


def part_one(processed):
    """Solve puzzle's part one."""
    for _ in range(10):
        for couple in processed:
            # if list of operation is empty
            # this couple will not 'evolve' anymore
            if processed[couple]["op"]:
                current = processed[couple]["current"]
                for op in processed[couple]["op"]:
                    processed[op]["next"] += current
                # the couple is 'consumed' into its next op
                processed[couple]["current"] = 0
        # current <- next
        for couple in processed:
            processed[couple]["current"] = processed[couple]["next"]
            processed[couple]["next"] = 0
    # count letters: count the first letter of each couple
    counter = defaultdict(int)
    for c in processed:
        counter[c[0]] += processed[c]["current"]
    # do not forget to count the last letter
    counter[last_letter] += 1
    count = Counter(counter).most_common()
    # most common - least common
    output = count[0][1] - count[-1][1]
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    # we already did 10 iteration in first part
    for _ in range(30):
        for couple in processed:
            # if list of operation is empty
            # this couple will not 'evolve' anymore
            if processed[couple]["op"]:
                current = processed[couple]["current"]
                for op in processed[couple]["op"]:
                    processed[op]["next"] += current
                # the couple is 'consumed' into its next op
                processed[couple]["current"] = 0
        # current <- next
        for couple in processed:
            processed[couple]["current"] = processed[couple]["next"]
            processed[couple]["next"] = 0
    # count letters: count the first letter of each couple
    counter = defaultdict(int)
    for c in processed:
        counter[c[0]] += processed[c]["current"]
    # do not forget to count the last letter
    counter[last_letter] += 1
    count = Counter(counter).most_common()
    # most common - least common
    output = count[0][1] - count[-1][1]
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
