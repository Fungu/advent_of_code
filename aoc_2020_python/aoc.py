import time

def runLines(mainFunction, day):
    with open("input/" + day) as file:
        rawInput = file.readlines()
    run(mainFunction, rawInput)

def runBlob(mainFunction, day):
    with open("input/" + day) as file:
        rawInput = file.read()
    run(mainFunction, rawInput)

def run(mainFunction, rawInput):
    start = time.time()
    part1, part2 = mainFunction(rawInput)
    print("Execution time:", time.time() - start, "s")
    print("Part 1:", part1)
    print("Part 2:", part2)