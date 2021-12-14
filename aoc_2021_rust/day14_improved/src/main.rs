use std::{
    collections::HashMap,
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

fn solve(lines: Vec<String>) -> (i64, i64) {
    let polymer_template = &lines[0];
    let mut pair_insertions: HashMap<(char, char), char> = HashMap::new();
    for i in 2..lines.len() {
        let line = &lines[i];
        let split: Vec<&str> = line.split(" -> ").collect::<Vec<&str>>();
        pair_insertions.insert(
            (
                split[0].chars().nth(0).unwrap(),
                split[0].chars().nth(1).unwrap(),
            ),
            split[1].chars().nth(0).unwrap(),
        );
    }

    let part1 = simulate(&pair_insertions, polymer_template.to_string(), 10);
    let part2 = simulate(&pair_insertions, polymer_template.to_string(), 40);

    (part1, part2)
}

fn simulate(
    pair_insertions: &HashMap<(char, char), char>,
    polymer_template: String,
    iterations: i32,
) -> i64 {
    let polymer: Vec<char> = polymer_template.chars().collect();
    let mut pair_amounts: HashMap<(char, char), i64> = HashMap::new();
    for i in 0..polymer.len() - 1 {
        *pair_amounts
            .entry((polymer[i], polymer[i + 1]))
            .or_insert(0) += 1;
    }

    for _iteration in 0..iterations {
        let mut next_amount: HashMap<(char, char), i64> = HashMap::new();
        for (key, value) in &pair_amounts {
            let &middle = pair_insertions.get(&key).unwrap();
            *next_amount.entry((key.0, middle)).or_insert(0) += value;
            *next_amount.entry((middle, key.1)).or_insert(0) += value;
        }
        pair_amounts = next_amount;
    }

    // Count how many times each element occurs
    let mut quantities: HashMap<char, i64> = HashMap::new();
    for (key, value) in &pair_amounts {
        *quantities.entry(key.0).or_insert(0) += value;
        *quantities.entry(key.1).or_insert(0) += value;
    }
    // The first and last elements are only part of one pair
    let first = polymer_template.chars().nth(0).unwrap();
    let last = polymer_template.chars().last().unwrap();
    *quantities.entry(first).or_insert(0) += 1;
    *quantities.entry(last).or_insert(0) += 1;
    // The elements are part of two pairs, so we divide the amounts by 2
    quantities.iter_mut().for_each(|(_k, v)| *v = *v / 2);

    quantities.values().max().unwrap() - quantities.values().min().unwrap()
}
