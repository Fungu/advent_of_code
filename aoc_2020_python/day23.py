import aoc

class Node:
    def __init__(self, data):
       self.data = data
       self.next = None
 
def main(input_blob):
    part1, _ = play(input_blob, 0, 100)
    _, part2 = play(input_blob, 1000000, 10000000)

    return part1, part2

def play(input_blob, extra_cups, iterations):
    nr_of_cups = max(len(input_blob), extra_cups)
    first_node = None
    last_node = None
    cup_dict = {}
    for a in input_blob:
        node = Node(int(a))
        if first_node == None:
            first_node = node
        if last_node != None:
            last_node.next = node
        cup_dict[int(a)] = node
        last_node = node
    for a in range(max([int(b) for b in input_blob]) + 1, extra_cups + 1):
        node = Node(a)
        cup_dict[a] = node
        last_node.next = node
        last_node = node
    current_cup = first_node
    last_node.next = first_node

    for _ in range(iterations):
        pickup = []
        c = current_cup.next
        for _ in range(3):
            pickup.append(c)
            c = c.next
        current_cup.next = pickup[-1].next
        
        destination = current_cup.data - 1
        if destination < 1:
            destination += nr_of_cups
        while True:
            is_destination_in_pickup = False
            for cup in pickup:
                if cup.data == destination:
                    is_destination_in_pickup = True
            if is_destination_in_pickup:
                destination -= 1
                if destination < 1:
                    destination += nr_of_cups
            else:
                break
        
        destination_cup = cup_dict[destination]
        pickup[2].next = destination_cup.next
        destination_cup.next = pickup[0]

        current_cup = current_cup.next
    
    part1 = ""
    cup = cup_dict[1].next
    while cup.data != 1:
        part1 += str(cup.data)
        cup = cup.next
    
    part2 = cup_dict[1].next.data * cup_dict[1].next.next.data 
    
    return part1, part2

aoc.run_raw(main, "day23.txt")