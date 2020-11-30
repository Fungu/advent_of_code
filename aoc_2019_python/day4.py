import datetime

def main():
    with open("input/day4.txt") as file:
        f = file.read().split("-")
    start = datetime.datetime.now()

    numbers = [int(val) for val in f[0]]
    for i in range(1, 6):
        if numbers[i - 1] > numbers[1]:
            for j in range(i, 6):
                numbers[j] = numbers[j - 1]
    
    maxLimit = int(f[1])
    nrOfHits1 = 0
    nrOfHits2 = 0
    password = list_to_number(numbers)
    while password <= maxLimit:
        if has_same(password, False):
            nrOfHits1 += 1
        if has_same(password, True):
            nrOfHits2 += 1
        
        index = 5
        numbers[index] += 1
        while numbers[index] == 10:
            numbers[index] = 0
            numbers[index - 1] += 1
            index -= 1
        for i in range(index, 6):
            numbers[i] = max(numbers[i], numbers[i - 1])
        password = list_to_number(numbers)
    
    print(datetime.datetime.now() - start)
    print("part 1: ", nrOfHits1)
    print("part 2: ", nrOfHits2)

def list_to_number(numbers):
    return numbers[0] * 100000 + numbers[1] * 10000 + numbers[2] * 1000 + numbers[3] * 100 + numbers[4] * 10 + numbers[5]

def has_same(password, part2 = False):
    passwordString = str(password)
    for i in range(5):
        if passwordString[i] == passwordString[i + 1]:
            if part2 == False:
                return True
            elif (i == 0 or passwordString[i] != passwordString[i - 1]) and (i == 4 or passwordString[i] != passwordString[i + 2]):
                return True
    return False

main()

"""
start = datetime.datetime.now()
lo , hi = 123257 , 647015
strings = [str(s) for s in range(lo, hi + 1)]
nodecrs = [s for s in strings if s == ''.join(sorted(list(s)))]
repeats = [str(i) * 2 for i in range(10)]
results = [s for s in nodecrs if any(d in s for d in repeats)]
print(len(results))
print(datetime.datetime.now() - start)
"""