import os

from aocd.models import Puzzle


def load_inputs():
    date = os.path.basename(__file__).split('.')[0]
    aoc_year = int(date.split('-')[0])
    aoc_day = int(date.split('-')[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.splitlines()

def part_one(input):
    depth = 0
    pos = 0
    for line in input:
        instr = line.split()[0]
        param = int(line.split()[1])
        if instr == "up":
            depth -= param
            if depth < 0:
                print("depth error ?")
        elif instr == "down":
            depth += param
        elif instr == "forward":
            pos += param
    output = pos * depth
    print("part one: {}".format(output))

def part_two(input):
    depth = 0
    pos = 0
    aim = 0
    for line in input:
        instr = line.split()[0]
        param = int(line.split()[1])
        if instr == "up":
            aim -= param
        elif instr == "down":
            aim += param
        elif instr == "forward":
            pos += param
            depth += (aim * param)
    output = pos * depth
    print("part two: {}".format(output))

if __name__ == "__main__":
    input = load_inputs()
    part_one(input)
    part_two(input)
