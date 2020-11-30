import datetime

def main():
    with open("input/day4.txt") as file:
        low, high = file.read().split("-")
    start = datetime.datetime.now()

    N = range(int(low), int(high) + 1)
    
    N = [n for n in N if len([i for i in range(5) if digit(n, i) > digit(n, i+1)]) == 0]
    a = [n for n in N if len([i for i in range(5) if digit(n, i) == digit(n, i+1)]) > 0]
    b = [n for n in a if len([i for i in range(5) if digit(n, i) == digit(n, i+1) and 
                                                    (i == 0 or digit(n, i-1) != digit(n, i)) and 
                                                    (i == 4 or digit(n, i+2) != digit(n, i))]) > 0]
    
    print(datetime.datetime.now() - start)
    print("part 1:", len(a), len(a) == 2220)
    print("part 2:", len(b), len(b) == 1515)

def digit(number, index):
    return int(number / (10 ** (5 - index))) % 10

main()