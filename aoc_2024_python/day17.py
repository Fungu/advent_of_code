import aoc

def main(lines: list):
    program = [int(a) for a in lines[4].split(": ")[1].split(",")]

    registers = [int(lines[0].split(": ")[1]), 
                 int(lines[1].split(": ")[1]), 
                 int(lines[2].split(": ")[1])]
    output = calculate(program, registers)
    part1 = ",".join([str(o) for o in output])


    a_replacement = 0
    current_index = len(program) - 1
    while True:
        registers = [a_replacement, 
                    int(lines[1].split(": ")[1]), 
                    int(lines[2].split(": ")[1])]
        output = calculate(program, registers)
        if current_index == 0 and output == program:
            break
        if program[current_index:] == output:
            a_replacement *= 8
            current_index -= 1
        else:
            a_replacement += 1
    part2 = a_replacement

    return part1, part2

def calculate(program, registers):
    instruction_pointer = 0
    output = []
    while True:
        if instruction_pointer >= len(program):
            break
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]
        
        if opcode == 0:
            registers[0] /= pow(2, combo(operand, registers))
        if opcode == 1:
            registers[1] ^= operand
        if opcode == 2:
            registers[1] = combo(operand, registers) % 8
        if opcode == 3:
            if registers[0] != 0:
                instruction_pointer = operand - 2
        if opcode == 4:
            registers[1] ^= registers[2]
        if opcode == 5:
            output.append(int(combo(operand, registers) % 8))
        if opcode == 6:
            registers[1] = registers[0] / pow(2, combo(operand, registers))
        if opcode == 7:
            registers[2] = registers[0] / pow(2, combo(operand, registers))
        
        instruction_pointer += 2
        for i in range(len(registers)):
            registers[i] = int(registers[i])
    return output

def combo(operand, registers):
    if operand <= 3:
        return operand
    return registers[operand - 4]

aoc.run_lines(main, "day17.txt")
