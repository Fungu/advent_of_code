import aoc

def main(lines: list):
    part1 = 0
    part2 = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    range_x = range(len(lines[0]))
    range_y = range(len(lines))
    for y in range_y:
        for x in range_x:
            if lines[y][x] == "0":
                open_set = []
                open_set.append((x, y))
                closed_set = set()
                while open_set:
                    current_position = open_set.pop()
                    for direction in directions:
                        xx = current_position[0] + direction[0]
                        yy = current_position[1] + direction[1]
                        if xx in range_x and yy in range_y and int(lines[yy][xx]) == int(lines[current_position[1]][current_position[0]]) + 1:
                            if lines[yy][xx] == "9":
                                part2 += 1
                                if (xx, yy) not in closed_set:
                                    part1 += 1
                                closed_set.add((xx, yy))
                            else:
                                open_set.append((xx, yy))
                

    return part1, part2


aoc.run_lines(main, "day10.txt")
