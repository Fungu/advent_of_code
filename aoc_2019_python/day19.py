import aoc
from intcode import Intcode

def main(puzzle_input):
    part1 = 0
    for y in range(50):
        for x in range(50):
            computer = Intcode(puzzle_input)
            computer.input = [x, y]
            computer.run_program()
            part1 += computer.output[0]

    left = 0
    right = []
    y = 5
    while True:
        for x in range(left, left + 100):    
            computer = Intcode(puzzle_input)
            computer.input = [x, y]
            computer.run_program()
            if computer.output[0] == 1:
                left = x
                break
        if len(right) == 0:
            right.append(left)
        for x in range(right[-1], right[-1] + 100):
            computer = Intcode(puzzle_input)
            computer.input = [x, y]
            computer.run_program()
            if computer.output[0] == 0:
                right.append(x - 1)
                break
        if len(right) > 100:
            if right[-100] - 99 >= left:
                part2 = left * 10000 + y - 99
                break
        y += 1
    
    return part1, part2

aoc.run_raw(main, "day19.txt")