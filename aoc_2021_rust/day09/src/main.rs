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

fn solve(lines: Vec<String>) -> (u32, i32) {
    let mut grid: Vec<Vec<u32>> = Vec::new();
    for line in lines {
        let row = line
            .chars()
            .map(|c| (c.to_digit(10).unwrap()))
            .collect::<Vec<_>>();
        grid.push(row);
    }

    let mut low_points: Vec<(i32, i32)> = Vec::new();
    let directions: [(i32, i32); 4] = [(-1, 0), (0, -1), (1, 0), (0, 1)];
    let mut part1 = 0;
    let height = grid.clone().len();
    let width = grid.clone()[0].len();
    for y in 0..height {
        for x in 0..width {
            let height = grid[y][x];
            let mut low_point = true;
            for (dx, dy) in directions {
                let nx = (x as i32) + dx;
                let ny = (y as i32) + dy;
                if in_bounds(&grid, nx, ny) && grid[ny as usize][nx as usize] <= height {
                    low_point = false;
                }
            }
            if low_point {
                part1 += height + 1;
                low_points.push((x as i32, y as i32));
            }
        }
    }
    let mut sizes: Vec<i32> = Vec::new();
    for low_point in low_points {
        let mut size = 0;
        let mut openset: Vec<(i32, i32)> = Vec::new();
        let mut closedset: Vec<(i32, i32)> = Vec::new();
        openset.push(low_point);
        while !openset.is_empty() {
            let point = openset.pop().unwrap();
            closedset.push(point);
            if grid[point.1 as usize][point.0 as usize] != 9 {
                size += 1;
                for (dx, dy) in directions {
                    let nx = (point.0 as i32) + dx;
                    let ny = (point.1 as i32) + dy;
                    let next_point = (nx, ny);
                    if !closedset.contains(&next_point)
                        && !openset.contains(&next_point)
                        && in_bounds(&grid, nx, ny)
                    {
                        openset.push(next_point);
                    }
                }
            }
        }
        sizes.push(size);
    }
    sizes.sort();
    sizes.reverse();
    let part2 = sizes[0] * sizes[1] * sizes[2];

    (part1, part2)
}

fn in_bounds(grid: &Vec<Vec<u32>>, x: i32, y: i32) -> bool {
    x >= 0 && y >= 0 && (x as usize) < grid[0].len() && (y as usize) < grid.len()
}
