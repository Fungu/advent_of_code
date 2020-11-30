def main():
    with open("input/day6.txt") as file:
        lines = file.readlines()
    
    orbitMap = {}
    for line in lines:
        elements = line.split(")")
        orbitMap[elements[1].strip()] = elements[0].strip()

    part1 = 0
    for planet in orbitMap.keys():
        while planet in orbitMap:
            planet = orbitMap.get(planet)
            part1 += 1
    
    myOrbits = []
    planet = "YOU"
    while planet in orbitMap:
        planet = orbitMap.get(planet)
        myOrbits.append(planet)
    
    part2 = 0
    planet = "SAN"
    while planet in orbitMap:
        planet = orbitMap.get(planet)
        if planet in myOrbits:
            part2 += myOrbits.index(planet)
            break
        part2 += 1

    print("part 1: ", part1, part1 == 119831)
    print("part 2: ", part2, part2 == 322)

main()