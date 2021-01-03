import aoc
from intcode import Intcode
from collections import defaultdict
import networkx as nx

"""
Movement via north, south, east, or west.

To take an item the droid sees in the environment, use the command take <name of item>. 
For example, if the droid reports seeing a red ball, you can pick it up with take red ball.

To drop an item the droid is carrying, use the command drop <name of item>. 
For example, if the droid is carrying a green ball, you can drop it with drop green ball.

To get a list of all of the items the droid is currently carrying, use the command inv (for "inventory").
"""

def manual_game(puzzle_input):
    computer = Intcode(puzzle_input)
    while not computer.finished:
        computer.run_program()
        computer.print_output()
        print(get_doors(computer.get_output_string()))
        print(get_items(computer.get_output_string()))

        computer.add_ascii_input(input())
        computer.output.clear()
    return None, None

def main(puzzle_input):
    blacklist = ["molten lava", "photons", "infinite loop", "giant electromagnet", "escape pod"]
    opposites = {"north" : "south",
                "south" : "north",
                "east" : "west",
                "west" : "east"}

    computer = Intcode(puzzle_input)
    computer.run_program()

    items = []
    doors = {}
    graph = nx.Graph()
    closed_set = set()
    open_set = [] # (room_name, door)
    room_name = get_room_name(computer.get_output_string())
    for door in get_doors(computer.get_output_string()):
        open_set.append((room_name, door))
    computer.output.clear()
    
    # Explore the maze
    while len(open_set):
        source_room, door_to_check = open_set.pop()
        closed_set.add((source_room, door_to_check))
        
        if source_room != room_name:
            path = nx.shortest_path(graph, source = room_name, target = source_room)
            path_edges = zip(path, path[1:])
            for edge in path_edges:
                computer.add_ascii_input(doors[edge])
            computer.run_program()
            computer.output.clear()
        
        computer.add_ascii_input(door_to_check)
        computer.run_program()

        new_room = get_room_name(computer.get_output_string())
        doors[(source_room, new_room)] = door_to_check
        doors[(new_room, source_room)] = opposites[door_to_check]
        closed_set.add((new_room, opposites[door_to_check]))
        graph.add_edge(source_room, new_room)
        if new_room != "Pressure-Sensitive Floor":
            for door in get_doors(computer.get_output_string()):
                if (new_room, door) not in closed_set and (new_room, door) not in open_set:
                    open_set.append((new_room, door))
        room_name = new_room

        for item in get_items(computer.get_output_string()):
            if not item in blacklist:
                computer.add_ascii_input("take " + item)
                #print("take ", item)
                items.append(item)
        computer.output.clear()
    
    # Get to Security Checkpoint
    if room_name != "Security Checkpoint":
        path = nx.shortest_path(graph, source = room_name, target = "Security Checkpoint")
        path_edges = zip(path, path[1:])
        for edge in path_edges:
            computer.add_ascii_input(doors[edge])
        computer.run_program()
        computer.output.clear()

    # Try all combinations
    inventory = items.copy()
    for permutation in gray_code(len(items)):
        computer.output.clear()
        for i, s in enumerate(permutation):
            if s == "1" and not items[i] in inventory:
                computer.add_ascii_input("take " + items[i])
                inventory.append(items[i])
            if s == "0" and items[i] in inventory:
                computer.add_ascii_input("drop " + items[i])
                inventory.remove(items[i])
        computer.add_ascii_input(doors[("Security Checkpoint", "Pressure-Sensitive Floor")])
        computer.run_program()

        if computer.get_output_string().find("Checkpoint") == -1:
            break

    part1 = computer.get_output_string().split("typing")[1].strip().split(" ")[0]

    return part1, "Align the Warp Drive"


def output_to_string(output):
    return "".join([chr(c) for c in output])

def get_room_name(output):
    return output.split("==")[1].strip() if "==" in output else ""

def get_doors(output):
    ret = []
    if "Doors here lead:" in output:
        output = output.split("Doors here lead:")[1]
        for direction in ["north", "south", "east", "west"]:
            if direction in output:
                ret.append(direction)
    return ret

def get_items(output):
    ret = []
    if "Items here:" in output:
        output = output.split("Items here:")[1].splitlines()[1:]
        for line in output:
            if "-" in line:
                ret.append(line.replace("-", "").strip())
            else:
                break
        return ret
    else:
        return []

def gray_code(n):
    def gray_code_recurse (g,n):
        k=len(g)
        if n<=0:
            return

        else:
            for i in range (k-1,-1,-1):
                char='1'+g[i]
                g.append(char)
            for i in range (k-1,-1,-1):
                g[i]='0'+g[i]

            gray_code_recurse (g,n-1)

    g=['0','1']
    gray_code_recurse(g,n-1)
    return g

aoc.run_raw(main, "day25.txt")
#aoc.run_raw(manual_game, "day25.txt")