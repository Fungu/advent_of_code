import aoc
import operator

# Cube coordinates (pointy topped)
directions = {
    "e": [1, -1, 0],
    "se": [0, -1, 1],
    "sw": [-1, 0, 1],
    "w": [-1, 1, 0],
    "nw": [0, 1, -1],
    "ne": [1, 0, -1]
}

def main(inputLines):
    state = initState(inputLines)
    
    part1 = countState(state)
    part2 = countState(runSimulation(state))

    return part1, part2

def initState(inputLines):
    state = {}
    for line in inputLines:
        position = [0, 0, 0]
        partialDirection = ""
        for c in line:
            if c in ["e", "w"]:
                direction = directions[partialDirection + c]
                position = list(map(operator.add, position, direction))
                partialDirection = ""
            else:
                partialDirection = c
        
        pos = tuple(position)
        if pos in state and state[pos]:
            state[pos] = False
        else:
            state[pos] = True
        initNeighbors(state, pos, directions.values())
    return state

def runSimulation(state, cycles = 100):
    for _ in range(cycles):
        nextState = {}
        for pos in state:
            neighbors = countNeighbors(state, pos, directions.values())
            # Any black pos with zero or more than 2 black poss immediately adjacent to it is flipped to white.
            if state[pos] and not (neighbors == 0 or neighbors > 2):
                nextState[pos] = True
                initNeighbors(nextState, pos, directions.values())
            # Any white pos with exactly 2 black poss immediately adjacent to it is flipped to black.
            elif not state[pos] and neighbors == 2:
                nextState[pos] = True
                initNeighbors(nextState, pos, directions.values())
        state = nextState
    
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
    return len(list(filter(lambda value: value, state.values())))

aoc.runLines(main, "day24.txt")