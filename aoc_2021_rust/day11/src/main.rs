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

fn solve(lines: Vec<String>) -> (i32, u64) {
    let mut grid: Vec<Vec<u32>> = Vec::new();
    for line in lines {
        let row = line
            .chars()
            .map(|c| (c.to_digit(10).unwrap()))
            .collect::<Vec<_>>();
        grid.push(row);
    }
    let directions: [(i32, i32); 8] = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    ];

    let mut part1 = 0;
    let mut step = 0;
    loop {
        step += 1;

        let mut openset: Vec<(usize, usize)> = Vec::new();
        let mut closedset: Vec<(usize, usize)> = Vec::new();
        for y in 0..10 {
            for x in 0..10 {
                grid[y][x] += 1;
                if grid[y][x] > 9 {
                    openset.push((x, y));
                }
            }
        }
        while !openset.is_empty() {
            if step <= 100 {
                part1 += 1;
            }
            let point = openset.pop().unwrap();
            grid[point.1][point.0] = 0;
            closedset.push((point.0, point.1));
            for (dx, dy) in directions {
                let nx = (point.0 as i32) + dx;
                let ny = (point.1 as i32) + dy;
                let np = (nx as usize, ny as usize);
                if nx >= 0
                    && ny >= 0
                    && nx <= 9
                    && ny <= 9
                    && !closedset.contains(&np)
                    && !openset.contains(&np)
                {
                    grid[np.1][np.0] += 1;
                    if grid[np.1][np.0] > 9 {
                        openset.push(np);
                    }
                }
            }
        }
        if closedset.len() == 100 {
            break;
        }
    }

    (part1, step)
}
