import intcode
import time
import astar
from collections import defaultdict

def main():
    with open("input/day15.txt") as file:
        memory = [int(val) for val in file.read().split(",")]

    #north (1), south (2), west (3), and east (4).
    dirToInput = {
        ( 0,-1): 1,
        ( 0, 1): 2,
        (-1, 0): 3,
        ( 1, 0): 4,
    }
    openStack = list(dirToInput.keys())
    area = defaultdict(lambda : -1)
    pos = (0, 0)
    area[pos] = 1
    ip = 0
    relativeBase = 0
    while len(openStack) > 0:
        pathList = astar.astar(area, pos, openStack.pop())[1:]

        for path in pathList:
            if path in openStack:
                openStack.remove(path)

            direction = dirToInput[(path[0] - pos[0], path[1] - pos[1])]
            output = []
            ip, _, relativeBase = intcode.runProgram(memory, [direction], output, ip, relativeBase)
            
            area[path] = output[0]
            #0: The repair droid hit a wall. Its position has not changed.
            if output[0] == 0:
                pathList.clear()
            #1: The repair droid has moved one step in the requested direction.
            elif output[0] == 1:
                pos = path
            #2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
            elif output[0] == 2:
                oxygenPos = path
                pos = path

            for testDir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                testPos = (pos[0] + testDir[0], pos[1] + testDir[1])
                if area[testPos] == -1 and testPos not in openStack:
                    openStack.append(testPos)

    #printGrid(area, pos)
    part1 = len(astar.astar(area, (0, 0), oxygenPos)) - 1
    print("part 1:", part1, part1 == 280)
    
    nextOpenSet = set()
    nextOpenSet.add(oxygenPos)
    closedSet = set()
    part2 = -1
    while len(nextOpenSet) > 0 and len(nextOpenSet) < 2000:
        part2 += 1
        openSet = nextOpenSet
        nextOpenSet = set()
        for pos in openSet:
            closedSet.add(pos)
            for testDir in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                testPos = (pos[0] + testDir[0], pos[1] + testDir[1])
                if area[(testPos[0], testPos[1])] <= 0:
                    continue
                if testPos in closedSet or testPos in openSet or testPos in nextOpenSet:
                    continue
                nextOpenSet.add(testPos)
    print("part 2:", part2, part2 == 400)

def printGrid(area, pos):
    lowBounds = [0, 0]
    highBounds = [0, 0]
    for a in area:
        lowBounds[0] = min(lowBounds[0], a[0])
        lowBounds[1] = min(lowBounds[1], a[1])
        highBounds[0] = max(highBounds[0], a[0])
        highBounds[1] = max(highBounds[1], a[1])
    for y in range(lowBounds[1], highBounds[1] + 1):
        for x in range(lowBounds[0], highBounds[0] + 1):
            if pos[0] == x and pos[1] == y:
                print("X", end = '')
            elif x == 0 and y == 0:
                print("S", end = '')
            elif area[(x, y)] == 0:
                print("#", end = '')
            elif area[(x, y)] == 1:
                print(".", end = '')
            elif area[(x, y)] == 2:
                print("O", end = '')
            elif area[(x, y)] == -1:
                print(" ", end = '')
        print("")

start = time.time()
main()
print(time.time() - start)