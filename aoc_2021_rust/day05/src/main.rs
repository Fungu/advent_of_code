use regex::Regex;
use std::{
    collections::HashMap,
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let lines = buf_reader
        .lines()
        .map(|line| line.unwrap())
        .collect::<Vec<String>>();

    let mut diagram1: HashMap<(i32, i32), i32> = HashMap::new();
    let mut diagram2: HashMap<(i32, i32), i32> = HashMap::new();

    let regex = Regex::new(r"(?P<x1>\d*),(?P<y1>\d*) -> (?P<x2>\d*),(?P<y2>\d*)").unwrap();
    for line in lines {
        let captures = regex.captures(&line).unwrap();
        let x1 = captures["x1"].parse::<i32>().unwrap();
        let y1 = captures["y1"].parse::<i32>().unwrap();
        let x2 = captures["x2"].parse::<i32>().unwrap();
        let y2 = captures["y2"].parse::<i32>().unwrap();
        let dx = clamp(x2 - x1, -1, 1);
        let dy = clamp(y2 - y1, -1, 1);
        let mut x = x1;
        let mut y = y1;
        loop {
            if dx == 0 || dy == 0 {
                increase(&mut diagram1, (x, y));
            }
            increase(&mut diagram2, (x, y));
            if x == x2 && y == y2 {
                break;
            }
            x += dx;
            y += dy;
        }
    }

    let part1 = diagram1.values().filter(|v| **v >= 2).count();
    println!("Part 1: {}", part1);

    let part2 = diagram2.values().filter(|v| **v >= 2).count();
    println!("Part 2: {}", part2);

    Ok(())
}

fn clamp(value: i32, min: i32, max: i32) -> i32 {
    if value > max {
        max
    } else if value < min {
        min
    } else {
        value
    }
}

fn increase(diagram: &mut HashMap<(i32, i32), i32>, key: (i32, i32)) {
    let count = diagram.entry(key).or_insert(0);
    *count += 1;
}
