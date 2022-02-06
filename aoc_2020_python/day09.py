import aoc

def main(input_lines):
    xmas = [int(line) for line in input_lines]

    preamble_length = 25
    for i in range(preamble_length + 1, len(xmas)):
        is_valid = False
        for a in range(i - preamble_length - 1, i):
            for b in range(a + 1, i):
                if xmas[i] == xmas[a] + xmas[b]:
                    is_valid = True
        if not is_valid:
            part1 = xmas[i]
            break
    
    contiguous_length = 2
    current_sum = sum(xmas[0 : contiguous_length])
    for i in range(len(xmas)):
        while current_sum < part1:
            current_sum += xmas[i + contiguous_length]
            contiguous_length += 1
        while current_sum > part1 and contiguous_length > 2:
            current_sum -= xmas[i + contiguous_length - 1]
            contiguous_length -= 1
        if current_sum == part1:
            part2 = min(xmas[i : i + contiguous_length]) + max(xmas[i : i + contiguous_length])
            break
        else:
            current_sum -= xmas[i]
            contiguous_length -= 1

    return part1, part2

aoc.run_lines(main, "day09.txt")