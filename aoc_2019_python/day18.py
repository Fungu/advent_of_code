import aoc
from collections import deque

def main(input_lines):
    part1 = do_part1(input_lines)
    part2 = do_part2(input_lines)
    return part1, part2

def do_part1(input_lines):
    area = {}
    keys = {}
    width = 0
    height = 0
    for y, line in enumerate(input_lines):
        for x, c in enumerate(line.strip()):
            area[(x, y)] = c.strip()
            width = max(width, x)
        height = max(height, y)
    
    for x in range(width):
        for y in range(height):
            if area[(x, y)].islower() or area[(x, y)] == "@":
                keys[area[(x, y)]] = (x, y)
    
    key_dict = djikstra(area, keys)
    
    part1 = 1000000
    seen = {}
    nodes = deque()
    nodes.append(("@", "@", 0))
    while len(nodes) > 0:
        current_key, seen_keys, distance = nodes.popleft()
        
        if len(seen_keys) == len(keys):
            part1 = min(part1, distance)
        
        for k, (kdistance, doors) in key_dict[current_key].items():
            if k in seen_keys:
                continue
            if any(b not in seen_keys for b in doors):
                continue

            nk = "".join(sorted(seen_keys + k))
            ndistance = distance + kdistance
            new_node = (k, nk, ndistance)
            if (k, nk) not in seen or seen[(k, nk)] > ndistance:
                seen[(k, nk)] = ndistance
                nodes.append(new_node)

    return part1

def do_part2(input_lines):
    area = {}
    keys = {}
    width = 0
    height = 0
    for y, line in enumerate(input_lines):
        for x, c in enumerate(line.strip()):
            area[(x, y)] = c.strip()
            width = max(width, x)
        height = max(height, y)
    
    w = int(width / 2)
    h = int(height / 2)
    for a in [-1, 0, 1]:
        area[(w + a, h)] = "#"
        area[(w, h + a)] = "#"
    area[(w + 1, h + 1)] = "0"
    area[(w + 1, h - 1)] = "1"
    area[(w - 1, h + 1)] = "2"
    area[(w - 1, h - 1)] = "3"
    

    for x in range(width):
        for y in range(height):
            if area[(x, y)].islower() or area[(x, y)] in "0123":
                keys[area[(x, y)]] = (x, y)
    
    key_dict = djikstra(area, keys)

    part2 = 0
    for quadrant in range(4):
        # Assume that no quadrant has both a specific key and its door
        for k, v in key_dict[str(quadrant)].items():
            for kk in v[1]:
                assert(kk not in key_dict[str(quadrant)].keys())

        quadrant_distance = 1000000
        seen = {}
        nodes = deque()
        nodes.append((str(quadrant), str(quadrant), 0))
        while len(nodes) > 0:
            current_key, seen_keys, distance = nodes.popleft()
            
            if len(seen_keys) == len(key_dict[str(quadrant)]) + 1:
                quadrant_distance = min(quadrant_distance, distance)
            
            for k, (kdistance, _) in key_dict[current_key].items():
                if k in seen_keys:
                    continue

                nk = "".join(sorted(seen_keys + k))
                ndistance = distance + kdistance
                new_node = (k, nk, ndistance)
                if (k, nk) not in seen or seen[(k, nk)] > ndistance:
                    seen[(k, nk)] = ndistance
                    nodes.append(new_node)
        part2 += quadrant_distance

    return part2

def djikstra(area, keys):
    """
    key_dict = {
        'a': {
            'b': (10, [e]),
            'c': (35, [])
        },
        'b': {
            'a': (10, [e]),
            'c': (5, [f])
        }
    }
    """
    key_dict = {}
    for k, v in keys.items():
        key_dict[k] = {}

        open_set = []
        open_set.append(v)
        closed_set = set()
        distance = {}
        distance[v] = 0
        parents = {}
        while len(open_set) > 0:
            x, y = open_set.pop(0)
            closed_set.add((x, y))
            for xx, yy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                testPos = (x + xx, y + yy)
                cell = area[(x + xx, y + yy)]
                if testPos in closed_set or testPos in open_set:
                    continue
                if cell == "#":
                    continue

                open_set.append(testPos)
                parents[testPos] = (x, y)
                distance[testPos] = distance[(x, y)] + 1

                if cell.islower() or cell in "@0123":
                    blockers = set()
                    p = (x, y)
                    while p in parents:
                        if area[p].isupper():
                            blockers.add(area[p].lower())
                        p = parents[p]
                    
                    key_dict[k][cell] = (distance[testPos], blockers)
    return key_dict

aoc.run_lines(main, "day18.txt")