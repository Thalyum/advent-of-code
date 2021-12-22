import os

from aocd.models import Puzzle


def load_inputs():
    """Load AoC inputs for the correct year + day, based on the filename."""
    date = os.path.basename(__file__).split(".")[0]
    aoc_year = int(date.split("-")[0])
    aoc_day = int(date.split("-")[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.splitlines()


def part_one(input):
    """Solve puzzle's part one."""
    coord = {}
    count = 0
    for line in input:
        line_coord = line.split("->")
        x1 = int(line_coord[0].split(",")[0])
        y1 = int(line_coord[0].split(",")[1])
        x2 = int(line_coord[1].split(",")[0])
        y2 = int(line_coord[1].split(",")[1])
        # keep only vertical/horizontal lines
        if x1 == x2:
            if y2 <= y1:
                tmp = y1
                y1 = y2
                y2 = tmp
            for i in range(y2 - y1 + 1):
                coord_name = str(x1) + "-" + str(y1 + i)
                value = coord.get(coord_name)
                if value == 1:
                    # new point crossed by a second line
                    coord[coord_name] = 2
                    count += 1
                elif value == 2:
                    # point already counted
                    continue
                else:
                    # first line
                    coord[coord_name] = 1
        elif y1 == y2:
            if x2 <= x1:
                tmp = x1
                x1 = x2
                x2 = tmp
            for i in range(x2 - x1 + 1):
                coord_name = str(x1 + i) + "-" + str(y1)
                value = coord.get(coord_name)
                if value == 1:
                    # new point crossed by a second line
                    coord[coord_name] = 2
                    count += 1
                elif value == 2:
                    # point already counted
                    continue
                else:
                    # first line
                    coord[coord_name] = 1
    output = count
    print("part one: {}".format(output))


def part_two(input):
    """Solve puzzle's part two."""
    coord = {}
    count = 0
    for line in input:
        line_coord = line.split("->")
        x1 = int(line_coord[0].split(",")[0])
        y1 = int(line_coord[0].split(",")[1])
        x2 = int(line_coord[1].split(",")[0])
        y2 = int(line_coord[1].split(",")[1])
        if x1 == x2:
            if y2 <= y1:
                tmp = y1
                y1 = y2
                y2 = tmp
            for i in range(y2 - y1 + 1):
                coord_name = str(x1) + "-" + str(y1 + i)
                value = coord.get(coord_name)
                if value == 1:
                    # new point crossed by a second line
                    coord[coord_name] = 2
                    count += 1
                elif value == 2:
                    # point already counted
                    continue
                else:
                    # first line
                    coord[coord_name] = 1
        elif y1 == y2:
            if x2 <= x1:
                tmp = x1
                x1 = x2
                x2 = tmp
            for i in range(x2 - x1 + 1):
                coord_name = str(x1 + i) + "-" + str(y1)
                value = coord.get(coord_name)
                if value == 1:
                    # new point crossed by a second line
                    coord[coord_name] = 2
                    count += 1
                elif value == 2:
                    # point already counted
                    continue
                else:
                    # first line
                    coord[coord_name] = 1
        else:
            for i in range(max(x1, x2) - min(x1, x2) + 1):
                if x1 > x2:
                    coord_x = str(x1 - i)
                else:
                    coord_x = str(x1 + i)
                if y1 > y2:
                    coord_y = str(y1 - i)
                else:
                    coord_y = str(y1 + i)
                coord_name = coord_x + "-" + coord_y
                value = coord.get(coord_name)
                if value == 1:
                    # new point crossed by a second line
                    coord[coord_name] = 2
                    count += 1
                elif value == 2:
                    # point already counted
                    continue
                else:
                    # first line
                    coord[coord_name] = 1
    output = count
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    part_one(input)
    part_two(input)
