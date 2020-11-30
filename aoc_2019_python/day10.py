import math
import datetime

def main():
    start = datetime.datetime.now()
    with open("input/day10.txt") as file:
        # grid becomes transposed :(
        grid = [[char.strip() == "#" for char in line.strip()] for line in file.readlines()]
    asteroids = {}
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y]:
                asteroids[(y, x)] = True
    
    part1 = 0
    for current in asteroids:
        nrSeen = 0
        for target in asteroids:
            if canSee(asteroids, current, target):
                nrSeen += 1
        if nrSeen > part1:
            part1 = nrSeen
            lazerPos = current
    print("part 1:", part1, part1 == 247)

    for current in asteroids:
        asteroids[current] = math.atan2(lazerPos[1] - current[1], lazerPos[0] - current[0]) - math.pi / 2
        if asteroids[current] < 0:
            asteroids[current] += math.pi * 2
    
    destroyed = 0
    asteroids = {k: v for k, v in sorted(asteroids.items(), key=lambda item: item[1])}
    for pos in asteroids:
        if canSee(asteroids, lazerPos, pos):
            destroyed += 1
            if destroyed == 200:
                part2 = pos[0] * 100 + pos[1]
                break
    print("part 2:", part2, part2 == 1919)
    print(datetime.datetime.now() - start)

def canSee(asteroids, current, target):
    if current != target:
        dx = target[0] - current[0]
        dy = target[1] - current[1]
        steps = math.gcd(dx, dy)
        dx //= steps
        dy //= steps

        x = current[0]
        y = current[1]
        for _ in range(steps - 1):
            x += dx
            y += dy
            if (x, y) in asteroids:
                return False
        return True
    else:
        return False

main()