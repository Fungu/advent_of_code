import aoc

def main(lines: list):
    connections = {}
    for line in lines:
        left, right = line.strip().split("-")
        if left not in connections:
            connections[left] = []
        if right not in connections:
            connections[right] = []
        connections[left].append(right)
        connections[right].append(left)

    triangles_starting_with_t = set()
    for k, v in connections.items():
        if k[0] == "t":
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    if v[j] in connections[v[i]]:
                        triangles_starting_with_t.add(",".join(sorted([k, v[i], v[j]])))
    part1 = len(triangles_starting_with_t)

    best_group = []
    for k, v in connections.items():
        for combination in range(pow(2, len(v))):
            b = bin(combination)[2:].rjust(len(v), "0")
            if b.count("1") < len(best_group):
                continue
            group = [k] + [x for i, x in enumerate(v) if b[i] == "1"]
            
            found_unconnected = False
            for i in range(len(group)):
                if found_unconnected:
                    break
                for j in range(i + 1, len(group)):
                    if group[j] not in connections[group[i]]:
                        found_unconnected = True
                        break
            if not found_unconnected:
                best_group = group
    
    part2 = ",".join(sorted(best_group))
    
    return part1, part2

aoc.run_lines(main, "day23.txt")
