import aoc

def main(inputLines):
    doorPublicKey = int(inputLines[0])
    cardPublicKey = int(inputLines[1])

    doorLoopSize = findLoopSize(doorPublicKey)
    doorEncryptionKey = transform(doorLoopSize, cardPublicKey)

    return doorEncryptionKey, "Pay 49 stars"

def findLoopSize(publicKey):
    loopSize = 0
    subjectNumber = 7
    value = 1
    while True:
        loopSize += 1
        value *= subjectNumber
        value = value % 20201227
        if value == publicKey:
            return loopSize


def transform(loopSize, subjectNumber):
    value = 1
    for _ in range(loopSize):
        value *= subjectNumber
        value = value % 20201227
    return value

aoc.runLines(main, "day25.txt")