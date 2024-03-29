import aoc
import re

def main(raw_input):
    passport_list = [{pair.split(":")[0] : pair.split(":")[1] for pair in passport.replace("\n", " ").split(" ")} for passport in raw_input.split("\n\n")]
    
    passport_list = list(filter(has_required_fields, passport_list))
    part1 = len(passport_list)

    passport_list = list(filter(is_valid, passport_list))
    part2 = len(passport_list)

    return part1, part2

def has_required_fields(passport):
    return all((field in passport) for field in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])

def is_valid(passport):
    #byr (Birth Year) - four digits; at least 1920 and at most 2002.
    if not (1920 <= int(passport["byr"]) <= 2002):
        return False
    #iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    if not (2010 <= int(passport["iyr"]) <= 2020):
        return False
    #eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    if not (2020 <= int(passport["eyr"]) <= 2030):
        return False
    #hgt (Height) - a number followed by either cm or in:
    if "cm" in passport["hgt"]:
        #If cm, the number must be at least 150 and at most 193.
        if not (150 <= int(passport["hgt"].replace("cm", "")) <= 193):
            return False
    elif "in" in passport["hgt"]:
        #If in, the number must be at least 59 and at most 76.
        if not (59 <= int(passport["hgt"].replace("in", "")) <= 76):
            return False
    else:
        return False
    #hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if not re.compile("^#([0-9, a-f]){6}$").match(passport["hcl"]):
        return False
    #ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if passport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False
    #pid (Passport ID) - a nine-digit number, including leading zeroes.
    if not re.compile("^[0-9]{9}$").match(passport["pid"]):
        return False
    #cid (Country ID) - ignored, missing or not.
    return True

aoc.run_raw(main, "day04.txt")