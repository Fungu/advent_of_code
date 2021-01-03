import aoc
from intcode import Intcode

def main(puzzle_input):
    computer = Intcode(puzzle_input)
    computer.input.append(1)
    computer.run_program()
    part1 = computer.output[0]
    
    computer = Intcode(puzzle_input)
    computer.input.append(2)
    computer.run_program()
    part2 = computer.output[0]

    return part1, part2

aoc.run_raw(main, "day09.txt")