import aoc

def main(rawInput):
    inputList = [int(a) for a in rawInput.split(",")]
    
    part1 = memoryGame(inputList, 2020)
    part2 = memoryGame(inputList, 30000000)

    return part1, part2

# TODO: This solution takes 10 seconds to run. Figure out a quicker way to do this.
def memoryGame(inputList, iterations):
    spokenNumbers = {}
    for i in range(len(inputList)):
        lastNumber = inputList[i]
        spokenNumbers[lastNumber] = i
    for i in range(len(inputList), iterations):
        if lastNumber in spokenNumbers:
            thisNumber = i - 1 - spokenNumbers[lastNumber]
        else:
            thisNumber = 0
        spokenNumbers[lastNumber] = i - 1
        lastNumber = thisNumber
    return lastNumber

aoc.runRaw(main, "day15.txt")