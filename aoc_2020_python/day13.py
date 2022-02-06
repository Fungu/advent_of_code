import aoc
import math

def main(input_lines):
    earliest_departure = int(input_lines[0])
    bus_list = [[i, int(bus)] for i, bus in enumerate(input_lines[1].split(",")) if bus != "x"]

    best_time = None
    for _, bus in bus_list:
        next_time = math.ceil(earliest_departure / bus) * bus
        if best_time == None or next_time < best_time:
            best_time = next_time
            best_bus = bus
    part1 = int(best_bus) * (best_time - earliest_departure)

    increment = bus_list[0][1]
    part2 = 0
    for i, bus in bus_list[1:]:
        while (part2 + i) % bus != 0:
            part2 += increment
        increment *= bus

    return part1, part2

aoc.run_lines(main, "day13.txt")