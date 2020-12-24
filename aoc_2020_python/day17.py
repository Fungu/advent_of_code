import aoc
import gameoflife
import itertools

def main(inputLines):
    neighbors3d, neighbors4d = getNeighborTypes()
    state = initState(inputLines, neighbors4d)
    remainActiveWhen = lambda adjacentCount: adjacentCount in [2, 3]
    becomeActiveWhen = lambda adjacentCount: adjacentCount == 3

    state1 = gameoflife.runSimulation(state, 6, neighbors3d, remainActiveWhen, becomeActiveWhen)
    part1 = gameoflife.countActive(state1)

    state2 = gameoflife.runSimulation(state, 6, neighbors4d, remainActiveWhen, becomeActiveWhen)
    part2 = gameoflife.countActive(state2)

    return part1, part2

def getNeighborTypes():
    directions = [-1, 0, 1]
    neighbors3d = list(itertools.product(directions, directions, directions, [0]))
    neighbors4d = list(itertools.product(directions, directions, directions, directions))
    neighbors3d.remove((0, 0, 0, 0))
    neighbors4d.remove((0, 0, 0, 0))
    return neighbors3d, neighbors4d

def initState(inputLines, neighborsType):
    state = {}
    for row, line in enumerate(inputLines):
        for col, char in enumerate(line):
            state[(row, col, 0, 0)] = char == "#"
    return state

aoc.runLines(main, "day17.txt")