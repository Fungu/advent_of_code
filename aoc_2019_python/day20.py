import time
from collections import defaultdict
import networkx as nx

def main():
    area = defaultdict(lambda : "#")
    width = 0
    height = 0
    with open("input/day20.txt") as file:
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                area[(x, y)] = c
                width = max(width, x)
            height = max(height, y)
    
    for y in range(height):
        for x in range(width):
            c = area[(x, y)]
            if c.isupper():
                isEntrance = False
                for xx, yy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    dc = area[(x + xx, y + yy)]
                    if dc.isupper():
                        if xx > 0 or yy > 0:
                            key = c + dc
                        else:
                            key = dc + c
                    if dc == ".":
                        isEntrance = True
                if isEntrance:
                    area[(x, y)] = key
                    if key == "AA":
                        startPos = findAdjacent(area, (x, y))
                    if key == "ZZ":
                        endPos = findAdjacent(area, (x, y))
    
    graph = nx.Graph()
    for y in range(height - 1):
        for x in range(width - 1):
            if area[(x, y)] == "." or isPortal(area[(x, y)]):
                if area[(x + 1, y)] == "." or isPortal(area[(x + 1, y)]):
                    graph.add_edge((x, y), (x + 1, y))
                if area[(x, y + 1)] == "." or isPortal(area[(x, y + 1)]):
                    graph.add_edge((x, y), (x, y + 1))
            if isPortal(area[(x, y)]) and area[(x, y)] != "AA" and area[(x, y)] != "ZZ":
                a = findAdjacent(area, (x, y))
                b = findAdjacent(area, findOtherSide(area, (x, y)))
                graph.add_edge(a, b)
    part1 = nx.shortest_path_length(graph, startPos, endPos)
    print("part 1", part1, part1 == 684)

    graph = nx.Graph()
    for level in range(30):
        for y in range(height - 1):
            for x in range(width - 1):
                if area[(x, y)] == "." or isPortal(area[(x, y)]):
                    if area[(x + 1, y)] == "." or isPortal(area[(x + 1, y)]):
                        graph.add_edge((x, y, level), (x + 1, y, level))
                    if area[(x, y + 1)] == "." or isPortal(area[(x, y + 1)]):
                        graph.add_edge((x, y, level), (x, y + 1, level))
                if isPortal(area[(x, y)]) and area[(x, y)] != "AA" and area[(x, y)] != "ZZ":
                    levelChange = 1 if 2 < x < width - 2 and 2 < y < height - 2 else -1
                    a = findAdjacent(area, (x, y))
                    b = findAdjacent(area, findOtherSide(area, (x, y)))
                    graph.add_edge((a[0], a[1], level), (b[0], b[1], level + levelChange))
    part2 = nx.shortest_path_length(graph, (startPos[0], startPos[1], 0), (endPos[0], endPos[1], 0))
    print("part 2", part2, part2 == 7758)
    
    
def isPortal(cell):
    return cell.isupper() and len(cell) == 2

def findAdjacent(area, pos):
    for xx, yy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        testPos = (pos[0] + xx, pos[1] + yy)
        if area[testPos] == ".":
            return testPos

def findOtherSide(area, pos):
    for key, value in area.items():
        if key != pos and value == area[pos]:
            return key
    print("findOtherSide", area[pos], pos)



start = time.time()
main()
print(time.time() - start)