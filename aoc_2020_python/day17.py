import aoc
import operator
import itertools

def main(inputLines):
    neighbors3d, neighbors4d = getNeighborTypes()
    state = getState(inputLines, neighbors4d)
    
    part1 = runSimulation(state, neighbors3d, 6)
    part2 = runSimulation(state, neighbors4d, 6)

    return part1, part2

def runSimulation(state, neighborsType, cycles):
    for _ in range(cycles):
        nextState = {}
        for pos in state:
            neighbors = countNeighbors(state, pos, neighborsType)
            # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
            if state[pos] and neighbors in [2, 3]:
                nextState[pos] = True
                initNeighbors(nextState, pos, neighborsType)
            # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
            elif not state[pos] and neighbors == 3:
                nextState[pos] = True
                initNeighbors(nextState, pos, neighborsType)
        state = nextState
    
    ret = countState(state)
    return ret

def getNeighborTypes():
    directions = [-1, 0, 1]
    neighbors3d = list(itertools.product(directions, directions, directions, [0]))
    neighbors4d = list(itertools.product(directions, directions, directions, directions))
    neighbors3d.remove((0, 0, 0, 0))
    neighbors4d.remove((0, 0, 0, 0))
    return neighbors3d, neighbors4d

def getState(inputLines, neighborsType):
    state = {}
    for row, line in enumerate(inputLines):
        for col, char in enumerate(line):
            state[(row, col, 0, 0)] = char == "#"
            initNeighbors(state, (row, col, 0, 0), neighborsType)
    return state

def initNeighbors(state, pos, neighbors):
    for n in neighbors:
        p = tuple(map(operator.add, n, pos))
        if p not in state:
            state[p] = False

def countNeighbors(state, pos, neighbors):
    ret = 0
    for n in neighbors:
        p = tuple(map(operator.add, n, pos))
        if p in state and state[p]:
            ret += 1
    return ret

def countState(state):
    ret = 0
    for value in state.values():
        if value:
            ret += 1
    return ret

aoc.runLines(main, "day17.txt")