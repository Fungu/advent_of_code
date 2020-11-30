import datetime
import math
import copy

class Moon:
    pos = []
    vel = []

    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0, 0]
    
    def updateVel(self, moons):
        for moon in moons:
            for i in range(3):
                delta = self.pos[i] - moon.pos[i]
                self.vel[i] += (1 if delta < 0 else (-1 if delta > 0 else 0))
    
    def updatePos(self):
        for i in range(3):
            self.pos[i] += self.vel[i]
    
    def calculateEnergy(self):
        potential = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        kinetic = abs(self.vel[0]) + abs(self.vel[1]) + abs(self.vel[2])
        return potential * kinetic

    def printMoon(self):
        print("pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(self.pos[0], self.pos[1], self.pos[2], self.vel[0], self.vel[1], self.vel[2]))
    
    def hasStopped(self, axis):
        return self.vel[axis] == 0

def main():
    with open("input/day12.txt") as file:
        lines = [line.replace("<", "").replace(">", "").strip() for line in file.readlines()]
        moons = [Moon([int(b.strip()[2:]) for b in a.split(",")]) for a in lines]
        moonsTemp = copy.deepcopy(moons)
    
    for _ in range(0, 1000):
        for moon in moons:
            moon.updateVel(moons)
        for moon in moons:
            moon.updatePos()
    part1 = sum(moon.calculateEnergy() for moon in moons)
    print("part 1:", part1, part1 == 7077)


    moons = moonsTemp
    iterations = [0, 0, 0]
    axisLeft = [0, 1, 2]
    while len(axisLeft) > 0:
        remove = -1
        for axis in axisLeft:
            stopped = True
            for moon in moons:
                stopped = stopped & moon.hasStopped(axis)
            if stopped and iterations[axis] > 0:
                remove = axis
                iterations[axis] *= 2
                print("repeat after", iterations[axis])
            else:
                iterations[axis] += 1
        if remove != -1:
            axisLeft.remove(remove)

        for moon in moons:
            moon.updateVel(moons)
        for moon in moons:
            moon.updatePos()
    lcm = (iterations[0] * iterations[1]) // math.gcd(iterations[0], iterations[1])
    part2 = (lcm * iterations[2]) // math.gcd(lcm, iterations[2])
    print("part 2:", part2, part2 == 402951477454512)
    

start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)