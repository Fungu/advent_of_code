import aoc

def main(inputLines):
    doorPublicKey = int(inputLines[0])
    cardPublicKey = int(inputLines[1])

    doorKeyCandidate = 1
    encryptionKey = 1
    while doorKeyCandidate != doorPublicKey:
        encryptionKey *= cardPublicKey
        encryptionKey = encryptionKey % 20201227
        doorKeyCandidate *= 7
        doorKeyCandidate = doorKeyCandidate % 20201227

    return encryptionKey, "Pay 49 stars"

aoc.runLines(main, "day25.txt")