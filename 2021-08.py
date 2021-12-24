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
    processed = input
    return processed


def part_one(processed):
    """Solve puzzle's part one."""
    count = 0
    for line in processed:
        out_digit = line.split("|")[1].split()
        for digit in out_digit:
            length = len(digit)
            if length == 2 or length == 4 or length == 3 or length == 7:
                count += 1
    output = count
    print("part one: {}".format(output))


class Digit:
    # TODO: find a cleaner way to solve this Puzzle to create a dictionary
    def __init__(self, input_seq):
        self.sequence_remain = copy.deepcopy(input_seq)
        # simpler: self.sequence_remain = input_seq[:]
        self.zero = ""
        self.two = ""
        self.three = ""
        self.five = ""
        self.six = ""
        self.nine = ""
        for digit in input_seq:
            if len(digit) == 7:
                self.height = digit
                self.sequence_remain.remove(digit)
            elif len(digit) == 4:
                self.four = digit
                self.sequence_remain.remove(digit)
            elif len(digit) == 3:
                self.seven = digit
                self.sequence_remain.remove(digit)
            elif len(digit) == 2:
                self.one = digit
                self.sequence_remain.remove(digit)
        if len(self.sequence_remain) != 6:
            print("error init")

    def find_nine(self):
        for digit in self.sequence_remain:
            # does the sequence contains 7's and 4's segments ?
            is_four = [c in digit for c in self.four]
            is_seven = [c in digit for c in self.seven]
            if False in is_four or False in is_seven:
                continue
            nine = digit
            break
        self.nine = nine
        self.sequence_remain.remove(nine)
        if len(self.sequence_remain) != 5:
            print("error 9")

    def find_zero_and_three(self):
        for digit in self.sequence_remain:
            # does it contains 7's segments ?
            is_seven = [c in digit for c in self.seven]
            if False in is_seven:
                continue
            if len(digit) == 6:
                zero = digit
                continue
            if len(digit) == 5:
                three = digit
                continue
        self.zero = zero
        self.three = three
        self.sequence_remain.remove(zero)
        self.sequence_remain.remove(three)
        if len(self.sequence_remain) != 3:
            print("error 03")

    def find_the_rest(self):
        six, five, two = "", "", ""
        filter_seg = [c for c in self.nine if c not in self.three]
        if len(filter_seg) != 1:
            print("error filter")
        else:
            filter_seg = filter_seg[0]
        for digit in self.sequence_remain:
            if len(digit) == 6 and not six:
                six = digit
                continue
            if filter_seg in digit and not five:
                five = digit
            if filter_seg not in digit and not two:
                two = digit
        self.six = six
        self.five = five
        self.two = two
        self.sequence_remain.remove(six)
        self.sequence_remain.remove(five)
        self.sequence_remain.remove(two)
        if len(self.sequence_remain) != 0:
            print("error finish")

    def translate_output(self, output):
        number = ""
        for digit in output:
            if sorted(self.nine) == sorted(digit):
                number += "9"
                continue
            if sorted(self.height) == sorted(digit):
                number += "8"
                continue
            if sorted(self.seven) == sorted(digit):
                number += "7"
                continue
            if sorted(self.six) == sorted(digit):
                number += "6"
                continue
            if sorted(self.five) == sorted(digit):
                number += "5"
                continue
            if sorted(self.four) == sorted(digit):
                number += "4"
                continue
            if sorted(self.three) == sorted(digit):
                number += "3"
                continue
            if sorted(self.two) == sorted(digit):
                number += "2"
                continue
            if sorted(self.one) == sorted(digit):
                number += "1"
                continue
            if sorted(self.zero) == sorted(digit):
                number += "0"
                continue
            print("not found !")
        return int(number)


def part_two(processed):
    """Solve puzzle's part two."""
    counter = 0
    for line in processed:
        in_digit = line.split("|")[0].split()
        out_digit = line.split("|")[1].split()
        digit_sequence = Digit(in_digit)
        digit_sequence.find_nine()
        digit_sequence.find_zero_and_three()
        digit_sequence.find_the_rest()
        counter += digit_sequence.translate_output(out_digit)
    output = counter
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
