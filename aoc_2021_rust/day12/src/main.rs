use std::{
    collections::{HashMap, HashSet},
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
    let mut connections: HashMap<&str, Vec<&str>> = HashMap::new();
    for line in lines.iter() {
        let a: Vec<&str> = line.split("-").collect::<Vec<&str>>();
        let left = a.get(0).unwrap();
        let right = a.get(1).unwrap();
        assert!(
            left.chars().nth(0).unwrap().is_lowercase()
                || right.chars().nth(0).unwrap().is_lowercase()
        );
        connections
            .entry(left)
            .or_insert(<Vec<&str>>::new())
            .push(right);
        connections
            .entry(right)
            .or_insert(<Vec<&str>>::new())
            .push(left);
    }

    let closed_set: &mut HashSet<&str> = &mut HashSet::new();
    let start = "start";
    let part1 = traverse(&connections, start, closed_set, true);
    let part2 = traverse(&connections, start, closed_set, false);

    (part1, part2)
}

fn traverse(
    connections: &HashMap<&str, Vec<&str>>,
    node: &str,
    closed_set: &mut HashSet<&str>,
    used_extra_visit: bool,
) -> i32 {
    let mut ret = 0;
    let mut closed = closed_set.clone();
    if node.chars().nth(0).unwrap().is_lowercase() {
        closed.insert(node);
    }
    if node == "end" {
        return 1;
    }
    for neighbor in connections.get(&node).unwrap() {
        if closed.contains(neighbor) && !used_extra_visit && *neighbor != "start" {
            ret += traverse(&connections, neighbor, &mut closed, true);
        }
        if !closed.contains(neighbor) {
            ret += traverse(&connections, neighbor, &mut closed, used_extra_visit);
        }
    }
    ret
}
