use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let values = buf_reader
        .lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .collect::<Vec<i32>>();

    let part1 = count_increases(values.clone());

    let mut sliding_values: Vec<i32> = Vec::new();
    for i in 0..values.len() - 2 {
        sliding_values.push(values[i] + values[i + 1] + values[i + 2]);
    }

    let part2 = count_increases(sliding_values.clone());

    println!("Part 1: {}", part1);
    println!("Part 2: {}", part2);

    Ok(())
}

fn count_increases(values: Vec<i32>) -> i32 {
    let mut ret = 0;
    for i in 0..values.len() - 1 {
        if values[i + 1] > values[i] {
            ret += 1;
        }
    }
    ret
}
