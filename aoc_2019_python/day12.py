import aoc
import math
import copy
import re

class Moon:
    pos = []
    vel = []

    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0, 0]
    
    def update_vel(self, moons1):
        for moon in moons1:
            for i in range(3):
                delta = self.pos[i] - moon.pos[i]
                self.vel[i] += (1 if delta < 0 else (-1 if delta > 0 else 0))
    
    def update_pos(self):
        for i in range(3):
            self.pos[i] += self.vel[i]
    
    def calculate_energy(self):
        potential = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        kinetic = abs(self.vel[0]) + abs(self.vel[1]) + abs(self.vel[2])
        return potential * kinetic

    def print_moon(self):
        print("pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(self.pos[0], self.pos[1], self.pos[2], self.vel[0], self.vel[1], self.vel[2]))
    
    def has_stopped(self, axis):
        return self.vel[axis] == 0

def main(input_lines):
    regex = re.compile(r"<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>")
    moons1 = [Moon([int(a) for a in regex.search(line).groups()]) for line in input_lines]
    moons2 = copy.deepcopy(moons1)
    
    for _ in range(0, 1000):
        for moon in moons1:
            moon.update_vel(moons1)
        for moon in moons1:
            moon.update_pos()
    part1 = sum(moon.calculate_energy() for moon in moons1)

    iterations = [0, 0, 0]
    axis_remaining = [0, 1, 2]
    while len(axis_remaining) > 0:
        remove = []
        for axis in axis_remaining:
            if iterations[axis] > 0 and all([moon.has_stopped(axis) for moon in moons2]):
                remove.append(axis)
                iterations[axis] *= 2
            else:
                iterations[axis] += 1
        for r in remove:
            axis_remaining.remove(r)

        for moon in moons2:
            moon.update_vel(moons2)
        for moon in moons2:
            moon.update_pos()
    lcm = (iterations[0] * iterations[1]) // math.gcd(iterations[0], iterations[1])
    part2 = (lcm * iterations[2]) // math.gcd(lcm, iterations[2])

    return part1, part2

aoc.run_lines(main, "day12.txt")