import aoc

def main(puzzle_input):
    low, high = puzzle_input.split("-")
    numbers = range(int(low), int(high) + 1)
    
    N = [n for n in numbers if str(n) == ''.join(sorted(list(str(n))))]
    a = [n for n in N if any([(str(d) * 2 in str(n)) for d in range(0, 10)])]
    b = [n for n in N if any([(str(d) * 2 in str(n)) and not (str(d) * 3 in str(n)) for d in range(0, 10)])]

    return len(a), len(b)

aoc.run_raw(main, "day04.txt")