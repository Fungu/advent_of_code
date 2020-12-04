import time
import math

def main():
    with open("input/day3.txt") as file:
        grid = [[char.strip() == "#" for char in line.strip()] for line in file.readlines()]

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
    
    print("Part 1:", collisions[1])
    print("Part 2:", math.prod(collisions))

start = time.time()
main()
print("Execution time:", time.time() - start, "ms")