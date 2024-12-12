import aoc

def main(lines: list):
    part1 = 0
    part2 = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    regions = []
    closed_set = set()
    range_x = range(len(lines[0]))
    range_y = range(len(lines))
    for y in range_y:
        for x in range_x:
            if (x, y) in closed_set:
                continue
            open_set = [(x, y)]
            region = []
            while open_set:
                pos = open_set.pop()
                closed_set.add(pos)
                region.append(pos)
                for dir in directions:
                    xx = pos[0] + dir[0]
                    yy = pos[1] + dir[1]
                    if xx in range_x and yy in range_y and (xx, yy) not in closed_set and (xx, yy) not in region and (xx, yy) not in open_set and lines[yy][xx] == lines[y][x]:
                        open_set.append((xx, yy))
            regions.append(region)

    for i, region in enumerate(regions):
        area = len(region)
        parameter = 0
        sides = 0
        counted_side_segments = set()
        for pos in region:
            for dir in directions:
                if (pos[0] + dir[0], pos[1] + dir[1]) not in region:
                    parameter += 1
                    
                    if (pos, dir) not in counted_side_segments:
                        sides += 1
                        if dir[0] == 0:
                            side_dirs = [(1, 0), (-1, 0)]
                        else:
                            side_dirs = [(0, 1), (0, -1)]
                        for side_dir in side_dirs:
                            i = 0
                            while True:
                                side_pos = (pos[0] + i * side_dir[0], pos[1] + i * side_dir[1])
                                if side_pos not in region or (side_pos[0] + dir[0], side_pos[1] + dir[1]) in region:
                                    break
                                counted_side_segments.add((side_pos, dir))
                                i += 1

        part1 += area * parameter
        part2 += area * sides
    
    return part1, part2


aoc.run_lines(main, "day12.txt")
