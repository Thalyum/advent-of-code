import os

from aocd.models import Puzzle


def load_inputs():
    date = os.path.basename(__file__).split('.')[0]
    aoc_year = int(date.split('-')[0])
    aoc_day = int(date.split('-')[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.splitlines()

def part_one(input):
    gamma = ''
    epsilon = ''
    for i in range(len(input[0])):
        vertical = [x[i] for x in input]
        zeroes = vertical.count('0')
        ones = vertical.count('1')
        if zeroes > ones:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    output = gamma * epsilon
    print("part one: {}".format(output))

def part_two(input):
    # oxygen
    filtered_input = input
    for i in range(len(input[0])):
        vertical = [x[i] for x in filtered_input]
        zeroes = vertical.count('0')
        ones = vertical.count('1')
        tmp = []
        for line in filtered_input:
            if line[i] == '0' and zeroes > ones:
                tmp.append(line)
            elif line[i] == '1' and ones >= zeroes:
                tmp.append(line)
        filtered_input = tmp
        if len(filtered_input) == 1:
            oxygen = int(filtered_input[0], 2)
            break
    # co2
    filtered_input = input
    for i in range(len(input[0])):
        vertical = [x[i] for x in filtered_input]
        zeroes = vertical.count('0')
        ones = vertical.count('1')
        tmp = []
        for line in filtered_input:
            if line[i] == '0' and zeroes <= ones:
                tmp.append(line)
            elif line[i] == '1' and ones < zeroes:
                tmp.append(line)
        filtered_input = tmp
        if len(filtered_input) == 1:
            co2 = int(filtered_input[0], 2)
            break
    output = oxygen * co2
    print("part two: {}".format(output))

if __name__ == "__main__":
    input = load_inputs()
    part_one(input)
    part_two(input)
