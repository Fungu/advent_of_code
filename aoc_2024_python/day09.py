import aoc

def main(data: str):
    flattened_disk_map = []
    disk_map = []
    free_spaces = []
    pos = 0
    id = 0
    is_file = True
    for c in data:
        for _ in range(int(c)):
            if is_file:
                flattened_disk_map.append(id)
            else:
                flattened_disk_map.append(None)
        if is_file:
            disk_map.append({"pos": pos, "size": int(c)})
            id += 1
        else:
            free_spaces.append({"pos": pos, "size": int(c)})
        pos += int(c)
        is_file = not is_file

    part1 = 0
    start_index = 0
    end_index = len(flattened_disk_map) - 1
    while True:
        while flattened_disk_map[end_index] == None:
            end_index -= 1
            if start_index >= end_index:
                break
        if start_index > end_index:
            break
        if flattened_disk_map[start_index] != None:
            part1 += start_index * flattened_disk_map[start_index]
        else:
            part1 += start_index * flattened_disk_map[end_index]
            end_index -= 1
        start_index += 1

    for i in range(len(disk_map) - 1, 0, -1):
        file = disk_map[i]
        for space in free_spaces:
            if space["pos"] > file["pos"]:
                break
            if space["size"] >= file["size"]:
                if i + 1 < len(space):
                    space[i]["size"] += file["size"]
                if i + 1 < len(space):
                    space[i]["size"] += space[i + 1]["size"]
                    space[i + 1]["size"] = 0
                file["pos"] = space["pos"]
                space["size"] -= file["size"]
                space["pos"] += file["size"]
                break
    
    part2 = 0
    for i, file in enumerate(disk_map):
        for a in range(file["size"]):
            part2 += (file["pos"] + a) * i
    return part1, part2

aoc.run_raw(main, "day09.txt")
