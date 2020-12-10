import aoc
import functools

def main(inputLines):
    boardingpassList = [getBoardingpass(line) for line in inputLines]
    
    part1 = functools.reduce(lambda a, b: a if a[2] > b[2] else b, boardingpassList)[2]
    part2 = findEmptySeat(boardingpassList)
    
    return part1, part2

def getBoardingpass(line):
    row = int(line[:7].replace("F", "0").replace("B", "1"), 2)
    column = int(line[7:].replace("L", "0").replace("R", "1"), 2)
    return row, column, getSeatId(row, column)

def findEmptySeat(boardingpassList):
    for row in range(0, 128):
        if all(((row, column, getSeatId(row, column)) in boardingpassList) for column in range(0, 8)):
            startRow = row + 1
            break
    for row in range(startRow, 128):
        for column in range(0, 8):
            seatId = getSeatId(row, column)
            if (row, column, seatId) not in boardingpassList:
                return seatId

def getSeatId(row, column):
    return row * 8 + column

aoc.runLines(main, "day05.txt")