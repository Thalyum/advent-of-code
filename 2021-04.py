import os

from aocd.models import Puzzle

BOARD_SIZE = 5


class Bingo:
    def __init__(self, data):
        self.win = False
        new_bingo_board = []
        for i in range(BOARD_SIZE):
            new_line = []
            for j in range(BOARD_SIZE):
                num = data[5 * i + j]
                new_element = {"number": num, "marked": False}
                new_line.append(new_element)
            new_bingo_board.append(new_line)
        self.board = new_bingo_board

    def display(self):
        print("\n")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                print(self.board[i][j]["number"], end=" ")
            print("")

    def _check_win(self, line, column):
        check_line = [
            e["marked"] for e in [self.board[line][j] for j in range(BOARD_SIZE)]
        ]
        check_column = [
            e["marked"] for e in [self.board[i][column] for i in range(BOARD_SIZE)]
        ]
        if False in check_line and False in check_column:
            return False
        else:
            self.win = True
            return True

    def mark_number(self, number):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j]["number"] == number:
                    self.board[i][j]["marked"] = True
                    return self._check_win(i, j)

    def compute_win(self, number):
        bingo_sum = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.board[i][j]["marked"]:
                    bingo_sum += self.board[i][j]["number"]
        return bingo_sum * number


def load_inputs():
    """Load AoC inputs for the correct year + day, based on the filename."""
    date = os.path.basename(__file__).split(".")[0]
    aoc_year = int(date.split("-")[0])
    aoc_day = int(date.split("-")[1])
    puzzle = Puzzle(year=aoc_year, day=aoc_day)
    return puzzle.input_data.splitlines()


def parse_boards(input):
    draw_list = [int(n) for n in input[0].split(",")]
    first = False
    bingo_list = []
    input.append("")
    for (line_number, line) in enumerate(input):
        if line == "":
            if not first:
                first = True
                continue
            else:
                board = []
                for i in range(5):
                    for n in input[line_number - 5 + i].split():
                        board.append(int(n))
                if len(board) != BOARD_SIZE ** 2:
                    print("error")
                bingo_list.append(Bingo(board))
    return (bingo_list, draw_list)


def part_one(bingo_list, draw_list):
    """Solve puzzle's part one."""
    for number in draw_list:
        for bingo in bingo_list:
            win = bingo.mark_number(number)
            if win:
                # bingo.display()
                final_score = bingo.compute_win(number)
                # remove first winning bingo for step two
                bingo_list.remove(bingo)
                break
        if win:
            break
    output = final_score
    print("part one: {}".format(output))


def part_two(bingo_list, draw_list):
    """Solve puzzle's part two."""
    last_win = False
    total_win = 0
    for number in draw_list:
        for bingo in bingo_list:
            if not bingo.win:
                win = bingo.mark_number(number)
                # we cannot remove a element of a list while we are iterating over it. Either we mark them for 'deletion' and remove them once outside of the loop, or we keep track of each win.
                if win:
                    total_win += 1
                if win and total_win == 99:
                    last_win = True
                    # bingo.display()
                    final_score = bingo.compute_win(number)
                    break
        if last_win:
            break
    output = final_score
    print("part two: {}".format(output))


if __name__ == "__main__":
    input = load_inputs()
    (bingo_list, draw_list) = parse_boards(input)
    part_one(bingo_list, draw_list)
    part_two(bingo_list, draw_list)
