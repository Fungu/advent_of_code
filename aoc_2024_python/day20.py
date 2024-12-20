import aoc

def main(lines: list):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)
    
    path = []
    pos = start
    while True:
        path.append(pos)
        if pos == end:
            break
        for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = (pos[0] + dir[0], pos[1] + dir[1])
            if lines[neighbor[1]][neighbor[0]] != "#" and (len(path) < 2 or neighbor != path[-2]):
                pos = neighbor
                break
    
    part1 = 0
    part2 = 0
    for a, start in enumerate(path):
        for b in range(a + 101, len(path)):
            end = path[b]
            cheat_distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
            saved_distance = b - a - cheat_distance
            if cheat_distance <= 2 and saved_distance >= 100:
                part1 += 1
            if cheat_distance <= 20 and saved_distance >= 100:
                part2 += 1

    return part1, part2

aoc.run_lines(main, "day20.txt")
