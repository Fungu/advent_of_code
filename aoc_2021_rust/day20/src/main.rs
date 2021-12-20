use std::{
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
    let algorithm = &lines[0].chars().collect::<Vec<_>>();

    let mut grid: Vec<Vec<char>> = Vec::new();
    for line in lines[2..].iter() {
        let row = line.chars().collect::<Vec<_>>();
        grid.push(row);
    }

    let part1 = simulate(algorithm, &grid, 2);
    let part2 = simulate(algorithm, &grid, 50);

    (part1, part2)
}

fn simulate(algorithm: &Vec<char>, grid: &Vec<Vec<char>>, iterations: i32) -> i32 {
    let mut grid = grid.clone();
    let mut infinity = '.';
    for _i in 0..iterations {
        let mut next_grid: Vec<Vec<char>> = Vec::new();
        for y in -1..grid[0].len() as i32 + 1 {
            let mut next_row: Vec<char> = Vec::new();
            for x in -1..grid.len() as i32 + 1 {
                let mut key = 0;
                for yy in -1..=1 {
                    for xx in -1..=1 {
                        key <<= 1;
                        key += (get_or_default(&grid, x + xx, y + yy, infinity) == '#') as usize;
                    }
                }
                next_row.push(*algorithm.get(key).unwrap());
            }
            next_grid.push(next_row);
        }
        grid = next_grid;
        infinity = algorithm[if infinity == '.' {
            0
        } else {
            algorithm.len() - 1
        }];
    }

    grid.iter()
        .map(|f| f.iter().map(|g| (*g == '#') as i32).sum::<i32>())
        .sum()
}

fn get_or_default(grid: &Vec<Vec<char>>, x: i32, y: i32, default: char) -> char {
    if x < 0 || y < 0 || x as usize >= grid.len() || y as usize >= grid[0].len() {
        return default;
    }
    grid[y as usize][x as usize]
}
