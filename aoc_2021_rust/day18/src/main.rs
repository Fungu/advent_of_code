use std::{
    cmp,
    fs::File,
    io::{self, BufRead, BufReader},
    time::Instant,
};

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let lines = buf_reader
        .lines()
        .map(|line| line.unwrap())
        .collect::<Vec<String>>();
    let now = Instant::now();

    let answer = solve(lines);

    println!("Execution time: {} ms", now.elapsed().as_millis());
    println!("Part 1: {}", answer.0);
    println!("Part 2: {}", answer.1);

    Ok(())
}

fn solve(lines: Vec<String>) -> (u32, u32) {
    let mut result: Vec<String> = Vec::new();
    for line in &lines {
        if result.is_empty() {
            result = to_vec_string(&line);
        } else {
            result = add(&mut result, &mut to_vec_string(&line));
        }
    }
    let part1 = get_magnitude(&result);

    let mut part2 = 0;
    for a in 0..lines.len() {
        for b in 0..lines.len() {
            if a == b {
                continue;
            }
            let result = add(&mut to_vec_string(&lines[a]), &mut to_vec_string(&lines[b]));
            part2 = cmp::max(part2, get_magnitude(&result));
        }
    }

    (part1, part2)
}

fn add(left: &mut Vec<String>, right: &mut Vec<String>) -> Vec<String> {
    // To add two snailfish numbers, form a pair from the left and right parameters of the addition operator.
    let mut ret: Vec<String> = Vec::new();
    ret.push("[".to_string());
    ret.append(left);
    ret.push(",".to_string());
    ret.append(right);
    ret.push("]".to_string());
    while reduce(&mut ret) {}
    ret
}

fn reduce(snailfish: &mut Vec<String>) -> bool {
    // If any pair is nested inside four pairs, the leftmost such pair explodes.
    let mut depth = 0;
    for i in 0..snailfish.len() {
        if snailfish[i] == "[" {
            depth += 1;
            if depth == 5 {
                explode(snailfish, i);
                return true;
            }
        } else if snailfish[i] == "]" {
            depth -= 1;
        }
    }
    // If any regular number is 10 or greater, the leftmost such regular number splits.
    for i in 0..snailfish.len() {
        if is_string_numeric(&snailfish[i]) && snailfish[i].parse::<u32>().unwrap() >= 10 {
            split(snailfish, i);
            return true;
        }
    }
    false
}

fn explode(snailfish: &mut Vec<String>, index: usize) {
    // To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any),
    // and the pair's right value is added to the first regular number to the right of the exploding pair (if any).
    // Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.
    let left = snailfish[index + 1].parse::<u32>().unwrap();
    let right = snailfish[index + 3].parse::<u32>().unwrap();
    for i in (0..index).rev() {
        if is_string_numeric(&snailfish[i]) {
            snailfish[i] = (snailfish[i].parse::<u32>().unwrap() + left).to_string();
            break;
        }
    }
    for i in index + 4..snailfish.len() {
        if is_string_numeric(&snailfish[i]) {
            snailfish[i] = (snailfish[i].parse::<u32>().unwrap() + right).to_string();
            break;
        }
    }
    snailfish.remove(index);
    snailfish.remove(index);
    snailfish.remove(index);
    snailfish.remove(index);
    snailfish[index] = "0".to_string();
}

fn split(snailfish: &mut Vec<String>, index: usize) {
    // To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down,
    // while the right element of the pair should be the regular number divided by two and rounded up.
    let number = snailfish[index].parse::<u32>().unwrap();
    snailfish.remove(index);
    snailfish.insert(index + 0, "[".to_string());
    snailfish.insert(
        index + 1,
        ((number as f32 / 2_f32).floor() as u32).to_string(),
    );
    snailfish.insert(index + 2, ",".to_string());
    snailfish.insert(
        index + 3,
        ((number as f32 / 2_f32).ceil() as u32).to_string(),
    );
    snailfish.insert(index + 4, "]".to_string());
}

fn get_magnitude(snailfish: &Vec<String>) -> u32 {
    // The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right element.
    // The magnitude of a regular number is just that number.
    if snailfish.len() == 1 {
        return snailfish[0].parse::<u32>().unwrap();
    }
    let mut depth = 0;
    for i in 0..snailfish.len() {
        if snailfish[i] == "[" {
            depth += 1;
        } else if snailfish[i] == "]" {
            depth -= 1;
        } else if snailfish[i] == "," && depth == 1 {
            let (left, right) = snailfish.split_at(i);
            let mut left = left.to_vec();
            left.remove(0);
            let mut right = right.to_vec();
            right.remove(0);
            right.remove(right.len() - 1);
            return 3 * get_magnitude(&left) + 2 * get_magnitude(&right);
        }
    }
    panic!()
}

fn is_string_numeric(str: &String) -> bool {
    for c in str.chars() {
        if !c.is_numeric() {
            return false;
        }
    }
    return true;
}

fn to_vec_string(input: &String) -> Vec<String> {
    input
        .chars()
        .map(|c| c.to_string())
        .collect::<Vec<String>>()
}
