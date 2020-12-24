import aoc
import gameoflife
import operator
import re

# Cube coordinates (pointy topped)
directions = {
    "se": [0, -1, 1],
    "nw": [0, 1, -1],
    "sw": [-1, 0, 1],
    "ne": [1, 0, -1],
    "e": [1, -1, 0],
    "w": [-1, 1, 0]
}

def main(inputLines):
    state = initState(inputLines)
    part1 = gameoflife.countActive(state)

    state = gameoflife.runSimulation(
        state, 100, directions.values(), 
        remainActiveWhen = lambda adjacentCount: 1 <= adjacentCount <= 2,
        becomeActiveWhen = lambda adjacentCount: adjacentCount == 2)
    part2 = gameoflife.countActive(state)

    return part1, part2

def initState(inputLines):
    state = {}
    prog = re.compile("se|nw|sw|ne|e|w")
    for line in inputLines:
        position = (0, 0, 0)
        for dirString in prog.findall(line):
            position = tuple(map(operator.add, position, directions[dirString]))
        state[position] = not (position in state and state[position])
    return state

aoc.runLines(main, "day24.txt")