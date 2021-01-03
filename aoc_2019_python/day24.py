import aoc
from collections import defaultdict

def main(input_lines):
    grid = defaultdict(lambda : False)
    for y, line in enumerate(input_lines):
        for x, c in enumerate(line.strip()):
            grid[(x, y, 0)] = c == "#"
    
    part1 = do_part1(grid)
    part2 = do_part2(grid)
    return part1, part2
    
def do_part1(grid):
    seen = set()
    while True:
        biodiversity = 0
        for y in range(5):
            for x in range(5):
                if grid[(x, y, 0)]:
                    biodiversity += 2 ** (x + y * 5)
        if biodiversity in seen:
            break
        seen.add(biodiversity)
        newGrid = defaultdict(lambda : False)
        
        for y in range(5):
            for x in range(5):
                count = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    count += grid[(x + dx, y + dy, 0)]
                # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
                if grid[(x, y, 0)] and count != 1:
                    newGrid[(x, y, 0)] = False
                # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
                elif not grid[(x, y, 0)] and count in [1, 2]:
                    newGrid[(x, y, 0)] = True
                # Otherwise, a bug or empty space remains the same.
                else:
                    newGrid[(x, y, 0)] = grid[(x, y, 0)]
        grid = newGrid.copy()
    
    return biodiversity

def do_part2(grid):
    lowest = 0
    highest = 0
    for _ in range(200):
        newGrid = defaultdict(lambda : False)
        for level in range(lowest - 1, highest + 2):
            for y in range(5):
                for x in range(5):
                    if x == 2 and y == 2:
                        continue
                    count = 0
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx = x + dx
                        ny = y + dy
                        # Count the outer grid
                        if nx < 0 or ny < 0 or nx >= 5 or ny >= 5:
                            count += grid[(2 + dx, 2 + dy, level - 1)]
                        # Count the inner grid
                        elif nx == 2 and ny == 2:
                            if dx < 0:
                                count += sum(grid[(4, yy, level + 1)] for yy in range(5))
                            elif dy < 0:
                                count += sum(grid[(xx, 4, level + 1)] for xx in range(5))
                            elif dx > 0:
                                count += sum(grid[(0, yy, level + 1)] for yy in range(5))
                            elif dy > 0:
                                count += sum(grid[(xx, 0, level + 1)] for xx in range(5))
                        # No level change
                        else:
                            count += grid[(x + dx, y + dy, level)]
                    if count > 0:
                        highest = max(highest, level)
                        lowest = min(lowest, level)

                    # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
                    if grid[(x, y, level)] and count != 1:
                        newGrid[(x, y, level)] = False
                    # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
                    elif not grid[(x, y, level)] and count in [1, 2]:
                        newGrid[(x, y, level)] = True
                    # Otherwise, a bug or empty space remains the same.
                    else:
                        newGrid[(x, y, level)] = grid[(x, y, level)]
        grid = newGrid.copy()
    
    part2 = len([x for x in grid.values() if x])
    return part2

aoc.run_lines(main, "day24.txt")