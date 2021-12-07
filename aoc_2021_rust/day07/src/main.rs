use std::{
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
    let values = lines[0]
        .split(",")
        .map(|v| v.parse::<i32>().unwrap())
        .collect::<Vec<i32>>();
    let min = *values.iter().min().unwrap();
    let max = *values.iter().max().unwrap();

    let mut part1 = std::i32::MAX;
    let mut part2 = std::i32::MAX;
    for target in min..max + 1 {
        let mut cost1 = 0;
        let mut cost2 = 0;
        for v in &values {
            let c = (v - target).abs();
            cost1 += c;
            cost2 += c * (c + 1) / 2;
        }
        part1 = part1.min(cost1);
        part2 = part2.min(cost2);
    }

    (part1, part2)
}
