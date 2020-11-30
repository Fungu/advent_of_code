import intcode
import datetime

def main():
    with open("input/day13.txt") as file:
        memory = [int(val) for val in file.read().split(",")]
    memory += [0] * 1000

    output = []
    intcode.runProgram(memory.copy(), [], output)
    part1 = 0
    for i in range(2, len(output), 3):
        if output[i] == 2:
            part1 += 1
    print("part 1:", part1, part1 == 420)

    ip = 0
    relativeBase = 0
    programInput = []
    memory[0] = 2
    score = 0
    highestX = 0
    highestY = 0
    tiles = {}
    while True:
        ip, finished, relativeBase = intcode.runProgram(memory, programInput, output, ip, relativeBase)
        if finished:
            break
        ballPos = 0
        paddlePos = 0
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
                    paddlePos = output[i]
                #4 is a ball tile. The ball moves diagonally and bounces off objects.
                elif output[i + 2] == 4: 
                    char = "O"
                    ballPos = output[i]
                tiles[(output[i], output[i + 1])] = char
                highestX = max(highestX, output[i])
                highestY = max(highestY, output[i + 1])
        output.clear()
        """for y in range(highestY + 1):
            for x in range(highestX + 1):
                if (x, y) in tiles:
                    print(tiles[(x, y)], end='')
            print("")
        """
        if paddlePos > ballPos:
            programInput.append(-1)
        elif paddlePos < ballPos:
            programInput.append(1)
        else:
            programInput.append(0)
        """
        userInput = input("")
        if userInput == "a":
            programInput.append(-1)
            print("left")
        if userInput == "d":
            programInput.append(1)
            print("right")
        if userInput == " ":
            programInput.append(0)
            print("pass")
        """
    for i in range(0, len(output), 3):
        #X=-1, Y=0 -> third is score
        if output[i] == -1 and output[i + 1] == 0:
            score = output[i + 2]
    
    print("part 2:", score, score == 21651)

start = datetime.datetime.now()
main()
print(datetime.datetime.now() - start)