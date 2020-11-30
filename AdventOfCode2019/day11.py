import intcode
import datetime
import cmath
from collections import defaultdict

def main():
    with open("input/day11.txt") as file:
        memory = [int(val) for val in file.read().split(",")]
    memory += [0] * 1000
    
    paint = defaultdict(lambda : 0)
    calculatePaint(memory.copy(), paint)
    part1 = len(paint)

    paint = defaultdict(lambda : 0)
    paint[0] = 1
    xMin, xMax, yMin, yMax = calculatePaint(memory.copy(), paint)
    
    print("part 1:", part1, part1 == 1964)
    print("part 2:")
    for y in range(yMin, yMax + 1):
        for x in range(xMin, xMax + 1):
            if paint[x + y * 1j] == 1:
                print("#", end = '')
            else:
                print(" ", end = '')
        print("")

def calculatePaint(memory, paint):
    xMin = yMin = 1000
    xMax = yMax = -1000
    pos = 0
    facing = -1j

    ip = 0
    finished = False
    relativeBase = 0
    while finished == False:
        output = []
        ip, finished, relativeBase = intcode.runProgram(memory, [paint[pos]], output, ip, relativeBase)
        paint[pos] = output[0]
        facing *= (1j if output[1] == 1 else -1j)
        pos += facing
        xMin = min(xMin, pos.real)
        xMax = max(xMax, pos.real)
        yMin = min(yMin, pos.imag)
        yMax = max(yMax, pos.imag)
    return int(xMin), int(xMax), int(yMin), int(yMax)

start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)