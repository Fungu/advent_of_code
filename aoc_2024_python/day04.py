import aoc

def main(lines: list):
    part1 = 0
    part2 = 0

    neighbors = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    diagonals = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    maxX = len(lines[0].strip())
    maxY = len(lines)
    
    for y in range(maxY):
        for x in range(maxX):
            part1 += findWord(lines, neighbors + diagonals, x, y, maxX, maxY, "XMAS", 0)
            if findWord(lines, diagonals, x, y, maxX, maxY, "MAS", -1) == 2:
                part2 += 1

    return part1, part2

def findWord(lines, directions, x, y, maxX, maxY, word, offset):
    ret = 0
    for dir in directions:
        foundError = False
        for i, c in enumerate(word):
            xx = x + (i + offset) * dir[0]
            yy = y + (i + offset) * dir[1]
            if xx < 0 or yy < 0 or xx >= maxX or yy >= maxY or lines[yy][xx] != c:
                foundError = True
                break
        if not foundError:
            ret += 1
    return ret


aoc.run_lines(main, "day04.txt")
