import aoc

def main(inputLines):
    everyDirection = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    height = len(inputLines)
    width = len(inputLines[0].strip())

    state = {}
    adjacentSeats = {}
    seenSeats = {}
    for row in range(height):
        for col in range(width):
            if inputLines[row][col] != ".":
                adjacentSeats[(row, col)] = []
                seenSeats[(row, col)] = []
                state[(row, col)] = inputLines[row][col] == "#"
                for dRow, dCol in everyDirection:
                    rowPos = row + dRow
                    colPos = col + dCol
                    directNeighbor = True
                    while 0 <= rowPos < height and 0 <= colPos < width:
                        if inputLines[rowPos][colPos] != ".":
                            if directNeighbor:
                                adjacentSeats[(row, col)].append((rowPos, colPos))
                            seenSeats[(row, col)].append((rowPos, colPos))
                            break
                        directNeighbor = False
                        rowPos += dRow
                        colPos += dCol

    part1 = simulateUntilStable(state, adjacentSeats, maxNeighbors=4)
    part2 = simulateUntilStable(state, seenSeats, maxNeighbors=5)
    
    return part1, part2

def simulateUntilStable(state, adjacentSeats, maxNeighbors):
    stateCopy = state.copy()
    resultChanged = True
    while resultChanged:
        stateCopy, resultChanged = simulate(stateCopy, adjacentSeats, maxNeighbors)
    ret = 0
    for seat in stateCopy:
        if stateCopy[seat]:
            ret += 1
    return ret

def simulate(state, adjacentSeats, maxNeighbors):
    result = {}
    resultChanged = False

    for key in state.keys():
        neighbors = 0
        for seat in adjacentSeats[key]:
            if state[seat]:
                neighbors += 1
        if state[key] and neighbors >= maxNeighbors:
            result[key] = False
            resultChanged = True
        elif not state[key] and neighbors == 0:
            result[key] = True
            resultChanged = True
        else:
            result[key] = state[key]

    return result, resultChanged

aoc.runLines(main, "day11.txt")