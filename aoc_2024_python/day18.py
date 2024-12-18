import aoc

def main(lines: list):
    part1 = None
    part2 = None

    grid_size = 70
    blockers = []
    for line in lines:
        a = line.split(",")
        blockers.append((int(a[0]), int(a[1])))
    
    path = dfs(blockers[:1024], grid_size)
    part1 = len(path)
    

    for nr_of_bytes in range(1024, len(lines)):
        if blockers[nr_of_bytes - 1] in path:
            path = dfs(blockers[:nr_of_bytes], grid_size)
        if not path:
            part2 = ",".join([str(a) for a in blockers[nr_of_bytes - 1]])
            break

    return part1, part2

def dfs(blockers, grid_size):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    grid_range = range(grid_size + 1)
    
    open_set = [((0, 0), [])]
    closed_set = set()
    closed_set.add((0, 0))
    while open_set:
        pos, path = open_set.pop(0)
        if pos == (grid_size, grid_size):
            return path
        
        for dir in directions:
            pn = (pos[0] + dir[0], pos[1] + dir[1])
            if pn[0] in grid_range and pn[1] in grid_range and pn not in blockers and pn not in closed_set and pn not in open_set:
                open_set.append((pn, path + [pn]))
                closed_set.add(pn)
    return False

aoc.run_lines(main, "day18.txt")
