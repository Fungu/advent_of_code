use regex::Regex;
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

fn solve(lines: Vec<String>) -> (i64, i64) {
    let regex = Regex::new(r"(?P<on_off>.+) x=(?P<x1>-?\d+)\.\.(?P<x2>-?\d+),y=(?P<y1>-?\d+)\.\.(?P<y2>-?\d+),z=(?P<z1>-?\d+)\.\.(?P<z2>-?\d+)").unwrap();
    let cubes: Vec<Cube> = lines
        .iter()
        .map(|l| Cube::new(l.to_string(), &regex))
        .collect();

    let part1 = reboot(&cubes, true);
    let part2 = reboot(&cubes, false);

    (part1, part2)
}

fn reboot(input_cubes: &Vec<Cube>, part1: bool) -> i64 {
    let mut cubes: Vec<Cube> = Vec::new();
    for new_cube in input_cubes {
        if part1 && !new_cube.is_initialization_area() {
            continue;
        }
        let mut next_cubes: Vec<Cube> = Vec::new();
        for cube in &cubes {
            if cube.intersects(&new_cube) {
                let temp = reduce(&cube, &new_cube);
                for t in temp {
                    next_cubes.push(t);
                }
            } else {
                next_cubes.push(cube.clone());
            }
        }
        if new_cube.on {
            next_cubes.push(new_cube.clone());
        }
        cubes = next_cubes;
    }
    cubes.iter().map(|c| c.volume()).sum()
}

fn reduce(cube: &Cube, other: &Cube) -> Vec<Cube> {
    let mut ret = Vec::new();
    for dx in -1..=1 {
        for dy in -1..=1 {
            for dz in -1..=1 {
                if dx == 0 && dy == 0 && dz == 0 {
                    continue;
                }
                let mut new_cube = cube.clone();
                let section = [dx, dy, dz];
                for axis in 0..3 {
                    if section[axis] == -1 {
                        new_cube.bounds[axis][0] = other.bounds[axis][1] + 1;
                    } else if section[axis] == 1 {
                        new_cube.bounds[axis][1] = other.bounds[axis][0] - 1;
                    } else {
                        new_cube.bounds[axis][0] =
                            cmp::max(new_cube.bounds[axis][0], other.bounds[axis][0]);
                        new_cube.bounds[axis][1] =
                            cmp::min(new_cube.bounds[axis][1], other.bounds[axis][1]);
                    }
                }
                if new_cube.valid() {
                    ret.push(new_cube);
                }
            }
        }
    }
    ret
}

#[derive(Clone)]
struct Cube {
    on: bool,
    bounds: [[i64; 2]; 3],
}

impl Cube {
    fn new(line: String, regex: &Regex) -> Cube {
        let c = regex.captures(&line).unwrap();
        let on = c["on_off"] == *"on";
        let x1 = c["x1"].parse::<i64>().unwrap();
        let x2 = c["x2"].parse::<i64>().unwrap();
        let y1 = c["y1"].parse::<i64>().unwrap();
        let y2 = c["y2"].parse::<i64>().unwrap();
        let z1 = c["z1"].parse::<i64>().unwrap();
        let z2 = c["z2"].parse::<i64>().unwrap();
        assert!(x1 <= x2 && y1 <= y2 && z1 <= z2);
        Cube {
            on,
            bounds: [[x1, x2], [y1, y2], [z1, z2]],
        }
    }

    fn intersects(&self, other: &Cube) -> bool {
        for axis in 0..3 {
            if self.bounds[axis][0] > other.bounds[axis][1]
                || self.bounds[axis][1] < other.bounds[axis][0]
            {
                return false;
            }
        }
        true
    }

    fn valid(&self) -> bool {
        self.bounds.iter().all(|a| a[0] <= a[1])
    }

    fn volume(&self) -> i64 {
        self.bounds
            .iter()
            .map(|a| a[1] - a[0] + 1)
            .reduce(|a, b| a * b)
            .unwrap()
    }

    fn is_initialization_area(&self) -> bool {
        self.bounds.iter().all(|a| a[0] >= -50 && a[1] <= 50)
    }
}
