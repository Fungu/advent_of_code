import aoc
import math

def main(input_lines):
    grid = [[char.strip() == "#" for char in line.strip()] for line in input_lines]

    slopes = [[1, 1],
            [3, 1],
            [5, 1],
            [7, 1],
            [1, 2]]

    collisions = [0] * len(slopes)
    for index in range(len(slopes)):
        pos_x = 0
        pos_y = 0
        for _ in range(int(len(grid) / slopes[index][1])):
            if grid[pos_y][pos_x]:
                collisions[index] += 1
            pos_x += slopes[index][0]
            pos_x %= len(grid[0])
            pos_y += slopes[index][1]
    
    return collisions[1], math.prod(collisions)

aoc.run_lines(main, "day03.txt")