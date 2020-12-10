import aoc

def main(inputLines):
    program = [[line.split(" ")[0], int(line.split(" ")[1])] for line in inputLines]

    part1, _ = runProgram(program, -1)
    for i in range(len(program)):
        acc, goodExit = runProgram(program, i)
        if goodExit:
            part2 = acc
            break

    return part1, part2

def runProgram(program, instructionToFlip):
    seenInstructions = []
    nopJmpCounter = 0
    programPointer = 0
    acc = 0
    while programPointer not in seenInstructions and programPointer < len(program):
        seenInstructions.append(programPointer)
        instruction = program[programPointer][0]
        value = program[programPointer][1]
        programPointer += 1

        if nopJmpCounter == instructionToFlip:
            if instruction == "nop":
                instruction = "jmp"
            elif instruction == "jmp":
                instruction = "nop"
        
        if instruction == "acc":
            acc += value
        elif instruction == "jmp":
            programPointer += value - 1
            nopJmpCounter += 1
        elif instruction == "nop":
            nopJmpCounter += 1
    
    return acc, programPointer >= len(program)

aoc.runLines(main, "day08.txt")