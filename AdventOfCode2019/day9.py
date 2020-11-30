import intcode
import datetime

def main():
    with open("input/day9.txt") as file:
        memory = [int(val) for val in file.read().split(",")]

    memory += [0] * 1000

    output = []
    intcode.runProgram(memory.copy(), [1], output)
    part1 = output[0]
    
    output = []
    intcode.runProgram(memory.copy(), [2], output)
    part2 = output[0]

    print("part 1:", part1, part1 == 2594708277)
    print("part 2:", part2, part2 == 87721)

start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)