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

fn solve(lines: Vec<String>) -> (i32, i32) {
    let mut part1 = 0;
    let mut part2 = 0;
    for line in lines {
        let splitted = line.split(" | ").collect::<Vec<&str>>();
        let left = splitted[0].split(" ").collect::<Vec<&str>>();
        let right = splitted[1].split(" ").collect::<Vec<&str>>();
        for r in &right {
            if [2, 4, 3, 7].contains(&(r.len() as i32)) {
                part1 += 1;
            }
        }
        let mapping = get_mapping(left);
        part2 += {
            let mut temp = 0;
            for s in right {
                let s = get_sorted(s);
                for entry in &mapping {
                    if entry.1.eq(&s) {
                        temp *= 10;
                        temp += entry.0;
                    }
                }
            }
            temp
        }
    }

    (part1, part2)
}

fn get_mapping(left: Vec<&str>) -> HashMap<i32, String> {
    let mut mapping: HashMap<i32, String> = HashMap::new();
    while mapping.len() < 10 {
        for r in &left {
            let signals = get_sorted(r);
            let number = match &(signals.len() as i32) {
                // 1, 4, 7, 8
                2 => 1,
                4 => 4,
                3 => 7,
                7 => 8,
                // 2, 3, 5
                5 => {
                    if mapping.contains_key(&1)
                        && contains_chars(signals.clone(), get(mapping.clone(), 1))
                    {
                        3
                    } else if mapping.contains_key(&9)
                        && contains_chars(get(mapping.clone(), 9), signals.clone())
                    {
                        5
                    } else if mapping.contains_key(&3) && mapping.contains_key(&5) {
                        2
                    } else {
                        -1
                    }
                }
                // 6, 9, 0
                6 => {
                    if mapping.contains_key(&1)
                        && !contains_chars(signals.clone(), get(mapping.clone(), 1))
                    {
                        6
                    } else if mapping.contains_key(&3)
                        && contains_chars(signals.clone(), get(mapping.clone(), 3))
                    {
                        9
                    } else if mapping.contains_key(&6) && mapping.contains_key(&9) {
                        0
                    } else {
                        -1
                    }
                }
                _ => -1,
            };
            if number != -1 {
                mapping.insert(number, signals);
            }
        }
    }
    mapping
}

fn get_sorted(s: &str) -> String {
    let mut chars: Vec<char> = s.chars().collect();
    chars.sort_by(|a, b| b.cmp(a));
    String::from_iter(chars)
}

fn contains_chars(string: String, chars: String) -> bool {
    for c in chars.chars() {
        if !string.contains(c) {
            return false;
        }
    }
    true
}

fn get(mapping: HashMap<i32, String>, key: i32) -> String {
    mapping.get(&key).unwrap().to_string()
}
