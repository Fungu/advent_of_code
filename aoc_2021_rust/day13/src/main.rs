use std::{
    collections::HashSet,
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

fn solve(lines: Vec<String>) -> (i32, String) {
    let mut dots: Vec<(i32, i32)> = Vec::new();
    let mut dots_finished = false;
    let mut part1 = -1;
    for line in lines.iter() {
        if line.is_empty() {
            dots_finished = true;
        } else if !dots_finished {
            let split: Vec<i32> = line
                .split(",")
                .map(|f| f.parse::<i32>().unwrap())
                .collect::<Vec<i32>>();
            dots.push((split[0], split[1]));
        } else {
            let fold = line.split("=").collect::<Vec<&str>>();
            let line_pos = fold[1].parse::<i32>().unwrap();
            for i in (0 as usize)..dots.len() {
                if fold[0].ends_with("x") {
                    if dots[i].0 > line_pos {
                        dots[i].0 = 2 * line_pos - dots[i].0;
                    }
                } else {
                    if dots[i].1 > line_pos {
                        dots[i].1 = 2 * line_pos - dots[i].1;
                    }
                }
            }
            if part1 == -1 {
                let hashset: HashSet<(i32, i32)> = HashSet::from_iter(dots.iter().cloned());
                part1 = hashset.len() as i32;
            }
        }
    }

    let part2 = get_printable(&dots);

    (part1, part2)
}

fn get_printable(dots: &Vec<(i32, i32)>) -> String {
    let max_x = dots.iter().map(|f| f.0).max().unwrap();
    let max_y = dots.iter().map(|f| f.1).max().unwrap();
    let mut ret = "\n".to_string();
    for y in 0..max_y + 1 {
        for x in 0..max_x + 1 {
            if dots.contains(&(x, y)) {
                ret.push('#');
            } else {
                ret.push(' ');
            }
        }
        ret.push('\n');
    }
    ret
}
