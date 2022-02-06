import aoc

def main(input_lines):
    program = [[line.split(" ")[0], int(line.split(" ")[1])] for line in input_lines]

    part1, _ = run_program(program, -1)
    for i in range(len(program)):
        acc, good_exit = run_program(program, i)
        if good_exit:
            part2 = acc
            break

    return part1, part2

def run_program(program, instruction_to_flip):
    seen_instructions = []
    nop_jmp_counter = 0
    program_pointer = 0
    acc = 0
    while program_pointer not in seen_instructions and program_pointer < len(program):
        seen_instructions.append(program_pointer)
        instruction = program[program_pointer][0]
        value = program[program_pointer][1]
        program_pointer += 1

        if nop_jmp_counter == instruction_to_flip:
            if instruction == "nop":
                instruction = "jmp"
            elif instruction == "jmp":
                instruction = "nop"
        
        if instruction == "acc":
            acc += value
        elif instruction == "jmp":
            program_pointer += value - 1
            nop_jmp_counter += 1
        elif instruction == "nop":
            nop_jmp_counter += 1
    
    return acc, program_pointer >= len(program)

aoc.run_lines(main, "day08.txt")