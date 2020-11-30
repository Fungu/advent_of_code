import io
#import itertools
import math
import sys
import datetime
 
start = datetime.datetime.now()
with open("input/day10.txt") as infile:
    raw_data = infile.read().strip()
    x_pos = 0
    y_pos = 0
    asteroids = {}
    max_visible = 0
    for c in raw_data:
        if c == '#':
            asteroids[(x_pos, y_pos)] = []
        if c == '\n':
            x_pos = 0
            y_pos += 1
        else:
            x_pos += 1
    for a in asteroids:
        ax, ay = a
        visible_from_a = []
        for b in asteroids:
            if b != a:
                is_visible = True
                bx, by = b
                x_diff = bx - ax
                y_diff = by - ay
                gcd = math.gcd(x_diff, y_diff)
                for i in range(1, gcd):
                    if (ax + i * x_diff // gcd, ay + i * y_diff // gcd) in asteroids:
                        is_visible = False
                        break
                if is_visible:
                    visible_from_a += [b]
        asteroids[a] = visible_from_a
        if len(visible_from_a) > max_visible:
            max_visible = len(visible_from_a)
            best_pos = a
print("Best position is {} with {} asteroids visible.".format(best_pos, max_visible))
 
base_x, base_y = best_pos
laser_targets = {}
for a in asteroids[best_pos]:
    ax, ay = a
    x_diff = ax - base_x
    y_diff = ay - base_y
    angle = - math.atan2(x_diff, y_diff) + math.pi
    laser_targets[angle] = a
 
[print(t) for i, (a, t) in enumerate(sorted(laser_targets.items()), 1) if i == 200]

print(datetime.datetime.now() - start)