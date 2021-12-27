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
    processed = [line.split("-") for line in input]
    return processed


class Cave:
    def __init__(self, name):
        self.name = name
        if name.isupper() and name != "start" and name != "end":
            self.big_cave = True
        else:
            self.big_cave = False
        self.passage_list = []

    def add_path(self, cave):
        if cave != self:
            self.passage_list.append(cave)

    def display_passage(self):
        for cave in self.passage_list:
            print(cave.name, end=",")
        print("\b")


class Maze:
    def __init__(self, path_list):
        self.cave_list = []
        self.start = False
        self.end = False
        for path in path_list:
            first_cave_name = path[0]
            second_cave_name = path[1]
            first_cave = self.search_for_cave(first_cave_name)
            if not first_cave:
                first_cave = Cave(first_cave_name)
                if first_cave_name == "start" and not self.start:
                    self.start = first_cave
                elif first_cave_name == "end" and not self.end:
                    self.end = first_cave
                self.cave_list.append(first_cave)
            second_cave = self.search_for_cave(second_cave_name)
            if not second_cave:
                second_cave = Cave(second_cave_name)
                if second_cave_name == "start" and not self.start:
                    self.start = second_cave
                elif second_cave_name == "end" and not self.end:
                    self.end = second_cave
                self.cave_list.append(second_cave)
            first_cave.add_path(second_cave)
            second_cave.add_path(first_cave)

    def search_for_cave(self, name):
        for cave in self.cave_list:
            if cave.name == name:
                return cave
        return False

    def display_maze(self, cave_list=[], brief=False):
        if not cave_list:
            cave_list = self.cave_list
        if not brief:
            for cave in cave_list:
                print("{}: ".format(cave.name), end="")
                cave.display_passage()
            print("---")
        else:
            for cave in cave_list:
                print(cave.name, end=",")
            print("\b")

    def find_all_paths(self, current_cave=False, path_list=[]):
        if not current_cave:
            self.path_found = 0
            current_cave = self.start
            path_list = [current_cave]
        for possible_cave in current_cave.passage_list:
            if possible_cave == self.end:
                # add last node
                final_path_list = copy.deepcopy(path_list)
                final_path_list.append(possible_cave)
                # print path found
                # self.display_maze(final_path_list, brief=True)
                self.path_found += 1
                continue
            is_crossed = [possible_cave.name == cave.name for cave in path_list]
            if True in is_crossed and not possible_cave.big_cave:
                continue
            new_path_list = copy.deepcopy(path_list)
            new_path_list.append(possible_cave)
            self.find_all_paths(possible_cave, new_path_list)


def part_one(processed):
    """Solve puzzle's part one."""
    maze = Maze(processed)
    maze.display_maze()
    maze.find_all_paths()
    output = maze.path_found
    print("part one: {}".format(output))


def part_two(processed):
    """Solve puzzle's part two."""
    output = "N/A"
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    processed = process_input(input)
    part_one(processed)
    part_two(processed)
