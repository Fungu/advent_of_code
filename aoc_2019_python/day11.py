import aoc
from intcode import Intcode
from collections import defaultdict

def main(puzzle_input):
    paint = defaultdict(int)
    calculate_paint(puzzle_input, paint)
    part1 = len(paint)

    paint = defaultdict(int)
    paint[0] = 1
    xmin, xmax, ymin, ymax = calculate_paint(puzzle_input, paint)
    
    part2 = ""
    for y in range(ymin, ymax + 1):
        part2 += "\n"
        for x in range(xmin, xmax + 1):
            if paint[x + y * 1j] == 1:
                part2 += "#"
            else:
                part2 += " "
    
    return part1, part2

def calculate_paint(puzzle_input, paint):
    xmin = ymin = float("inf")
    xmax = ymax = -float("inf")
    pos = 0
    facing = -1j

    computer = Intcode(puzzle_input)
    while not computer.finished:
        computer.output.clear()
        computer.input.append(paint[pos])
        computer.run_program()
        paint[pos] = computer.output[0]
        facing *= (1j if computer.output[1] == 1 else -1j)
        pos += facing
        xmin = min(xmin, pos.real)
        xmax = max(xmax, pos.real)
        ymin = min(ymin, pos.imag)
        ymax = max(ymax, pos.imag)
    return int(xmin), int(xmax), int(ymin), int(ymax)

aoc.run_raw(main, "day11.txt")