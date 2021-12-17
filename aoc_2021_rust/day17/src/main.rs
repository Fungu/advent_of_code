use regex::Regex;
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

fn solve(lines: Vec<String>) -> (i32, i32) {
    let regex =
        Regex::new(r"target area: x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)")
            .unwrap();
    let captures = regex.captures(&lines[0]).unwrap();
    let x1 = captures["x1"].parse::<i32>().unwrap();
    let x2 = captures["x2"].parse::<i32>().unwrap();
    let y1 = captures["y1"].parse::<i32>().unwrap();
    let y2 = captures["y2"].parse::<i32>().unwrap();
    assert!(x2 > x1);
    assert!(x1 > 0);
    assert!(y2 > y1);
    assert!(y1 < 0);

    let mut part1 = 0;
    let mut part2 = 0;
    for dx_start in 1..x2 + 1 {
        for dy_start in y1..-y1 + 1 {
            let mut dx = dx_start;
            let mut dy = dy_start;
            let mut x = 0;
            let mut y = 0;
            let mut highest_y = 0;
            loop {
                x += dx;
                y += dy;
                highest_y = cmp::max(y, highest_y);
                if x >= x1 && x <= x2 && y >= y1 && y <= y2 {
                    part1 = cmp::max(part1, highest_y);
                    part2 += 1;
                    break;
                }
                if y < y1 || x > x2 || (dx == 0 && x < x1) {
                    break;
                }
                if dx > 0 {
                    dx -= 1
                }
                dy -= 1;
            }
        }
    }

    (part1, part2)
}
