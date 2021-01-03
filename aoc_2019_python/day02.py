import aoc
from intcode import Intcode

def main(puzzle_input):
    part1 = run_program(puzzle_input, 12, 2)

    for x in range(0, 100):
        for y in range(0, 100):
            if run_program(puzzle_input, x, y) == 19690720:
                part2 = 100 * x + y
                break
    
    return part1, part2

def run_program(puzzle_input, noun, verb):
    computer = Intcode(puzzle_input)
    computer.memory[1] = noun
    computer.memory[2] = verb
    computer.run_program()

    return computer.memory[0]

aoc.run_raw(main, "day02.txt")