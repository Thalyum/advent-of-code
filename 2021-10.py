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
    # example input
    # input = [
    #     "[({(<(())[]>[[{[]{<()<>>",
    #     "[(()[<>])]({[<{<<[]>>(",
    #     "{([(<{}[<>[]}>{[]{[(<()>",
    #     "(((({<>}<{<{<>}{[]{[]{}",
    #     "[[<[([]))<([[{}[[()]]]",
    #     "[{[{({}]{}}([{[{{{}}([]",
    #     "{<[[]]>}<{[{[{[]{()[[[]",
    #     "[<(<(<(<{}))><([]([]()",
    #     "<{([([[(<>()){}]>(<<{{",
    #     "<{([{{}}[<[[[<>{}]]]>[]]",
    # ]
    processed = input
    return processed


def check_syntax(instruction):
    opening = ["(", "[", "{", "<"]
    closing = [")", "]", "}", ">"]
    stack = deque([])
    for c in instruction:
        if c in opening:
            index = opening.index(c)
            stack.append(index)
        elif c in closing:
            index = closing.index(c)
            if stack[-1] == index:
                # we are good
                stack.pop()
            else:
                # corrupted !
                return c
        else:
            print("wtf?!")
    return False


def check_completion(instruction):
    opening = ["(", "[", "{", "<"]
    closing = [")", "]", "}", ">"]
    stack = deque([])
    for c in instruction:
        if c in opening:
            index = opening.index(c)
            stack.append(index)
        elif c in closing:
            index = closing.index(c)
            if stack[-1] == index:
                # we are good
                stack.pop()
            else:
                # corrupted ! should not happen
                print("wtf?!")
        else:
            print("wtf?!")
    # completion time !
    completion = ""
    while stack:
        missing_char_index = stack.pop()
        completion += closing[missing_char_index]
    return completion


corrupt_score_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
completion_score_table = {")": 1, "]": 2, "}": 3, ">": 4}


def part_one(processed):
    """Solve puzzle's part one."""
    total_score = 0
    for line in processed:
        corruption = check_syntax(line)
        if corruption:
            # print(corruption, corrupt_score_table[corruption])
            total_score += corrupt_score_table[corruption]
    output = total_score
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    total_score_list = []
    for line in processed:
        corruption = check_syntax(line)
        if corruption:
            continue
        incomplete = check_completion(line)
        total_score = 0
        for c in incomplete:
            total_score = (total_score * 5) + completion_score_table[c]
        total_score_list.append(total_score)
    output = int(np.median(total_score_list))
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
