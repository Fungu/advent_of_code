use std::{
    cmp,
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

fn solve(lines: Vec<String>) -> (String, String) {
    let mut sections: Vec<(i64, i64, i64)> = Vec::new();
    for i in 0..14 {
        // a comes from 'div z a' on line 4
        let a = lines[i * 18 + 4].split(" ").collect::<Vec<&str>>()[2]
            .parse::<i64>()
            .unwrap();
        // b comes from 'add x b' on line 5
        let b = lines[i * 18 + 5].split(" ").collect::<Vec<&str>>()[2]
            .parse::<i64>()
            .unwrap();
        // c comes from 'add y c' on line 15
        let c = lines[i * 18 + 15].split(" ").collect::<Vec<&str>>()[2]
            .parse::<i64>()
            .unwrap();
        assert!(a == 1 || a == 26);
        assert!(a == 1 || b < 10);
        assert!(c > 0);
        sections.push((a, b, c));
    }

    let mut pairs: Vec<(usize, usize)> = Vec::new();
    let mut stack = Vec::new();
    for i in 0..sections.len() {
        let a = sections[i].0;
        if a == 1 {
            stack.push(i);
        } else {
            let other = stack.pop().unwrap();
            pairs.push((other, i));
        }
    }

    let part1 = find_digits(&sections, &pairs, 9, cmp::max);
    let part2 = find_digits(&sections, &pairs, 1, cmp::min);

    (part1, part2)
}

fn find_digits(
    sections: &Vec<(i64, i64, i64)>,
    pairs: &Vec<(usize, usize)>,
    fixed_int: i64,
    minmax: fn(i64, i64) -> i64,
) -> String {
    let mut digits = [0; 14];
    for &(index_a, index_b) in pairs {
        let mut digit_a = fixed_int;
        let mut digit_b = digit_a + sections[index_a].2 + sections[index_b].1;
        let margin = minmax(digit_a, digit_b) - fixed_int;
        digit_a -= margin;
        digit_b -= margin;
        digits[index_a] = digit_a;
        digits[index_b] = digit_b;
    }
    digits.iter().map(|i| i.to_string()).collect::<String>()
}
