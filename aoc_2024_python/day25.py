import aoc
import re

def main(lines: list):
    lines.append("")
    height = lines.index("")
    width = len(lines[0])
    locks = []
    keys = []
    is_lock = None
    thingy = [0] * width
    for line in lines:
        if is_lock == None:
            is_lock = (line[0] == "#")
        if line == "":
            if is_lock:
                locks.append(thingy)
            else:
                keys.append(thingy)
            thingy = [0] * width
            is_lock = None
        else:
            for i in range(width):
                if line[i] == "#":
                    thingy[i] += 1

    part1 = 0
    for lock in locks:
        for key in keys:
            found_overlap = False
            for i in range(width):
                if lock[i] + key[i] > height:
                    found_overlap = True
                    break
            if not found_overlap:
                part1 += 1

    return part1, "God jul!"

aoc.run_lines(main, "day25.txt")
