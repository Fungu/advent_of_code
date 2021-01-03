import aoc

def test():
    size = 11
    value = 3

    deck = list(range(size))
    print(deck)



    print()
    print("deal")
    deck = list(range(size))
    deck = deal(deck, value)
    print(deck)

    offset, increment = dealFast(0, 1, size, value)
    printFast(offset, increment, size)


    print()
    print("new stack")
    deck = list(range(size))
    newStack(deck)
    print(deck)

    offset, increment = newStackFast(0, 1)
    printFast(offset, increment, size)


    print()
    print("cut")
    deck = list(range(size))
    deck = cut(deck, value)
    print(deck)

    offset, increment = cutFast(0, 1, value)
    printFast(offset, increment, size)




    deck = list(range(size))
    offset = 0
    increment = 1

    print()
    print("test")
    
    for _ in range(10):
        value = 7
        deck = deal(deck, value)
        offset, increment = dealFast(offset, increment, size, value)

        value = 4
        deck = cut(deck, value)
        offset, increment = cutFast(offset, increment, value)
        
        value = 2
        deck = newStack(deck)
        offset, increment = newStackFast(offset, increment)

        value = 3
        deck = newStack(deck)
        offset, increment = newStackFast(offset, increment)

        value = 6
        deck = deal(deck, value)
        offset, increment = dealFast(offset, increment, size, value)

        value = 5
        deck = cut(deck, value)
        offset, increment = cutFast(offset, increment, value)
        
        offset = offset % size
        increment = increment % size
        #printFast(offset, increment, size)
        print(offset, increment)

    """
    print()
    for value in range(1, size):
        deck = list(range(size))
        deck = deal(deck, value)
        print(value, deck)
    """



# what number is on the card that ends up in position 2020?

def main(inputLines):
    techniques = [line.strip() for line in inputLines]
    size = 10007
    
    offset = 0
    increment = 1
    deck = list(range(size))
    #print(deck[:10])
    #printFast(offset, increment, size, 10)

    for t in techniques:
        #print(t)
        if t.count("increment"):
            value = int(t.replace("deal with increment ", ""))
            deck = deal(deck, value)
            offset, increment = dealFast(offset, increment, size, value)
        if t.count("stack"):
            deck = newStack(deck)
            offset, increment = newStackFast(offset, increment)
        if t.count("cut"):
            value = int(t.replace("cut ", ""))
            deck = cut(deck, value)
            offset, increment = cutFast(offset, increment, value)
        #break
        #print(deck[:10])
        #printFast(offset, increment, size, 10)
        #input()
    for i, c in enumerate(deck):
        #if c == 2019:
        #    part1 = i
        if ((offset + i * increment) % size) == 2019:
            part1 = i
    print(increment, offset % size)
    #print(deck[:10])
    #printFast(offset, increment, size, 10)

    offset = 0
    increment = 1
    size = 119315717514047
    parsedTechniques = []
    for t in techniques:
        value = t.split()[-1]
        #print(t)
        if t.count("increment"):
            offset, increment = dealFast(offset, increment, size, int(value))
            parsedTechniques.append((0, int(value)))
        if t.count("stack"):
            offset, increment = newStackFast(offset, increment)
            parsedTechniques.append((1, None))
        if t.count("cut"):
            offset, increment = cutFast(offset, increment, int(value))
            parsedTechniques.append((2, int(value)))
        offset = offset % size
        increment = increment % size
    
    print(offset, increment)
    print(offset == 2220204964869, increment == 51399895659261)
    
    firstOffset = offset
    firstIncrement = increment
    #offset = 0
    #increment = 1
    iterations = 101741582076661
    """for i in range(iterations):
        if i % 100000 == 0:
            print(i)
        for t in parsedTechniques:
            #print(t)
            if t[0] == 0:
                offset, increment = dealFast(offset, increment, size, t[1])
            if t[0] == 1:
                offset, increment = newStackFast(offset, increment)
            if t[0] == 2:
                offset, increment = cutFast(offset, increment, t[1])
            offset = offset % size
            increment = increment % size
            if offset == firstOffset and increment == firstIncrement:
                print("match", i)
                break"""
    
    #offset = (offset * iterations) % size
    #increment = (increment * iterations) % size
    #offset, increment = shuffleManyTimes(offset, increment, size, iterations)
    
    increment, offset = run_many(increment, offset, size, iterations)
    part2 = (offset + 2020 * increment) % size
    # number is on the card that ends up in position 2020?
    
    # 35014662191179 - too low
    # 101759002476291 - too high
    # 101757421051592 - too high
    # 103352912640574 - nope
    # 34862349713698 - nope
    # 55574110161534 - correct?
    return part1, part2

def run_many(a,b,e,LEN):
  if e==1:
    return a,b
  elif e%2==0:
    return run_many((a*a)%LEN, (a*b+b)%LEN, e/2,LEN)
  else:
    c,d = run_many(a,b,e-1,LEN)
    return (a*c)%LEN,(a*d+b)%LEN

def shuffleManyTimes(offset, increment, size, iterations):
    if iterations == 1:
        return offset, increment
    elif iterations % 2 == 0:
        return shuffleManyTimes(
            (increment * offset + offset) % size, 
            (increment * increment) % size, 
            size, iterations / 2)
    else:
        offset2, increment2 = shuffleManyTimes(offset, increment, size, iterations - 1)
        return (increment * offset2 + offset) % size, (increment * increment2) % size

def printFast(offset, increment, size, numbersToPrint = None):
    print(" ", end = "")
    if numbersToPrint != None:
        r = range(numbersToPrint)
    else:
        r = range(size)
    for i in r:
        print((offset + i * increment) % size, " ", end = "")
    print()

def newStack(deck):
    deck.reverse()
    return deck

def newStackFast(offset, increment):
    offset -= increment
    increment = -increment
    return offset, increment

def cut(deck, n):
    newDeck = deck[n:] + deck[:n]
    return newDeck

def cutFast(offset, increment, n):
    offset += n * increment
    return offset, increment

def deal(deck, increment):
    newDeck = [0] * len(deck)
    for i in range(len(deck)):
        newDeck[(i * increment) % len(deck)] = deck[i]
    return newDeck

def dealFast(offset, increment, size, value):
    #increment *= int(size / value) + 1
    #increment *= (int(size % value) + 1)
    #increment = increment % size
    #for i in range(size):
    #    if (i * value) % size == 1:
    #        newIncrement = i
    #        break
    #print(newIncrement)
     
    for N in range(size):
        x = (N * size + 1) / value
        if x % 1 == 0:
            newIncrement = x
            break
    increment *= newIncrement
    increment = increment % size
    # x = (N * size + 1) / increment
    
    
    return offset, int(increment)


test()
#aoc.runLines(main, "day22.txt")
