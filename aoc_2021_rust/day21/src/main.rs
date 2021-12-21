use regex::Regex;
use std::{
    cmp,
    collections::HashMap,
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

fn solve(lines: Vec<String>) -> (i32, i64) {
    let regex = Regex::new(r"Player \d starting position: (?P<pos>\d+)").unwrap();
    let pos1 = regex.captures(&lines[0]).unwrap()["pos"]
        .parse::<i32>()
        .unwrap();
    let pos2 = regex.captures(&lines[1]).unwrap()["pos"]
        .parse::<i32>()
        .unwrap();
    let states = [
        State {
            position: pos1,
            score: 0,
            rolls_left: 3,
        },
        State {
            position: pos2,
            score: 0,
            rolls_left: 0,
        },
    ];

    let part1 = play_part1(&states);

    let mut dp: HashMap<[State; 2], [i64; 2]> = HashMap::new();
    let result = play_part2(&states, &mut dp);
    let part2 = cmp::max(result[0], result[1]);

    (part1, part2)
}

fn play_part1(states: &[State; 2]) -> i32 {
    let mut states = states.clone();
    let mut dice_rolls = 0;
    let mut dice = 1;

    while states[0].score < 1000 && states[1].score < 1000 {
        let i = (states[0].rolls_left == 0) as usize;
        for _i in 0..3 {
            states[i].position += dice;
            dice += 1;
            dice_rolls += 1;
            if dice > 100 {
                dice = 1;
            }
        }
        while states[i].position > 10 {
            states[i].position -= 10;
        }
        states[i].score += states[i].position;
        states[i].rolls_left = 0;
        states[1 - i].rolls_left = 1;
    }

    cmp::min(states[0].score, states[1].score) * dice_rolls
}

fn play_part2(states: &[State; 2], dp: &mut HashMap<[State; 2], [i64; 2]>) -> [i64; 2] {
    if dp.contains_key(states) {
        return *dp.get(states).unwrap();
    }

    let mut result = [0, 0];
    let i = (states[0].rolls_left == 0) as usize;

    if states[1 - i].score >= 21 {
        result[i] = 1;
        return result;
    }

    for roll in 1..=3 {
        let mut next_states = states.clone();
        next_states[i].rolls_left -= 1;
        next_states[i].position += roll;
        while next_states[i].position > 10 {
            next_states[i].position -= 10;
        }
        if next_states[i].rolls_left == 0 {
            next_states[i].score += next_states[i].position;
            next_states[1 - i].rolls_left = 3;
        }
        let sub_result = play_part2(&next_states, dp);
        result[0] += sub_result[0];
        result[1] += sub_result[1];
    }

    dp.insert(states.clone(), result);
    result
}

#[derive(PartialEq, Eq, Hash, Clone, Debug)]
struct State {
    position: i32,
    rolls_left: i32,
    score: i32,
}
