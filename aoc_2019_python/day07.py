import aoc
from intcode import Intcode
import itertools

def main(puzzle_input):
    part1 = 0
    for phaseSettings in itertools.permutations(range(5)):
        prev_output = [0]
        for phaseSetting in phaseSettings:
            computer = Intcode(puzzle_input)
            computer.input = [phaseSetting, prev_output[0]]
            computer.run_program()
            part1 = max(part1, computer.output[0])
            prev_output = computer.output

    part2 = 0
    computer_count = 5
    for phaseSettings in itertools.permutations(range(5, 10)):
        computers = [Intcode("0") for _ in range(computer_count)]
        for i in range(computer_count):
            computers[i].memory = computer.memory.copy()
            computers[i].output = [phaseSettings[i]]
        for i in range(computer_count):
            computers[i].input = computers[i - 1].output
        computers[0].input.append(0)
        
        while computers[0].finished == False:
            for i in range(computer_count):
                computers[i].run_program()
        part2 = max(part2, computers[-1].output[0])
    
    return part1, part2

aoc.run_raw(main, "day07.txt")