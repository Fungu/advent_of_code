import time

def test():
    size = 11
    value = 4

    deck = list(range(size))
    print(deck)



    print()
    print("deal")
    deck = list(range(size))
    deck = deal(deck, value)
    print(deck)

    offset = 0
    increment = 1
    increment += int(size / value)
    for i in range(size):
        print((offset + i * increment) % size, " ", end = "")
    print()



    print()
    print("new stack")
    deck = list(range(size))
    newStack(deck)
    print(deck)

    offset = 0
    increment = 1
    increment = -increment
    offset -= 1
    for i in range(size):
        print((offset + i * increment) % size, " ", end = "")
    print()



    print()
    print("cut")
    deck = list(range(size))
    deck = cut(deck, 3)
    print(deck)

    offset = 0
    increment = 1
    offset += value + 1
    for i in range(size):
        print((offset + i * increment) % size, " ", end = "")
    print()



    deck = list(range(size))
    offset = 0
    increment = 1

    print()
    print("test")
    value = 2
    deck = deal(deck, value)
    increment += int(size / value)

    value = 3
    deck = deal(deck, value)
    increment += int(size / value)

    print(deck)
    for i in range(size):
        print((offset + i * increment) % size, " ", end = "")
    print()
    print()


# what number is on the card that ends up in position 2020?

def main():
    with open("input/day22.txt") as file:
        techniques = [line.strip() for line in file.readlines()]
    
    deck = list(range(10007))
    for t in techniques:
        if t.count("increment"):
            deck = deal(deck, int(t.replace("deal with increment ", "")))
        if t.count("stack"):
            newStack(deck)
        if t.count("cut"):
            deck = cut(deck, int(t.replace("cut ", "")))
    #print(deck)
    for i, c in enumerate(deck):
        if c == 2019:
            print("part 1:", i, i == 3939)
    

    # size9315717514047 space cards
    # 101741582076661 times in a row

    deck = list(range(10007))
    offset = 0
    increment = 1
    for t in techniques:
        # deal
        if t.count("increment"):
            value = int(t.replace("deal with increment ", ""))
            increment *= int(1 + len(deck) / value)
        # new stack
        if t.count("stack"):
            increment = -increment
            offset -= 1
        # cut
        if t.count("cut"):
            value = int(t.replace("cut ", ""))
            offset += value
    
    """for i in range(101741582076661):
        if i % 10000000 == 0:
            print(i)
        pass"""
    print((offset + 2019 * increment) % len(deck))
    print((offset + 3939 * increment) % len(deck))


def newStack(deck):
    deck.reverse()

def cut(deck, n):
    newDeck = deck[n:] + deck[:n]
    return newDeck

def deal(deck, increment):
    newDeck = [0] * len(deck)
    for i in range(len(deck)):
        newDeck[(i * increment) % len(deck)] = deck[i]
    return newDeck

start = time.time()
test()
main()
print(time.time() - start)