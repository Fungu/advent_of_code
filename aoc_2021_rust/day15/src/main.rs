use std::{
    fs::File,
    io::{self, BufRead, BufReader},
    time::Instant, cmp::Ordering, collections::{BinaryHeap, HashSet},
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

fn solve(lines: Vec<String>) -> (u32, u32) {
    let mut grid: Vec<Vec<u32>> = Vec::new();
    for line in lines {
        let row = line
            .chars()
            .map(|c| (c.to_digit(10).unwrap()))
            .collect::<Vec<_>>();
        grid.push(row);
    }

    let part1 = astar(&grid);

    let width = grid[0].len();
    let height = grid.len();
    let mut big_grid: Vec<Vec<u32>> = Vec::new();
    for y in 0..(height * 5) {
        let mut row: Vec<u32> = Vec::new();
        for x in 0..(width * 5) {
            let mut value = grid[y % height][x % width];
            value += (x / width) as u32;
            value += (y / height) as u32;
            while value > 9 {
                value -= 9;
            }
            row.push(value);
        }
        big_grid.push(row);
    }

    let part2 = astar(&big_grid);

    (part1, part2)
}

fn astar(grid: &Vec<Vec<u32>>) -> u32 {
    let end = (grid[0].len() as i32 - 1, grid.len() as i32 - 1);
    let mut closed_set: HashSet<(i32, i32)> = HashSet::new();
    let mut open_set = BinaryHeap::new();
    open_set.push(Node { g: 0, f: 0, pos: (0, 0) });

    while let Some(node) = open_set.pop() {
        if node.pos == end {
            return node.g;
        }
        closed_set.insert(node.pos);
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let nx = node.pos.0 + dx;
            let ny = node.pos.1 + dy;
            if nx >= 0 && ny >= 0 && nx <= end.0 && ny <= end.1 && !closed_set.contains(&(nx, ny)) {
                let ng = node.g + grid[ny as usize][nx as usize];
                let h = (end.0 - nx + end.1 - ny)  as u32;
                open_set.push(Node { 
                    g: ng, 
                    f: ng + h, 
                    pos: (nx, ny) });
            }
        }
    }
    0
}

#[derive(Copy, Clone, Eq, PartialEq)]
struct Node {
    g: u32, // Cost
    f: u32, // Guess
    pos: (i32, i32),
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.f.cmp(&self.f).then_with(|| self.pos.cmp(&other.pos))
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
