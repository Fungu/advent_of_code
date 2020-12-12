import aoc

def main(inputLines):
    part1 = followInstructions(inputLines, 1 + 0j, True)
    part2 = followInstructions(inputLines, 10 + 1j, False)
    
    return part1, part2

def followInstructions(instructions, speed, part1):
    # Complex numbers are  used for position and rotation. The real part represents East and West. The imaginary part represents North and South.
    # To rotate a direction, just multiply it with the corresponding value in rotations.
    # Example: directions["E"] * rotations["L"] == directions["N"]
    directions = { "E": 1, "W": -1, "N": 1j, "S": -1j }
    rotations = { "L": 1j, "R": -1j }
    position = 0 + 0j

    for line in instructions:
        action = line[0]
        value = int(line[1:])
        # E, W, N, S
        if action in directions:
            if part1:
                position += directions[action] * value
            else:
                speed += directions[action] * value
        # L, R
        elif action in rotations:
            assert value % 90 == 0
            speed *= rotations[action] ** int(value / 90)
        # F
        elif action == "F":
            position += speed * value
        else:
            assert False
    
    return int(abs(position.real) + abs(position.imag))

aoc.runLines(main, "day12.txt")