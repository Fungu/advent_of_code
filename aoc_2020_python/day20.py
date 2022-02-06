import aoc
import re
import colorama

def main(input_blob):
    tile_dict = {}
    for raw_tile in input_blob.split("\n\n"):
        lines = raw_tile.splitlines()
        tile_dict[lines[0].split()[1].replace(":", "")] = lines[1:]

    assembled_grid, tile_positions = assemble(tile_dict)
    
    min_x = min([x for x, y in tile_positions.keys()])
    max_x = max([x for x, y in tile_positions.keys()])
    min_y = min([y for x, y in tile_positions.keys()])
    max_y = max([y for x, y in tile_positions.keys()])
    part1 = int(tile_positions[(min_x, min_y)]) * int(tile_positions[(max_x, min_y)]) * int(tile_positions[(min_x, max_y)]) * int(tile_positions[(max_x, max_y)])

    for _ in range(4):
        for flipping in [False, True]:
            found, roughness = find_sea_monsters(assembled_grid)
            if found:
                part2 = roughness
                break
            if flipping:
                assembled_grid = flip(assembled_grid, True)
            else:
                assembled_grid = rotate(assembled_grid, 1)
    
    #print_grid(assembled_grid)

    return part1, part2

def get_edges(tile):
    """0->up, 1->left, 2->down, 3->right"""

    edges = []
    edges.append(tile[0])
    edges.append("".join([tile[i][0] for i in range(0, len(tile))])[::-1])
    edges.append(tile[-1][::-1])
    edges.append("".join([tile[i][-1] for i in range(0, len(tile))]))

    return edges

def rotate(tile, rotation):
    """rotation: 0->default, 1->90deg ccw, 2->180deg ccw, 3->270deg ccw"""

    for _ in range(rotation):
        new_tile = []
        for column in range(len(tile[0])):
            new_tile.append("".join([tile[i][len(tile[0]) - column - 1] for i in range(len(tile))]))
        tile = new_tile
    return tile

def flip(tile, horizontal):
    if horizontal:
        new_tile = []
        for line in tile:
            new_tile.append(line[::-1])
    else:
        new_tile = tile[::-1]
    return new_tile

def assemble(tile_dict):
    start_tile_id = list(tile_dict.keys())[0]
    direction_dict = {0: (0, -1), 1: (-1, 0), 2: (0, 1), 3: (1, 0)}

    # key=position, value=tile_id
    tile_positions = {}
    tile_positions[(0, 0)] = start_tile_id
    open_set = set()
    open_set.add((0, 0))
    while open_set:
        current_position = open_set.pop()
        current_tile_id = tile_positions[current_position]
        current_edges = get_edges(tile_dict[current_tile_id])
        for other_id, other_tile in tile_dict.items():
            if other_id in tile_positions.values():
                continue
            other_edges = get_edges(other_tile)
            for direction, edge_a in enumerate(current_edges):
                for other_direction, edge_b in enumerate(other_edges):
                    match = False
                    needs_flip = False
                    if edge_a == edge_b:
                        match = True
                        needs_flip = True
                    if edge_a == edge_b[::-1]:
                        match = True
                    if match:
                        d_x, d_y = direction_dict[direction]
                        position = (current_position[0] + d_x, current_position[1] + d_y)
                        if position not in tile_positions:
                            relative_rotation = direction - other_direction + 2
                            if relative_rotation < 0:
                                relative_rotation += 4
                            other_tile = rotate(other_tile, relative_rotation)
                            if needs_flip:
                                other_tile = flip(other_tile, direction in [0, 2])
                            tile_dict[other_id] = other_tile
                            tile_positions[position] = other_id
                            open_set.add(position)
    
    min_x = min([x for x, y in tile_positions.keys()])
    max_x = max([x for x, y in tile_positions.keys()])
    min_y = min([y for x, y in tile_positions.keys()])
    max_y = max([y for x, y in tile_positions.keys()])

    assembled_grid = []
    for y in range(min_y, max_y + 1):
        for inner_y in range(1, len(tile_dict[start_tile_id]) - 1):
            line = ""
            for x in range(min_x, max_x + 1):
                other_tile = tile_dict[tile_positions[(x, y)]]
                line += other_tile[inner_y][1:-1]
            assembled_grid.append(line)
    assembled_grid = flip(assembled_grid, False)
    return assembled_grid, tile_positions

def find_sea_monsters(grid):
    sea_monster = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   "
    ]
    
    sea_monster_match = []
    sea_monster_match.append(re.compile("(?=(" + sea_monster[0].replace(" ", ".") + "))"))
    sea_monster_match.append(re.compile("(?=(" + sea_monster[1].replace(" ", ".") + "))"))
    sea_monster_match.append(re.compile("(?=(" + sea_monster[2].replace(" ", ".") + "))"))

    sea_monster_count = 0
    for row in range(len(grid) - len(sea_monster_match) + 1):
        matches = []
        for pattern_index in range(len(sea_monster_match)):
            inner_matches = []
            for m in sea_monster_match[pattern_index].findall(grid[row + pattern_index]):
                inner_matches.append(grid[row + pattern_index].index(m))
            matches.append(inner_matches)
        for match_index in matches[1]:
            if match_index in matches[0] and match_index in matches[2]:
                sea_monster_count += 1
                for monster_index, monster_row in enumerate(sea_monster):
                    for monster_char_index, monster_char in enumerate(monster_row):
                        if monster_char == "#":
                            grid[row + monster_index] = grid[row + monster_index][: match_index + monster_char_index] + "O" + grid[row + monster_index][match_index + monster_char_index + 1 :]
    roughness = sum([row.count("#") for row in grid])

    return sea_monster_count != 0, roughness

def print_grid(grid):
    colorama.init()
    for row in grid:
        for char in row:
            if char == "#":
                print(colorama.Fore.BLUE, end='')
            elif char == ".":
                print(colorama.Fore.CYAN, end='')
            elif char == "O":
                print(colorama.Fore.YELLOW, end='')
            else:
                assert False
            print(char + colorama.Style.RESET_ALL, end='')
        print()

aoc.run_raw(main, "day20.txt")