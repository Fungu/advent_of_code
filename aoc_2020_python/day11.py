import aoc

def main(inputLines):
    state = {}
    everyDirection = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    closest = {}
    for line in range(len(inputLines)):
        for row in range(len(inputLines[line].strip())):
            if inputLines[line][row] != ".":
                closest[(line, row)] = []
                state[(line, row)] = False
                for direction in everyDirection:
                    linePos = line + direction[0]
                    rowPos = row + direction[1]
                    if linePos >= 0 and linePos < len(inputLines) and rowPos >= 0 and rowPos < len(inputLines[line].strip()) and inputLines[linePos][rowPos] == "L":
                        closest[(line, row)].append((linePos, rowPos))

    resultChanged = True
    while resultChanged:
        state, resultChanged = simulate(state, closest, 4)
    part1 = 0
    for key in state:
        if state[key]:
            part1 += 1


    state = {}
    seen = {}
    for line in range(len(inputLines)):
        for row in range(len(inputLines[line].strip())):
            if inputLines[line][row] != ".":
                seen[(line, row)] = []
                state[(line, row)] = False
                for direction in everyDirection:
                    linePos = line + direction[0]
                    rowPos = row + direction[1]
                    while linePos >= 0 and linePos < len(inputLines) and rowPos >= 0 and rowPos < len(inputLines[line].strip()):
                        if inputLines[linePos][rowPos] != ".":
                            seen[(line, row)].append((linePos, rowPos))
                            break
                        linePos += direction[0]
                        rowPos += direction[1]

    resultChanged = True
    while resultChanged:
        state, resultChanged = simulate(state, seen, 5)
    part2 = 0
    for key in state:
        if state[key]:
            part2 += 1

    return part1, part2

def simulate(state, seats, maxNeighbors):
    result = {}
    resultChanged = False

    for key in state.keys():
        neighbors = 0
        for seat in seats[key]:
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