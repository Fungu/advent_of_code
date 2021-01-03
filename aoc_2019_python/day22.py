import aoc

def main(input_lines):
    # Part 1
    # What is the position of card 2019?
    size = 10007
    a, b = parse_techniques(input_lines, size)
    part1 = apply_shuffle(a, b, 2019, size)

    # Part 2
    # What number is on the card that ends up in position 2020?
    size = 119315717514047
    iterations = 101741582076661
    a, b = parse_techniques(input_lines, size)
    a, b = modular_exponentiation(a, b, iterations, size)
    part2 = apply_shuffle_inverted(a, b, 2020, size)

    return part1, part2

def parse_techniques(techniques, size):
    a = 1
    b = 0
    for t in techniques:
        value = t.split()[-1]
        if t.count("increment"):
            c = int(value)
            d = 0
        if t.count("stack"):
            c = -1
            d = -1
        if t.count("cut"):
            c = 1
            d = -int(value)
        a, b = combine_functions(a, b, c, d, size)
    return a, b

# f(x) = ax + b
# Returns the position of card x after applying the shuffle
def apply_shuffle(a, b, x, size):
    return (a * x + b) % size

# Returns which card will be on position x after applying the shuffle
def apply_shuffle_inverted(a, b, x, size):
    return ((x - b) * modular_inverse(a, size)) % size

# g(f(x)) = cf(x) + d = cax + cb + d
def combine_functions(a, b, c, d, size):
    return (c * a) % size, (c * b + d) % size

def modular_inverse(x, size):
    ret, _ = modular_exponentiation(x, 0, size - 2, size)
    return ret

def modular_exponentiation(a, b, iterations, size):
    if iterations == 1:
        return a, b
    elif iterations % 2 == 0:
        a, b = combine_functions(a, b, a, b, size)
        return modular_exponentiation(a, b, iterations / 2, size)
    else:
        c, d = modular_exponentiation(a, b, iterations - 1, size)
        return combine_functions(a, b, c, d, size)

aoc.run_lines(main, "day22.txt")