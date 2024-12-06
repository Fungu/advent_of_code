import aoc

def main(lines: list):
    for y, line in enumerate(lines):
        x = line.find("^")
        if x >= 0:
            pos = (x, y)
            break

    visited_positions, obstruction_positions = simulate(lines, pos, (0, -1), None)
    part1 = len(visited_positions)
    part2 = len(obstruction_positions)
    
    return part1, part2

def simulate(lines, pos, dir, obstruction):
    range_x = range(len(lines[0]))
    range_y = range(len(lines))
    obstacle_posistions = set()
    obstruction_positions = set()
    loop_detection = set()

    while True:
        obstruction_positions.add(pos)
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])
        if next_pos[0] not in range_x or next_pos[1] not in range_y:
            break
        if lines[next_pos[1]][next_pos[0]] == "#" or next_pos == obstruction:
            dir = (-dir[1], dir[0])
        else:
            if obstruction:
                if (pos, dir) in loop_detection:
                    return None, True
                loop_detection.add((pos, dir))
            elif next_pos not in obstruction_positions:
                _, found_loop = simulate(lines, pos, dir, next_pos)
                if found_loop:
                    obstacle_posistions.add(next_pos)
            pos = next_pos
    return obstruction_positions, obstacle_posistions

aoc.run_lines(main, "day06.txt")
