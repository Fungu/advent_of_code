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

fn solve(lines: Vec<String>) -> (usize, i32) {
    let mut scanners: Vec<Vec<[i32; 3]>> = Vec::new();
    let mut beacons_temp: Vec<[i32; 3]> = Vec::new();
    for line in lines {
        if line.starts_with("---") {
            if !beacons_temp.is_empty() {
                scanners.push(beacons_temp);
            }
            beacons_temp = Vec::new();
        } else if !line.is_empty() {
            let s: Vec<&str> = line.split(",").collect();
            beacons_temp.push([
                s[0].parse::<i32>().unwrap(),
                s[1].parse::<i32>().unwrap(),
                s[2].parse::<i32>().unwrap(),
            ]);
        }
    }
    scanners.push(beacons_temp);

    let mut beacons: Vec<[i32; 3]> = scanners.pop().unwrap();
    let mut scanner_positions: Vec<[i32; 3]> = Vec::new();
    scanner_positions.push([0, 0, 0]);
    let mut volumes: Vec<Volume> = Vec::new();

    while !scanners.is_empty() {
        let mut i = 0;
        while i < scanners.len() {
            if match_scanner(
                &scanners[i],
                &mut beacons,
                &mut scanner_positions,
                &mut volumes,
            ) {
                scanners.remove(i);
            } else {
                i += 1;
            }
        }
    }

    let part1 = beacons.len();
    let mut part2 = 0;
    for a in 0..scanner_positions.len() {
        for b in 0..scanner_positions.len() {
            if a != b {
                part2 = cmp::max(
                    part2,
                    i32::abs(scanner_positions[a][0] - scanner_positions[b][0])
                        + i32::abs(scanner_positions[a][1] - scanner_positions[b][1])
                        + i32::abs(scanner_positions[a][2] - scanner_positions[b][2]),
                );
            }
        }
    }

    (part1, part2)
}

fn match_scanner(
    scanner: &Vec<[i32; 3]>,
    beacons: &mut Vec<[i32; 3]>,
    scanner_positions: &mut Vec<[i32; 3]>,
    volumes: &mut Vec<Volume>,
) -> bool {
    let rotations = [
        [(1, 0), (1, 1), (1, 2)],
        [(1, 0), (1, 2), (-1, 1)],
        [(1, 0), (-1, 1), (-1, 2)],
        [(1, 0), (-1, 2), (1, 1)],
        [(1, 1), (-1, 0), (1, 2)],
        [(1, 1), (1, 2), (1, 0)],
        [(1, 1), (1, 0), (-1, 2)],
        [(1, 1), (-1, 2), (-1, 0)],
        [(-1, 0), (-1, 1), (1, 2)],
        [(-1, 0), (-1, 2), (-1, 1)],
        [(-1, 0), (1, 1), (-1, 2)],
        [(-1, 0), (1, 2), (1, 1)],
        [(-1, 1), (1, 0), (1, 2)],
        [(-1, 1), (-1, 2), (1, 0)],
        [(-1, 1), (-1, 0), (-1, 2)],
        [(-1, 1), (1, 2), (-1, 0)],
        [(1, 2), (1, 1), (-1, 0)],
        [(1, 2), (1, 0), (1, 1)],
        [(1, 2), (-1, 1), (1, 0)],
        [(1, 2), (-1, 0), (-1, 1)],
        [(-1, 2), (-1, 1), (-1, 0)],
        [(-1, 2), (-1, 0), (1, 1)],
        [(-1, 2), (1, 1), (1, 0)],
        [(-1, 2), (1, 0), (-1, 1)],
    ];
    for r in rotations {
        let mut rotated_beacons: Vec<[i32; 3]> = Vec::new();
        for beacon in scanner {
            rotated_beacons.push([
                r[0].0 * beacon[r[0].1],
                r[1].0 * beacon[r[1].1],
                r[2].0 * beacon[r[2].1],
            ]);
        }
        for anchor in &*beacons {
            for anchor2 in &rotated_beacons {
                let mut matches = 0;
                let delta = [
                    anchor[0] - anchor2[0],
                    anchor[1] - anchor2[1],
                    anchor[2] - anchor2[2],
                ];
                for test_beacon in &rotated_beacons {
                    let pos = [
                        test_beacon[0] + delta[0],
                        test_beacon[1] + delta[1],
                        test_beacon[2] + delta[2],
                    ];
                    if beacons.contains(&pos) {
                        matches += 1;
                    } else if volumes.iter().any(|v| v.contains(pos)) {
                        break;
                    }
                    if matches >= 12 {
                        break;
                    }
                }
                if matches >= 12 {
                    for test_beacon in &rotated_beacons {
                        let pos = [
                            test_beacon[0] + delta[0],
                            test_beacon[1] + delta[1],
                            test_beacon[2] + delta[2],
                        ];
                        if !beacons.contains(&pos) {
                            beacons.push(pos);
                        }
                        scanner_positions.push(delta);
                    }
                    volumes.push(Volume::new(&rotated_beacons, &delta));
                    return true;
                }
            }
        }
    }
    false
}

struct Volume {
    min_x: i32,
    min_y: i32,
    min_z: i32,
    max_x: i32,
    max_y: i32,
    max_z: i32,
}

impl Volume {
    pub fn new(beacons: &Vec<[i32; 3]>, delta: &[i32; 3]) -> Self {
        let mut min_x = i32::MAX;
        let mut min_y = i32::MAX;
        let mut min_z = i32::MAX;
        let mut max_x = i32::MIN;
        let mut max_y = i32::MIN;
        let mut max_z = i32::MIN;
        for b in &*beacons {
            min_x = cmp::min(min_x, b[0] + delta[0]);
            min_y = cmp::min(min_y, b[1] + delta[1]);
            min_z = cmp::min(min_z, b[2] + delta[2]);
            max_x = cmp::max(max_x, b[0] + delta[0]);
            max_y = cmp::max(max_y, b[1] + delta[1]);
            max_z = cmp::max(max_z, b[2] + delta[2]);
        }
        Self {
            min_x,
            min_y,
            min_z,
            max_x,
            max_y,
            max_z,
        }
    }

    pub fn contains(&self, pos: [i32; 3]) -> bool {
        pos[0] >= self.min_x
            && pos[0] <= self.max_x
            && pos[1] >= self.min_y
            && pos[1] <= self.max_y
            && pos[2] >= self.min_z
            && pos[2] <= self.max_z
    }
}
