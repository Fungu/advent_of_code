import aoc
from intcode import Intcode

def main(puzzle_input):
    computer = Intcode(puzzle_input)

    program_input = []
    add_function(program_input, "NOT C J")
    add_function(program_input, "AND D J")
    add_function(program_input, "NOT A T")
    add_function(program_input, "OR T J")
    add_function(program_input, "WALK")
    computer.input = program_input
    computer.run_program()

    for c in computer.output:
        if c >= 256:
            part1 = c
            break
    
    # ABC[D]EFG[H]I
    program_input = []
    
    # Hole in A or B or C
    add_function(program_input, "NOT A J") 
    add_function(program_input, "NOT B T") 
    add_function(program_input, "OR T J") 
    add_function(program_input, "NOT C T")
    add_function(program_input, "OR T J")

    # Ground in D and (H or (E and I))
    add_function(program_input, "AND D J")
    add_function(program_input, "OR I T")
    add_function(program_input, "AND E T")  
    add_function(program_input, "OR H T")
    add_function(program_input, "AND T J") 
    add_function(program_input, "RUN")

    computer = Intcode(puzzle_input)
    computer.input = program_input
    computer.run_program()
    for c in computer.output:
        if c >= 256:
            part2 = c
            break
    
    return part1, part2
    
def add_function(program_input, function):
    new_line = 10
    for c in function:
        program_input.append(ord(c))
    program_input.append(new_line)

aoc.run_raw(main, "day21.txt")