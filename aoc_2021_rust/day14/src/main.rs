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

    let polymer = get_polymer(&pair_insertions, polymer_template.chars().collect(), 10);
    let quantities = get_quantities(&polymer);
    let part1 = get_score(quantities);

    let mut pair_insertions_20: HashMap<(char, char), HashMap<char, i64>> = HashMap::new();
    for ((left, right), _middle) in &pair_insertions {
        let polymer = get_polymer(&pair_insertions, vec![*left, *right], 20);
        let quantities = get_quantities(&polymer);
        pair_insertions_20.insert((*left, *right), quantities);
    }

    let mut quantities: HashMap<char, i64> = HashMap::new();
    let polymer: Vec<char> = polymer_template.chars().collect();
    let polymer = get_polymer(&pair_insertions, polymer, 20);
    for i in 0..polymer.len() - 1 {
        if i != 0 {
            modify_value(&mut quantities, polymer[i], -1);
        }
        let pair_quantities = pair_insertions_20
            .get(&(polymer[i], polymer[i + 1]))
            .unwrap();
        for (k, v) in pair_quantities {
            modify_value(&mut quantities, *k, *v);
        }
    }

    let part2 = get_score(quantities);

    (part1, part2)
}

fn get_polymer(
    pair_insertions: &HashMap<(char, char), char>,
    polymer: Vec<char>,
    iterations: i32,
) -> Vec<char> {
    let mut polymer: Vec<char> = polymer;
    for _iteration in 0..iterations {
        let mut next_polymer = Vec::new();
        for i in 0..polymer.len() - 1 {
            let key = (polymer[i], polymer[i + 1]);
            next_polymer.push(polymer[i]);
            next_polymer.push(pair_insertions[&key]);
        }
        next_polymer.push(polymer[polymer.len() - 1]);
        polymer = next_polymer;
    }
    polymer
}

fn get_quantities(polymer: &Vec<char>) -> HashMap<char, i64> {
    let mut quantities: HashMap<char, i64> = HashMap::new();
    for c in polymer {
        let a = &quantities.entry(*c).or_insert(0);
        let b = **a + 1;
        quantities.insert(*c, b);
    }
    quantities
}

fn get_score(quantities: HashMap<char, i64>) -> i64 {
    quantities.values().max().unwrap() - quantities.values().min().unwrap()
}

fn modify_value(map: &mut HashMap<char, i64>, key: char, value: i64) {
    let a = map.entry(key).or_insert(0);
    let a = *a + value;
    map.insert(key, a);
}
