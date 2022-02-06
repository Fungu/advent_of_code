import aoc

def main(input_lines):
    door_public_key = int(input_lines[0])
    card_public_key = int(input_lines[1])

    door_key_candidate = 1
    encryption_key = 1
    while door_key_candidate != door_public_key:
        encryption_key *= card_public_key
        encryption_key = encryption_key % 20201227
        door_key_candidate *= 7
        door_key_candidate = door_key_candidate % 20201227

    return encryption_key, "Pay 49 stars"

aoc.run_lines(main, "day25.txt")