import aoc

class Node:
    def __init__(self, data):
       self.data = data
       self.next = None
       self.prev = None

class CircularLinkedList:
    def __init__(self):
        self.first = None
 
    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node
 
    def insert_at_end(self, new_node):
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.first.prev, new_node)
 
    def remove(self, node):
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next
 
def main(inputBlob):
    part1, _ = play(inputBlob, 0, 100)
    _, part2 = play(inputBlob, 1000000, 10000000)

    return part1, part2

def play(inputBlob, extraCups, iterations):
    nrOfCups = max(len(inputBlob), extraCups)
    cups = CircularLinkedList()
    cupDict = {}
    for a in inputBlob:
        node = Node(int(a))
        cups.insert_at_end(node)
        cupDict[int(a)] = node
    for a in range(max([int(b) for b in inputBlob]) + 1, extraCups + 1):
        node = Node(a)
        cups.insert_at_end(node)
        cupDict[a] = node
    currentCup = cupDict[int(inputBlob[0])]

    for _ in range(iterations):
        pickup = []
        c = currentCup.next
        for _ in range(3):
            pickup.append(c)
            c = c.next
        pickup[0].prev.next = pickup[2].next
        pickup[2].next.prev = pickup[0].prev
        
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
        destinationCup.next.prev = pickup[2]
        pickup[2].next = destinationCup.next
        destinationCup.next = pickup[0]
        pickup[0].prev = destinationCup

        currentCup = currentCup.next
    
    part1 = ""
    cup = cupDict[1].next
    while cup.data != 1:
        part1 += str(cup.data)
        cup = cup.next
    
    part2 = cupDict[1].next.data * cupDict[1].next.next.data 
    
    return part1, part2

aoc.runRaw(main, "day23.txt")