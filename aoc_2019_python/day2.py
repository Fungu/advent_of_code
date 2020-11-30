import intcode
import datetime

def main():
    with open("input/day2.txt") as file:
        memory = [int(val) for val in file.read().split(",")]

    output = run_program(memory.copy(), 12, 2)
    print("part 1: ", output, output == 3409710)

    for x in range(0, 99):
        for y in range(0, 99):
            output = run_program(memory.copy(), x, y)
            if output == 19690720:
                print("part 2: ", 100 * x + y, 100 * x + y == 7912)
                break

def run_program(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb

    intcode.runProgram(memory)
    
    return memory[0]


start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)