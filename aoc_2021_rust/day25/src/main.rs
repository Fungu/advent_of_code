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
    let width = lines[0].len();
    let height = lines.len();

    let mut right = HashSet::new();
    let mut down = HashSet::new();
    for y in 0..lines.len() {
        for x in 0..lines[y].len() {
            let c = lines[y].chars().nth(x).unwrap();
            if c == '>' {
                right.insert((x, y));
            } else if c == 'v' {
                down.insert((x, y));
            }
        }
    }

    let mut part1 = 0;
    let mut moved = true;
    while moved {
        moved = false;
        part1 += 1;
        let mut next = HashSet::new();
        for cucumber in &right {
            let mut pos = (cucumber.0 + 1, cucumber.1);
            if pos.0 >= width {
                pos.0 = 0;
            }
            if right.contains(&pos) || down.contains(&pos) {
                pos = *cucumber;
            } else {
                moved = true;
            }
            next.insert(pos);
        }
        right = next;

        let mut next = HashSet::new();
        for cucumber in &down {
            let mut pos = (cucumber.0, cucumber.1 + 1);
            if pos.1 >= height {
                pos.1 = 0;
            }
            if right.contains(&pos) || down.contains(&pos) {
                pos = *cucumber;
            } else {
                moved = true;
            }
            next.insert(pos);
        }
        down = next;
    }

    (part1, "Merry Christmas!".to_string())
}
