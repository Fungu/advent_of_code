import aoc
import re

def main(lines: list):
    part1 = 0
    part2 = 0

    pattern = r".*X(?:\+|=)(\d+), Y(?:\+|=)(\d+)"
    for i in range(0, len(lines), 4):
        button_a = [int(x) for x in re.match(pattern, lines[i]).groups()]
        button_b = [int(x) for x in re.match(pattern, lines[i+1]).groups()]
        prize = [int(x) for x in re.match(pattern, lines[i+2]).groups()]

        part1 += required_tokens(button_a, button_b, prize)
        part2 += required_tokens(button_a, button_b, (prize[0] + 10000000000000, prize[1] + 10000000000000))
    
    return part1, part2

def required_tokens(button_a, button_b, prize):
    b = (prize[1] * button_a[0] - prize[0] * button_a[1]) / (button_b[1] * button_a[0] - button_b[0] * button_a[1])
    if b == int(b):
        a = (prize[0] - int(b) * button_b[0]) / button_a[0]
        if a == int(a):
            return 3 * int(a) + int(b)
    return 0

aoc.run_lines(main, "day13.txt")
