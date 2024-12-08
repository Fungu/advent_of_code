import aoc

def main(lines: list):
    rangeX = range(len(lines[0]))
    rangeY = range(len(lines))

    antennas = {}
    for y in rangeY:
        for x in rangeX:
            freq = lines[y][x]
            if freq != ".":
                antennas.setdefault(freq, [])
                antennas[freq].append({"x": x, "y": y})

    antinode_locations = set()
    harmonics_antinode_locations = set()
    for freq, pos_list in antennas.items():
        for p1 in pos_list:
            for p2 in pos_list:
                if p1 == p2:
                    continue
                
                dx = p1["x"] - p2["x"]
                dy = p1["y"] - p2["y"]
                
                x = p1["x"] + dx
                y = p1["y"] + dy
                if x in rangeX and y in rangeY:
                    antinode_locations.add((x, y))
                
                i = 0
                while True:
                    x = p1["x"] + dx * i
                    y = p1["y"] + dy * i
                    i += 1
                    if x not in rangeX or y not in rangeY:
                        break
                    harmonics_antinode_locations.add((x, y))

    part1 = len(antinode_locations)
    part2 = len(harmonics_antinode_locations)

    return part1, part2

aoc.run_lines(main, "day08.txt")
