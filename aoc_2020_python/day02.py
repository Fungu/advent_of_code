import aoc
import scanf

def main(input_lines):
    part1 = 0
    part2 = 0

    for line in input_lines:
        low, high, letter, password = scanf.scanf("%d-%d %c: %s", line)
        if low <= password.count(letter) <= high:
            part1 += 1
        if (password[low - 1] == letter) ^ (password[high - 1] == letter):
            part2 += 1
    
    return part1, part2

aoc.run_lines(main, "day02.txt")