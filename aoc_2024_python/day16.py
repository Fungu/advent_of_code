import aoc

def main(lines: list):
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
            if c == "E":
                end = (x, y)

    part1 = None
    open_set = [(start, (1, 0), 0, [start])]
    closed_set = set()
    on_best_path = set()
    while len(open_set) > 0:
        pos, dir, score, path = open_set.pop(0)
        if part1 != None and part1 < score:
            break
        
        if pos == end:
            part1 = score
            for p in path:
                on_best_path.add(p)
        
        # This breaks part 2.
        # TODO: Make a solution that saves the number of best paths to each position+direction
        #if (pos, dir) in closed_set:
            #continue
        closed_set.add((pos, dir))
        
        forward = (pos[0] + dir[0], pos[1] + dir[1])
        if lines[forward[1]][forward[0]] != "#" and (forward, dir) not in closed_set:
            open_set.append((forward, dir, score + 1, path + [forward]))
        right = (-dir[1], dir[0])
        left = (dir[1], -dir[0])
        
        if (pos, right) not in closed_set:
            open_set.append((pos, right, score + 1000, path))
        if (pos, left) not in closed_set:
            open_set.append((pos, left, score + 1000, path))
        
        open_set.sort(key=sortfunc)
    part2 = len(on_best_path)

    return part1, part2

def sortfunc(e):
  return e[2]


aoc.run_lines(main, "day16.txt")
