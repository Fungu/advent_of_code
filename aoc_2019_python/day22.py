import aoc

def main(inputLines):
    # Part 1
    # What is the position of card 2019?
    size = 10007
    a, b = parseTechniques(inputLines, size)
    part1 = applyShuffle(a, b, 2019, size)

    # Part 2
    # What number is on the card that ends up in position 2020?
    size = 119315717514047
    iterations = 101741582076661
    a, b = parseTechniques(inputLines, size)
    a, b = exponentiationBySquaring(a, b, iterations, size)
    part2 = applyShuffleInverted(a, b, 2020, size)

    return part1, part2

def parseTechniques(techniques, size):
    a = 1
    b = 0
    for t in techniques:
        value = t.split()[-1]
        if t.count("increment"):
            A = int(value)
            B = 0
        if t.count("stack"):
            A = -1
            B = -1
        if t.count("cut"):
            A = 1
            B = -int(value)
        a, b = combineFunctions(a, b, A, B, size)
    return a, b

# f(x) = ax + b
# Returns the position of card x after applying the shuffle
def applyShuffle(a, b, x, size):
    return (a * x + b) % size

# Returns which card will be on position x after applying the shuffle
def applyShuffleInverted(a, b, x, size):
    return ((x - b) * modularInverse(a, size)) % size

# g(f(x)) = Af(x) + B = Aax + Ab + B
def combineFunctions(a, b, A, B, size):
    return (A * a) % size, (A * b + B) % size

def modularInverse(x, size):
    return modularExponentiation(x, size - 2, size)

def modularExponentiation(x, iterations, size):
    if iterations == 0:
        return 1
    elif iterations % 2 == 0:
        return modularExponentiation((x * x) % size, iterations / 2, size)
    else:
        return (x * modularExponentiation(x, iterations - 1, size)) % size

def exponentiationBySquaring(a, b, iterations, size):
    if iterations == 1:
        return a, b
    elif iterations % 2 == 0:
        a, b = combineFunctions(a, b, a, b, size)
        return exponentiationBySquaring(a, b, iterations / 2, size)
    else:
        A, B = exponentiationBySquaring(a, b, iterations - 1, size)
        return combineFunctions(a, b, A, B, size)

aoc.runLines(main, "day22.txt")