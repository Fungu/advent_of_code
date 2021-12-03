use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let lines = buf_reader
        .lines()
        .map(|line| line.unwrap())
        .collect::<Vec<String>>();

    let line_len = lines.clone()[0].len();
    let most_common = get_most_common(lines.clone());

    let mut gamma: String = String::new();
    let mut epsilon: String = String::new();
    for i in 0..most_common.len() {
        if most_common[i] > 0 {
            gamma.push_str("1");
            epsilon.push_str("0");
        } else {
            gamma.push_str("0");
            epsilon.push_str("1");
        }
    }
    let gamma_decimal = isize::from_str_radix(&gamma, 2).unwrap();
    let epsilon_decimal = isize::from_str_radix(&epsilon, 2).unwrap();

    println!("Part 1: {}", gamma_decimal * epsilon_decimal);

    let mut oxygen_candidates = lines.clone();
    let mut co2_candidates = lines.clone();
    for i in 0..line_len {
        if oxygen_candidates.len() != 1 {
            let most_common = get_most_common(oxygen_candidates.clone());
            oxygen_candidates = oxygen_candidates
                .iter()
                .filter(|&x| (x.chars().nth(i).unwrap() == '1') == (most_common[i] >= 0))
                .cloned()
                .collect::<Vec<_>>();
        }
        if co2_candidates.len() != 1 {
            let most_common = get_most_common(co2_candidates.clone());
            co2_candidates = co2_candidates
                .iter()
                .filter(|&x| (x.chars().nth(i).unwrap() == '1') != (most_common[i] >= 0))
                .cloned()
                .collect::<Vec<_>>();
        }
    }

    let oxygen = isize::from_str_radix(&oxygen_candidates[0], 2).unwrap();
    let co2 = isize::from_str_radix(&co2_candidates[0], 2).unwrap();

    println!("Part 2: {}", oxygen * co2);

    Ok(())
}

fn get_most_common(values: Vec<String>) -> Vec<i32> {
    let line_len = values.clone()[0].len();
    let mut most_common = vec![0; line_len];
    for line in values.clone() {
        for i in 0..line_len {
            if line.chars().nth(i).unwrap() == '1' {
                most_common[i] += 1;
            } else {
                most_common[i] -= 1;
            }
        }
    }
    most_common
}
