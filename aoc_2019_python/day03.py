import aoc

def main(input_lines):
    visitedA = {}
    visitedB = {}
    part1 = float("inf")
    part2 = float("inf")

    delta = {
        'U':[ 0,-1],
        'R':[ 1, 0],
        'D':[ 0, 1],
        'L':[-1, 0],
    }

    for line in input_lines:
        pos = [0, 0]
        distance = 0
        for element in line.split(","):
            for _ in range(int(element[1:])):
                dirChar = element[0]
                pos[0] += delta[dirChar][0]
                pos[1] += delta[dirChar][1]
                
                key = tuple(pos)
                distance += 1
                
                visitedA[key] = visitedA.get(key, distance)

                if key in visitedB.keys():
                    part1 = min(part1, abs(pos[0]) + abs(pos[1]))
                    part2 = min(part2, visitedA[key] + visitedB[key])

        visitedB = visitedA
        visitedA = {}

    return part1, part2    

aoc.run_lines(main, "day03.txt")