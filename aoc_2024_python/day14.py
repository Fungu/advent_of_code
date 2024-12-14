from functools import reduce
from operator import mul
import aoc
import re

def main(lines: list):
    part1 = 0

    width = 101
    height = 103
    iterations = 100
    center_vertical = int(width / 2)
    center_horizontal = int(height / 2)

    quadrants = [0, 0, 0, 0]
    robots = []

    pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
    for i in range(len(lines)):
        robot = [int(x) for x in re.match(pattern, lines[i]).groups()]
        robots.append(robot)
        x = (robot[0] + robot[2] * iterations) % width
        y = (robot[1] + robot[3] * iterations) % height
        if x < center_vertical and y < center_horizontal:
            quadrants[0] += 1
        if x > center_vertical and y < center_horizontal:
            quadrants[1] += 1
        if x < center_vertical and y > center_horizontal:
            quadrants[2] += 1
        if x > center_vertical and y > center_horizontal:
            quadrants[3] += 1
    part1 = reduce(mul, quadrants)

    part2 = 0
    while True:
        for robot in robots:
            robot[0] = (robot[0] + robot[2]) % width
            robot[1] = (robot[1] + robot[3]) % height
        part2 += 1
        if part2 == 7847:
        #if (part2 - 69) % 101 == 0:
            for y in range(height):
                for x in range(width):
                    found_robot = False
                    for robot in robots:
                        if robot[0] == x and robot[1] == y:
                            print('#', end='')
                            found_robot = True
                            break
                    if not found_robot:
                        print(" ", end='')
                print()
            #print(part2)
            #input()
            break
        
    return part1, part2

aoc.run_lines(main, "day14.txt")
