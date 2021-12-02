use std::fs::File;
use std::io::{BufRead, BufReader, self};
use regex::Regex;

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let lines = buf_reader.lines();

    let regex = Regex::new(r"(?P<direction>\D*) (?P<value>\d*)").unwrap();
    
    let mut horizontal = 0;
    let mut depth_a = 0;
    let mut depth_b = 0;
    let mut aim = 0;

    for line in lines {
        let line = line.unwrap();
        let captures = regex.captures(&line).unwrap();
        let value = &captures["value"].parse::<i32>().unwrap();
        match &captures["direction"] {
            "forward" => {
                horizontal += value;
                depth_b += aim * value;
            },
            "down" => {
                depth_a += value;
                aim += value;
            },
            "up" => {
                depth_a -= value;
                aim -= value;
            },
            _ => panic!()
        }
    }

    println!("Part 1: {}", horizontal * depth_a);
    println!("Part 2: {}", horizontal * depth_b);
    Ok(())
}
