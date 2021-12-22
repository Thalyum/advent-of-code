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
    """Create the initial state list.

    Each element represents the number of fishes whose
    timer is equal to the array index.
    """
    fish_array = np.zeros(9, dtype=int)
    for day_remaining in [int(n) for n in input[0].split(",")]:
        fish_array[day_remaining] += 1
    return fish_array


def part_one(processed):
    """Solve puzzle's part one."""
    timer_fish = processed
    for i in range(80):
        new_fish = timer_fish[0]
        # shift the calendar
        for f in range(len(timer_fish) - 1):
            timer_fish[f] = timer_fish[f + 1]
        # process new-born: child
        timer_fish[8] = new_fish
        # process new-born: parent
        timer_fish[6] += new_fish
    output = sum(timer_fish)
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    timer_fish = processed
    # first 80 days has already been computed by part 1,
    # as I did not deep-copied the array
    # we should've used:
    # timer_fish = copy.deepcopy(processed)
    for i in range(256 - 80):
        new_fish = timer_fish[0]
        # shift the calendar
        for f in range(len(timer_fish) - 1):
            timer_fish[f] = timer_fish[f + 1]
        # process new-born: child
        timer_fish[8] = new_fish
        # process new-born: parent
        timer_fish[6] += new_fish
    output = sum(timer_fish)
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
