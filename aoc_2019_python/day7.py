import intcode
import itertools

def main():
    with open("input/day7.txt") as file:
        memory = [int(val) for val in file.read().split(",")]

    part1 = 0
    for phaseSettings in itertools.permutations(range(5)):
        output = [0]
        for phaseSetting in phaseSettings:
            input = [phaseSetting, output[0]]
            output = []
            intcode.runProgram(memory.copy(), input, output)
            part1 = max(part1, output[0])
    print("part 1: ", part1, part1 == 118936)

    part2 = 0
    for phaseSettings in itertools.permutations(range(5)):
        phaseSettings = [p + 5 for p in phaseSettings]
        memoryArray = [memory.copy() for _ in range(5)]
        ipArray = [0 for _ in range(5)]
        outputArray = [[phaseSettings[i]] for i in range(5)]
        outputArray[-1].append(0)
        inputArray = [outputArray[i - 1] for i in range(5)]
        
        programFinished = False
        while programFinished == False:
            for i in range(5):
                ipArray[i], programFinished, _ = intcode.runProgram(memoryArray[i], inputArray[i], outputArray[i], ipArray[i])
        part2 = max(part2, outputArray[-1][0])
    print("part 2: ", part2, part2 == 57660948)
main()