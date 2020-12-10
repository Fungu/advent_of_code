import aoc
import math

def main(inputLines):
    grid = [[char.strip() == "#" for char in line.strip()] for line in inputLines]

    slopes = [[1, 1],
            [3, 1],
            [5, 1],
            [7, 1],
            [1, 2]]

    collisions = [0] * len(slopes)
    for index in range(len(slopes)):
        posX = 0
        posY = 0
        for _ in range(int(len(grid) / slopes[index][1])):
            if grid[posY][posX]:
                collisions[index] += 1
            posX += slopes[index][0]
            posX %= len(grid[0])
            posY += slopes[index][1]
    
    return collisions[1], math.prod(collisions)

aoc.runLines(main, "day03.txt")