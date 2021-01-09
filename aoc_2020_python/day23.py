import aoc

class Node:
    def __init__(self, data):
       self.data = data
       self.next = None
 
def main(inputBlob):
    part1, _ = play(inputBlob, 0, 100)
    _, part2 = play(inputBlob, 1000000, 10000000)

    return part1, part2

def play(inputBlob, extraCups, iterations):
    nrOfCups = max(len(inputBlob), extraCups)
    firstNode = None
    lastNode = None
    cupDict = {}
    for a in inputBlob:
        node = Node(int(a))
        if firstNode == None:
            firstNode = node
        if lastNode != None:
            lastNode.next = node
        cupDict[int(a)] = node
        lastNode = node
    for a in range(max([int(b) for b in inputBlob]) + 1, extraCups + 1):
        node = Node(a)
        cupDict[a] = node
        lastNode.next = node
        lastNode = node
    currentCup = firstNode
    lastNode.next = firstNode

    for _ in range(iterations):
        pickup = []
        c = currentCup.next
        for _ in range(3):
            pickup.append(c)
            c = c.next
        currentCup.next = pickup[-1].next
        
        destination = currentCup.data - 1
        if destination < 1:
            destination += nrOfCups
        while True:
            isDestinationInPickup = False
            for cup in pickup:
                if cup.data == destination:
                    isDestinationInPickup = True
            if isDestinationInPickup:
                destination -= 1
                if destination < 1:
                    destination += nrOfCups
            else:
                break
        
        destinationCup = cupDict[destination]
        pickup[2].next = destinationCup.next
        destinationCup.next = pickup[0]

        currentCup = currentCup.next
    
    part1 = ""
    cup = cupDict[1].next
    while cup.data != 1:
        part1 += str(cup.data)
        cup = cup.next
    
    part2 = cupDict[1].next.data * cupDict[1].next.next.data 
    
    return part1, part2

aoc.runRaw(main, "day23.txt")