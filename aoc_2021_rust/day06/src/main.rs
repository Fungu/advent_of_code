use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let lines = buf_reader
        .lines()
        .map(|line| line.unwrap())
        .collect::<Vec<String>>();

    let mut fishes: Vec<i32> = Vec::new();
    for v in lines[0].split(",") {
        fishes.push(v.parse::<i32>().unwrap());
    }
    for _generation in 0..80 {
        let len = fishes.len();
        for i in 0..len {
            fishes[i] -= 1;
            if fishes[i] < 0 {
                fishes[i] = 6;
                fishes.push(8);
            }
        }
    }

    println!("Part 1: {}", fishes.len());

    let mut numbers: Vec<u64> = vec![0; 9];
    for v in lines[0].split(",") {
        numbers[v.parse::<i32>().unwrap() as usize] += 1;
    }
    for _generation in 0..256 {
        let mut next_numbers: Vec<u64> = vec![0; 9];
        for i in 0..8 {
            next_numbers[i] = numbers[i + 1];
        }
        next_numbers[6] += numbers[0];
        next_numbers[8] = numbers[0];
        numbers = next_numbers;
    }

    println!("Part 2: {}", numbers.iter().sum::<u64>());

    Ok(())
}
