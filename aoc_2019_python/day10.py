import aoc
import math
import itertools

def main(input_lines):
    asteroids = {(x, y) : 0 for x, y in itertools.product(range(len(input_lines)), range(len(input_lines[0].strip()))) if input_lines[y][x] == "#"}
    
    part1 = 0
    for current in asteroids:
        seen_count = 0
        for target in asteroids:
            if can_see(asteroids, current, target):
                seen_count += 1
        if seen_count > part1:
            part1 = seen_count
            lazer_pos = current

    for current in asteroids:
        asteroids[current] = math.atan2(lazer_pos[1] - current[1], lazer_pos[0] - current[0]) - math.pi / 2
        if asteroids[current] < 0:
            asteroids[current] += math.pi * 2
    
    destroyed = 0
    asteroids = {k : v for k, v in sorted(asteroids.items(), key=lambda item: item[1])}
    for pos in asteroids:
        if can_see(asteroids, lazer_pos, pos):
            destroyed += 1
            if destroyed == 200:
                part2 = pos[0] * 100 + pos[1]
                break
    
    print("part 1:", part1, part1 == 247)
    print("part 2:", part2, part2 == 1919)

    return part1, part2

def can_see(asteroids, current, target):
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

aoc.run_lines(main, "day10.txt")