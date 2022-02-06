import aoc

def main(raw_input):
    input_decks = []
    input_decks.append([int(a) for a in raw_input.split("\n\n")[0].splitlines() if a.isnumeric()])
    input_decks.append([int(a) for a in raw_input.split("\n\n")[1].splitlines() if a.isnumeric()])

    _, part1 = play(input_decks.copy(), False)
    _, part2 = play(input_decks, True)

    return part1, part2

def calculate_score(decks):
    ret = 0
    mult = len(decks[0]) + len(decks[1])
    for deck in decks:
        for i in range(len(deck)):
            ret += deck[i] * mult
            mult -= 1
    return ret

def play(decks, part2 = False):
    previous_rounds = set()
    while decks[0] and decks[1]:
        # Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. 
        # Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
        deck_configuration = (tuple(decks[0]), tuple(decks[1]))
        if deck_configuration in previous_rounds:
            return 0, decks
        previous_rounds.add(deck_configuration)
    
        # Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
        draw = []
        for player in [0, 1]:
            draw.append(decks[player][0])
            decks[player] = decks[player][1:]

        # If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
        if draw[0] <= len(decks[0]) and draw[1] <= len(decks[1]) and part2:
            new_decks = []
            new_decks.append(decks[0][:draw[0]])
            new_decks.append(decks[1][:draw[1]])
            if max(max(new_decks[0]), max(new_decks[1])) in new_decks[0]:
                sub_winner = 0
            else:
                sub_winner, _ = play(new_decks, part2)
        
        # Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.
        else:
            sub_winner = 0 if draw[0] > draw[1] else 1
        
        decks[sub_winner].append(draw[sub_winner])
        decks[sub_winner].append(draw[(sub_winner+1)%2])
    
    winner = 0 if len(decks[0]) > 0 else 1
    return winner, calculate_score(decks)

aoc.run_raw(main, "day22.txt")