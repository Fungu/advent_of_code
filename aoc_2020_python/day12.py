import aoc

def main(inputLines):
    part1 = followInstructions(inputLines, 0 + 0j, 1 + 0j, True)
    part2 = followInstructions(inputLines, 0 + 0j, 10 + 1j, False)
    
    return part1, part2

def followInstructions(instructions, position, direction, part1):
    dirDict = { "E": 1, "W": -1, "N": 1j, "S": -1j}
    rotDict = { "L": 1j, "R": -1j}

    for line in instructions:
        action = line[0]
        value = int(line[1:])
        # E, W, N, S
        if action in dirDict:
            if part1:
                position += dirDict[action] * value
            else:
                direction += dirDict[action] * value
        # L, R
        elif action in rotDict:
            assert(value % 90 == 0)
            direction *= rotDict[action] ** int(value / 90)
        # F
        elif action == "F":
            position += direction * value
        else:
            assert(False)
    
    return int(abs(position.real) + abs(position.imag))

aoc.runLines(main, "day12.txt")