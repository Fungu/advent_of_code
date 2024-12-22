import aoc

def main(lines: list):
    part1 = 0
    part2 = 0

    sequences = set()
    banananana = []
    for line in lines:
        buy_options = {}
        prices = []
        secret = int(line)
        prices.append(secret % 10)
        for _ in range(2000):
            secret = prune(mix(secret, secret * 64))
            secret = prune(mix(secret, int(secret / 32)))
            secret = prune(mix(secret, secret * 2048))
            prices.append(secret % 10)
            if len(prices) >= 5:
                sequence = ""
                for i in range(-4, 0):
                    sequence += str(prices[i] - prices[i - 1])
                if sequence not in buy_options:
                    buy_options[sequence] = secret % 10
                sequences.add(sequence)
        part1 += secret
        banananana.append(buy_options)
    
    for sequence in sequences:
        banan = 0
        for buy_options in banananana:
            if sequence in buy_options:
                banan += buy_options[sequence]
        if banan > part2:
            part2 = banan
    
    return part1, part2

def mix(secret, value):
    return secret ^ value

def prune(secret):
    return secret % 16777216

aoc.run_lines(main, "day22.txt")
