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
    # example input
    # input = [
    #     "start-A",
    #     "start-b",
    #     "A-c",
    #     "A-b",
    #     "b-d",
    #     "A-end",
    #     "b-end",
    # ]
    # larger example
    # input = [
    #     "dc-end",
    #     "HN-start",
    #     "start-kj",
    #     "dc-start",
    #     "dc-HN",
    #     "LN-dc",
    #     "HN-end",
    #     "kj-sa",
    #     "kj-HN",
    #     "kj-dc",
    # ]
    graph = {}
    for arc in [line.split("-") for line in input]:
        if arc[0] not in graph:
            graph[arc[0]] = []
        graph[arc[0]].append(arc[1])
        if arc[1] not in graph:
            graph[arc[1]] = []
        graph[arc[1]].append(arc[0])
    return graph


def iterate_path_maze(graph, path_list):
    new_path_list = []
    for path in path_list:
        last_cave = path[-1]
        if last_cave == 'end':
            # path finished, keep it
            new_path_list.append(path)
            continue
        for possible_cave in graph[last_cave]:
            if possible_cave == 'start':
                # we do not pass through start cave twice
                continue
            elif possible_cave.islower() and possible_cave in path:
                # forget this path, as we do not cross small caves twice
                continue
            else:
                # register possible path
                new_path = copy.deepcopy(path)
                new_path.append(possible_cave)
                new_path_list.append(new_path)
    return new_path_list


def iterate_path_maze_part2(graph, path_list, small_cave_ok):
    new_path_list = []
    new_small_cave_ok = []
    for (index, path) in enumerate(path_list):
        last_cave = path[-1]
        if last_cave == 'end':
            # path finished, keep it
            new_path_list.append(path)
            new_small_cave_ok.append(small_cave_ok[index])
            continue
        for possible_cave in graph[last_cave]:
            if possible_cave == 'start':
                # we do not pass through start cave twice
                continue
            elif possible_cave.islower() and possible_cave in path:
                if small_cave_ok[index]:
                    new_path = copy.deepcopy(path)
                    new_path.append(possible_cave)
                    new_path_list.append(new_path)
                    new_small_cave_ok.append(False)
                else:
                    # forget this path, as we do not cross small caves more than once
                    continue
            else:
                # register possible path
                new_path = copy.deepcopy(path)
                new_path.append(possible_cave)
                new_path_list.append(new_path)
                new_small_cave_ok.append(small_cave_ok[index])
    return (new_path_list, new_small_cave_ok)


def is_iteration_finished(path_list):
    return all([path[-1] == 'end' for path in path_list])


def part_one(processed):
    """Solve puzzle's part one."""
    path_list = []
    path_list.append(['start'])
    while not is_iteration_finished(path_list):
        path_list = iterate_path_maze(processed, path_list)
    # print(path_list)
    output = len(path_list)
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    path_list = []
    small_cave_ok = []
    path_list.append(['start'])
    small_cave_ok.append(True)
    while not is_iteration_finished(path_list):
        (path_list, small_cave_ok) = iterate_path_maze_part2(processed, path_list, small_cave_ok)
    output = "N/A"
    # print(path_list)
    output = len(path_list)
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
