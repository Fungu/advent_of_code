import aoc

def main(input_lines):
    orbit_map = {}
    for line in input_lines:
        elements = line.split(")")
        orbit_map[elements[1].strip()] = elements[0].strip()

    part1 = 0
    for planet in orbit_map.keys():
        while planet in orbit_map:
            planet = orbit_map.get(planet)
            part1 += 1
    
    my_orbits = []
    planet = "YOU"
    while planet in orbit_map:
        planet = orbit_map.get(planet)
        my_orbits.append(planet)
    
    part2 = 0
    planet = "SAN"
    while planet in orbit_map:
        planet = orbit_map.get(planet)
        if planet in my_orbits:
            part2 += my_orbits.index(planet)
            break
        part2 += 1

    return part1, part2

aoc.run_lines(main, "day06.txt")