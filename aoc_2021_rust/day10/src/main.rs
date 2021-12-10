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

fn solve(lines: Vec<String>) -> (i32, u64) {
    let pairs: HashMap<char, char> =
        HashMap::from([('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]);
    let costs: HashMap<char, i32> = HashMap::from([(')', 3), (']', 57), ('}', 1197), ('>', 25137)]);
    let costs2: HashMap<char, u64> = HashMap::from([('(', 1), ('[', 2), ('{', 3), ('<', 4)]);

    let mut scores: Vec<u64> = Vec::new();
    let mut part1 = 0;
    for line in lines {
        let mut stack: Vec<char> = Vec::new();
        let mut corrupted = false;
        for c in line.chars() {
            if pairs.contains_key(&c) {
                stack.push(c);
            } else {
                let cc = stack.pop().unwrap_or('x');
                if pairs.get(&cc).unwrap() != &c {
                    part1 += costs.get(&c).unwrap();
                    corrupted = true;
                    break;
                }
            }
        }
        if !corrupted {
            let mut score: u64 = 0;
            while !stack.is_empty() {
                score *= 5;
                let c = stack.pop().unwrap();
                score += costs2.get(&c).unwrap();
            }
            scores.push(score);
        }
    }
    scores.sort();
    let part2 = *scores.get(scores.len() / 2).unwrap();

    (part1, part2)
}
