import aoc
import functools

def main(input_lines):
    boardingpass_list = [get_boardingpass(line) for line in input_lines]
    
    part1 = functools.reduce(lambda a, b: a if a[2] > b[2] else b, boardingpass_list)[2]
    part2 = find_empty_seat(boardingpass_list)
    
    return part1, part2

def get_boardingpass(line):
    row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
    column = int(line[7:].replace("L", "0").replace("R", "1"), 2)
    return row, column, get_seat_id(row, column)

def find_empty_seat(boardingpass_list):
    for row in range(0, 128):
        if all(((row, column, get_seat_id(row, column)) in boardingpass_list) for column in range(0, 8)):
            start_row = row + 1
            break
    for row in range(start_row, 128):
        for column in range(0, 8):
            seat_id = get_seat_id(row, column)
            if (row, column, seat_id) not in boardingpass_list:
                return seat_id

def get_seat_id(row, column):
    return row * 8 + column

aoc.run_lines(main, "day05.txt")