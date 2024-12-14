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

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    part2 = 0
    while True:
        positions = set()
        
        # Step the robots
        for robot in robots:
            robot[0] = (robot[0] + robot[2]) % width
            robot[1] = (robot[1] + robot[3]) % height
            positions.add((robot[0], robot[1]))
        part2 += 1
        
        # Find the average x-position among robots that has neighbors
        x_sum = 0
        x_num = 0
        for robot in robots:
            neighbors = False
            for dir in directions:
                if (robot[0] + dir[0], robot[1] + dir[1]) in positions:
                    neighbors = True
                    break
            if neighbors:
                x_sum += robot[0]
                x_num += 1
        if x_num == 0:
            continue
        x_avg = x_sum / x_num

        # Check if at least half the robots have a mirrored robot
        mirrored_robots = 0
        for robot in robots:
            if (2 * int(x_avg) - robot[0], robot[1]) in positions:
                mirrored_robots += 1
        if mirrored_robots / len(robots) >= 0.5:
            break
        
    return part1, part2

aoc.run_lines(main, "day14.txt")
