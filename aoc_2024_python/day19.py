import aoc

def main(lines: list):
    part1 = 0
    part2 = 0

    towels = lines[0].split(", ")
    patterns = lines[2:]
    dp = {}
    for pattern in patterns:
        possible_ways = isPossible(towels, pattern, dp)
        if possible_ways:
            part1 += 1
        part2 += possible_ways

    return part1, part2

def isPossible(towels, pattern: str, dp: dict):
    if (pattern in dp):
        return dp[pattern]
    if pattern == "":
        return 1
    possible_ways = 0
    for towel in towels:
        if pattern.startswith(towel):
            possible_ways += isPossible(towels, pattern[len(towel):], dp)
    dp[pattern] = possible_ways
    return possible_ways

aoc.run_lines(main, "day19.txt")
