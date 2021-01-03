import aoc
from intcode import Intcode

def main(puzzle_input):
    computer = Intcode(puzzle_input)
    computer.run_program()
    part1 = sum([1 for i in range(2, len(computer.output), 3) if computer.output[i] == 2])

    computer = Intcode(puzzle_input)
    computer.memory[0] = 2
    score = 0
    while not computer.finished:
        computer.output.clear()
        computer.run_program()
        output = computer.output
        for i in range(0, len(output), 3):
            #X=-1, Y=0 -> third is score
            if output[i] == -1 and output[i + 1] == 0:
                score = output[i + 2]
            else:
                #3 is a horizontal paddle tile. The paddle is indestructible.
                if output[i + 2] == 3: 
                    paddle_pos = output[i]
                #4 is a ball tile. The ball moves diagonally and bounces off objects.
                elif output[i + 2] == 4: 
                    ball_pos = output[i]
        if paddle_pos > ball_pos:
            computer.input.append(-1)
        elif paddle_pos < ball_pos:
            computer.input.append(1)
        else:
            computer.input.append(0)
    
    return part1, score

def manual_game(puzzle_input):
    computer = Intcode(puzzle_input)
    computer.memory[0] = 2
    score = 0
    tiles = {}
    while not computer.finished:
        computer.output.clear()
        computer.run_program()
        output = computer.output
        for i in range(0, len(output), 3):
            #X=-1, Y=0 -> third is score
            if output[i] == -1 and output[i + 1] == 0:
                score = output[i + 2]
            else:
                #0 is an empty tile. No game object appears in this tile.
                if output[i + 2] == 0: 
                    char = " "
                #1 is a wall tile. Walls are indestructible barriers.
                elif output[i + 2] == 1: 
                    char = "#"
                #2 is a block tile. Blocks can be broken by the ball.
                elif output[i + 2] == 2: 
                    char = "*"
                #3 is a horizontal paddle tile. The paddle is indestructible.
                elif output[i + 2] == 3: 
                    char = "-"
                #4 is a ball tile. The ball moves diagonally and bounces off objects.
                elif output[i + 2] == 4: 
                    char = "O"
                tiles[(output[i], output[i + 1])] = char
        
        print("Score:", score)
        for y in range(max([x for x, _ in tiles.keys()]) + 1):
            for x in range(max([y for _, y in tiles.keys()]) + 1):
                if (x, y) in tiles:
                    print(tiles[(x, y)], end='')
            print("")
        
        user_input = input()
        if user_input == "a":
            computer.input.append(-1)
        if user_input == "d":
            computer.input.append(1)
        if user_input == " ":
            computer.input.append(0)
    return None, None

#aoc.run_raw(manual_game, "day13.txt")
aoc.run_raw(main, "day13.txt")