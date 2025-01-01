import aoc

def main(lines: list):
    part1 = 0
    for code in lines:
        code = code.strip()
        robot = enter_code(code, True)
        robot = enter_code(robot, False)
        me = enter_code(robot, False)
        part1 += len(me) * int(code[:-1])

    dp = {}
    part2 = 0
    for code in lines:
        robot = enter_code_part2({code.strip(): 1}, True, dp)
        for _ in range(25):
            robot = enter_code_part2(robot, False, dp)
        me = enter_code_part2(robot, False, dp)
        part2 += sum(me.values()) * int(code.strip()[:-1])
    
    return part1, part2

def enter_code(code: str, is_numeric: bool) -> str:
    ret = ""
    pos = "A"
    for c in code:
        ret += press_button(pos, c, is_numeric)
        pos = c
    return ret

def enter_code_part2(code_amount: dict[str, int], is_numeric: bool, dp: dict) -> dict[str, int]:
    ret = {}
    for code, amount in code_amount.items():
        pressed_buttons = []
        # The dp is not needed, but it reduces the execution time on my machine from 5 ms to 1 ms
        if (code, is_numeric) in dp:
            pressed_buttons = dp.get((code, is_numeric))
        else:
            pos = "A"
            for c in code:
                pressed_buttons.append(press_button(pos, c, is_numeric))
                pos = c
            dp[(code, is_numeric)] = pressed_buttons
        for buttons in pressed_buttons:
            if buttons not in ret:
                ret[buttons] = 0
            ret[buttons] += amount
    return ret

def press_button(start_pos, button, is_numeric) -> str:
    #+---+---+---+
    #| 7 | 8 | 9 |
    #+---+---+---+
    #| 4 | 5 | 6 |
    #+---+---+---+
    #| 1 | 2 | 3 |
    #+---+---+---+
    #    | 0 | A |
    #    +---+---+
    numeric = {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "0": (1, 3),
        "A": (2, 3)
    }
    #    +---+---+
    #    | ^ | A |
    #+---+---+---+
    #| < | v | > |
    #+---+---+---+
    directional = {
        "^": (1, 0),
        "A": (2, 0),
        "<": (0, 1),
        "v": (1, 1),
        ">": (2, 1)
    }
    keypad = (numeric if is_numeric else directional)
    delta_x = keypad.get(button)[0] - keypad.get(start_pos)[0]
    delta_y = keypad.get(button)[1] - keypad.get(start_pos)[1]
    ret = ""
    # The first 4 cases are for avoiding the empty spot in the keypads
    # We want to first push the buttons furthest from 'A', which is the left column buttons. 
    # We then push the middle column buttons, and finally the right column buttons.
    if is_numeric and keypad.get(start_pos)[1] == 3 and keypad.get(button)[1] != 3 and keypad.get(button)[0] == 0:
        if delta_y < 0:
            ret += "^" * abs(delta_y)
        if delta_x < 0:
            ret += "<" * abs(delta_x)
        if delta_x > 0:
            ret += ">" * abs(delta_x)
    elif is_numeric and keypad.get(start_pos)[1] != 3 and keypad.get(button)[1] == 3 and keypad.get(start_pos)[0] == 0:
        if delta_x < 0:
            ret += "<" * abs(delta_x)
        if delta_x > 0:
            ret += ">" * abs(delta_x)
        if delta_y > 0:
            ret += "v" * abs(delta_y)
    elif not is_numeric and keypad.get(start_pos) == (0, 1) and keypad.get(button)[1] != 1:
        if delta_x > 0:
            ret += ">" * abs(delta_x)
        if delta_x < 0:
            ret += "<" * abs(delta_x)
        if delta_y < 0:
            ret += "^" * abs(delta_y)
    elif not is_numeric and keypad.get(start_pos)[1] == 0 and keypad.get(button) == (0, 1):
        if delta_y > 0:
            ret += "v" * abs(delta_y)
        if delta_x > 0:
            ret += ">" * abs(delta_x)
        if delta_x < 0:
            ret += "<" * abs(delta_x)
    else:
        if delta_x < 0:
            ret += "<" * abs(delta_x)
        if delta_y < 0:
            ret += "^" * abs(delta_y)
        if delta_y > 0:
            ret += "v" * abs(delta_y)
        if delta_x > 0:
            ret += ">" * abs(delta_x)
    ret += "A"
    return ret

aoc.run_lines(main, "day21.txt")
