import aoc

def main(input_lines):
    adapters = [int(line) for line in input_lines]
    adapters.append(0)
    adapters = sorted(adapters)
    adapters.append(adapters[-1] + 3)

    differences = [0, 0, 0]
    for i in range(len(adapters) - 1):
        differences[adapters[i + 1] - adapters[i] - 1] += 1
    part1 = differences[0] * differences[2]
    
    part2 = get_combinations_from(0, adapters, {})

    return part1, part2

# Dynamic programming
def get_combinations_from(index, adapters, memory):
    if index + 1 == len(adapters):
        return 1
    if index in memory:
        return memory[index]
    ret = 0
    for i in range(index + 1, index + 4):
        if i < len(adapters) and adapters[i] - adapters[index] <= 3:
            ret += get_combinations_from(i, adapters, memory)
    memory[index] = ret
    return ret

aoc.run_lines(main, "day10.txt")