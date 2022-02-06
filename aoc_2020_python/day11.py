import aoc

def main(input_lines):
    every_direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    height = len(input_lines)
    width = len(input_lines[0].strip())

    state = {}
    adjacent_seats = {}
    seen_seats = {}
    for row in range(height):
        for col in range(width):
            if input_lines[row][col] != ".":
                adjacent_seats[(row, col)] = []
                seen_seats[(row, col)] = []
                state[(row, col)] = input_lines[row][col] == "#"
                for d_row, d_col in every_direction:
                    row_pos = row + d_row
                    col_pos = col + d_col
                    direct_neighbor = True
                    while 0 <= row_pos < height and 0 <= col_pos < width:
                        if input_lines[row_pos][col_pos] != ".":
                            if direct_neighbor:
                                adjacent_seats[(row, col)].append((row_pos, col_pos))
                            seen_seats[(row, col)].append((row_pos, col_pos))
                            break
                        direct_neighbor = False
                        row_pos += d_row
                        col_pos += d_col

    part1 = simulate_until_stable(state, adjacent_seats, max_neighbors=4)
    part2 = simulate_until_stable(state, seen_seats, max_neighbors=5)
    
    return part1, part2

def simulate_until_stable(state, adjacent_seats, max_neighbors):
    state_copy = state.copy()
    result_changed = True
    while result_changed:
        state_copy, result_changed = simulate(state_copy, adjacent_seats, max_neighbors)
    ret = 0
    for seat in state_copy:
        if state_copy[seat]:
            ret += 1
    return ret

def simulate(state, adjacent_seats, max_neighbors):
    result = {}
    result_changed = False

    for key in state.keys():
        neighbors = 0
        for seat in adjacent_seats[key]:
            if state[seat]:
                neighbors += 1
        if state[key] and neighbors >= max_neighbors:
            result[key] = False
            result_changed = True
        elif not state[key] and neighbors == 0:
            result[key] = True
            result_changed = True
        else:
            result[key] = state[key]

    return result, result_changed

aoc.run_lines(main, "day11.txt")