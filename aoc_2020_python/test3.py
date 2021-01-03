from itertools import count

def p1(smart, **_):
    start = smart[0]
    buses = tuple(int(b) for b in smart[1].split(",") if b != "x")
    return next(
        (n - start) * next(b for b in buses if n % b == 0)
        for n in count(start)
        if any(n % b == 0 for b in buses)
    )

def p2(smart, **_):
    n = smart[0]
    buses = tuple((i, b) for i, b in enumerate(smart[1]) if isinstance(b, int))
    step = 1
    for i, b in buses:
        n = next(c for c in count(n, step) if (c + i) % b == 0)
        step *= b
    return n

with open("input/day13.txt") as file:
    rawInput = file.readlines()
print(p1(rawInput))