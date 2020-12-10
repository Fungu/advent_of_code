import time

def runLines(mainFunction, day):
    with open("input/" + day) as file:
        rawInput = file.readlines()
    run(mainFunction, rawInput)

def runRaw(mainFunction, day):
    with open("input/" + day) as file:
        rawInput = file.read()
    run(mainFunction, rawInput)

def run(mainFunction, rawInput):
    start = time.time()
    part1, part2 = mainFunction(rawInput)
    executionTime = time.time() - start
    executionTime = round(executionTime * 1000)
    print("Execution time:", executionTime, "ms")
    print("Part 1:", part1)
    print("Part 2:", part2)