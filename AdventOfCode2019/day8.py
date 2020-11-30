def main():
    with open("input/day8.txt") as file:
        data = [int(x) for x in file.read()]
    width = 25
    height = 6
    
    best = float("inf")
    i = 0
    while i < len(data):
        values = {}
        for _ in range(width * height):
            values[data[i]] = 1 + values.get(data[i], 0)
            i += 1
        if values[0] < best:
            best = values[0]
            part1 = values[1] * values[2]
    print("part 1", part1, part1 == 2480)
    
    part2 = ""
    for y in range(height):
        for x in range(width):
            for i in range(len(data) // (width * height)):
                pixel = data[x + y * width + i * width * height]
                if pixel == 0: # black
                    part2 += " "
                    break
                elif pixel == 1: # white
                    part2 += "#"
                    break
        part2 += "\n"
    print("part 2")
    print(part2)
    
main()