import aoc
import re

def main(inputBlob):
    tileDict = {}
    for rawTile in inputBlob.split("\n\n"):
        lines = rawTile.splitlines()
        tileDict[lines[0].split()[1].replace(":", "")] = lines[1:]

    assembledGrid, tilePositions = assemble(tileDict)
    
    minX = min([x for x, y in tilePositions.keys()])
    maxX = max([x for x, y in tilePositions.keys()])
    minY = min([y for x, y in tilePositions.keys()])
    maxY = max([y for x, y in tilePositions.keys()])
    part1 = int(tilePositions[(minX, minY)]) * int(tilePositions[(maxX, minY)]) * int(tilePositions[(minX, maxY)]) * int(tilePositions[(maxX, maxY)])

    for _ in range(4):
        assembledGrid = rotate(assembledGrid, 1)
        found, roughness = findSeaMonsters(assembledGrid)
        if found:
            part2 = roughness
        assembledGrid = flip(assembledGrid, True)
        found, roughness = findSeaMonsters(assembledGrid)
        if found:
            part2 = roughness

    return part1, part2

def getEdges(tile):
    """0->up, 1->left, 2->down, 3->right"""

    edges = []
    edges.append(tile[0])
    edges.append("".join([tile[i][0] for i in range(0, len(tile))])[::-1])
    edges.append(tile[-1][::-1])
    edges.append("".join([tile[i][-1] for i in range(0, len(tile))]))

    return edges

def rotate(tile, rotation):
    """rotation: 0->default, 1->90deg ccw, 2->180deg ccw, 3->270deg ccw"""

    for _ in range(rotation):
        newTile = []
        for column in range(len(tile[0])):
            newTile.append("".join([tile[i][len(tile[0]) - column - 1] for i in range(len(tile))]))
        tile = newTile
    return tile

def flip(tile, horizontal):
    if horizontal:
        newTile = []
        for line in tile:
            newTile.append(line[::-1])
    else:
        newTile = tile[::-1]
    return newTile

def assemble(tileDict):
    startTileId = list(tileDict.keys())[0]
    directionDict = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3: (1, 0)}

    # key=position, value=tileId
    tilePositions = {}
    tilePositions[(0, 0)] = startTileId
    openSet = set()
    openSet.add((0, 0))
    while openSet:
        currentPosition = openSet.pop()
        currentTileId = tilePositions[currentPosition]
        currentEdges = getEdges(tileDict[currentTileId])
        for otherId, otherTile in tileDict.items():
            if otherId in tilePositions.values():
                continue
            otherEdges = getEdges(otherTile)
            for direction, edgeA in enumerate(currentEdges):
                for otherDirection, edgeB in enumerate(otherEdges):
                    match = False
                    needsFlip = False
                    if edgeA == edgeB:
                        match = True
                        needsFlip = True
                    if edgeA == edgeB[::-1]:
                        match = True
                    if match:
                        dX, dY = directionDict[direction]
                        position = (currentPosition[0] + dX, currentPosition[1] + dY)
                        if position not in tilePositions:
                            relativeRotation = direction - otherDirection + 2
                            if relativeRotation < 0:
                                relativeRotation += 4
                            otherTile = rotate(otherTile, relativeRotation)
                            if needsFlip:
                                otherTile = flip(otherTile, direction in [0, 2])
                            tileDict[otherId] = otherTile
                            tilePositions[position] = otherId
                            openSet.add(position)
    
    minX = min([x for x, y in tilePositions.keys()])
    maxX = max([x for x, y in tilePositions.keys()])
    minY = min([y for x, y in tilePositions.keys()])
    maxY = max([y for x, y in tilePositions.keys()])

    assempledGrid = []
    for y in range(minY, maxY + 1):
        for innerY in range(1, len(tileDict[startTileId]) - 1):
            line = ""
            for x in range(minX, maxX + 1):
                otherTile = tileDict[tilePositions[(x, y)]]
                line += otherTile[innerY][1:-1]
            assempledGrid.append(line)
    assempledGrid = flip(assempledGrid, False)
    return assempledGrid, tilePositions

def findSeaMonsters(grid):
    seaMonster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]
    
    seaMonsterMatch = []
    seaMonsterMatch.append(re.compile("(?=(" + seaMonster[0].replace(" ", ".") + "))"))
    seaMonsterMatch.append(re.compile("(?=(" + seaMonster[1].replace(" ", ".") + "))"))
    seaMonsterMatch.append(re.compile("(?=(" + seaMonster[2].replace(" ", ".") + "))"))

    seaMonsterCount = 0
    for row in range(len(grid) - len(seaMonsterMatch)):
        matches = []
        for patternIndex in range(len(seaMonsterMatch)):
            innerMatches = []
            for m in seaMonsterMatch[patternIndex].findall(grid[row + patternIndex]):
                innerMatches.append(grid[row + patternIndex].index(m))
            matches.append(innerMatches)
        for matchIndex in matches[0]:
            if matchIndex in matches[1] and matchIndex in matches[2]:
                seaMonsterCount += 1
    hashCount = sum([row.count("#") for row in grid])
    seaMonsterSize = sum([row.count("#") for row in seaMonster])

    return seaMonsterCount != 0, hashCount - seaMonsterSize * seaMonsterCount

aoc.runRaw(main, "day20.txt")