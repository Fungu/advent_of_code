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

fn solve(lines: Vec<String>) -> (u64, u64) {
    let part1 = simulate(&lines, 80);
    let part2 = simulate(&lines, 256);

    (part1, part2)
}

fn simulate(lines: &Vec<String>, generations: u32) -> u64 {
    let mut numbers: Vec<u64> = vec![0; 9];
    for v in lines[0].split(",") {
        numbers[v.parse::<i32>().unwrap() as usize] += 1;
    }
    for _generation in 0..generations {
        let mut next_numbers: Vec<u64> = vec![0; 9];
        for i in 0..8 {
            next_numbers[i] = numbers[i + 1];
        }
        next_numbers[6] += numbers[0];
        next_numbers[8] = numbers[0];
        numbers = next_numbers;
    }
    numbers.iter().sum::<u64>()
}
