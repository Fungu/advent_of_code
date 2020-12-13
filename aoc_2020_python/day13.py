import aoc
import math

def main(inputLines):
    earliestDeparture = int(inputLines[0])
    busList = [[i, int(bus)] for i, bus in enumerate(inputLines[1].replace("x", "-1").split(","))]
    busList = list(filter(lambda b: b[1] != -1, busList))

    bestTime = -1
    for _, bus in busList:
        nextTime = math.ceil(earliestDeparture / bus) * bus
        if bestTime == -1 or nextTime < bestTime:
            bestTime = nextTime
            bestBus = bus
    part1 = int(bestBus) * (bestTime - earliestDeparture)

    increment = busList[0][1]
    part2 = 0
    for i, bus in busList[1:]:
        while (part2 + i) % bus != 0:
            part2 += increment
        increment *= bus

    return part1, part2

aoc.runLines(main, "day13.txt")