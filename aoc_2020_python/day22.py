import aoc

def main(inputBlob):
    inputDecks = []
    inputDecks.append([int(a) for a in inputBlob.split("\n\n")[0].splitlines() if a.isnumeric()])
    inputDecks.append([int(a) for a in inputBlob.split("\n\n")[1].splitlines() if a.isnumeric()])

    _, part1 = play(inputDecks.copy(), False)
    _, part2 = play(inputDecks, True)

    return part1, part2

def calculateScore(decks):
    ret = 0
    mult = len(decks[0]) + len(decks[1])
    for deck in decks:
        for i in range(len(deck)):
            ret += deck[i] * mult
            mult -= 1
    return ret

def play(decks, part2 = False):
    previousRounds = set()
    while decks[0] and decks[1]:
        # Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. 
        # Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
        deckConfiguration = (tuple(decks[0]), tuple(decks[1]))
        if deckConfiguration in previousRounds:
            return 0, decks
        previousRounds.add(deckConfiguration)
    
        # Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
        draw = []
        for player in [0, 1]:
            draw.append(decks[player][0])
            decks[player] = decks[player][1:]

        # If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
        if draw[0] <= len(decks[0]) and draw[1] <= len(decks[1]) and part2:
            newDecks = []
            newDecks.append(decks[0][:draw[0]])
            newDecks.append(decks[1][:draw[1]])
            if max(max(newDecks[0]), max(newDecks[1])) in newDecks[0]:
                subWinner = 0
            else:
                subWinner, _ = play(newDecks, part2)
        
        # Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.
        else:
            subWinner = 0 if draw[0] > draw[1] else 1
        
        decks[subWinner].append(draw[subWinner])
        decks[subWinner].append(draw[(subWinner+1)%2])
    
    winner = 0 if len(decks[0]) > 0 else 1
    return winner, calculateScore(decks)

aoc.runRaw(main, "day22.txt")