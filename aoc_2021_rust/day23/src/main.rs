use std::{
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

fn solve(lines: Vec<String>) -> (i32, i32) {
    let part1 = search(lines.clone(), false);

    let mut lines = lines.clone();
    lines.insert(3, "  #D#C#B#A#".to_string());
    lines.insert(4, "  #D#B#A#C#".to_string());
    let part2 = search(lines, true);

    (part1, part2)
}

fn search(lines: Vec<String>, extended: bool) -> i32 {
    let mut positions: [(char, usize, usize); 16] = [(' ', 0, 0); 16];
    let mut i = 0;
    for y in 0..lines.len() {
        for x in 0..lines[y].len() {
            if lines[y].chars().nth(x).unwrap().is_ascii_uppercase() {
                positions[i] = (lines[y].chars().nth(x).unwrap(), x, y);
                i += 1;
            }
        }
    }
    let type_dest: HashMap<char, usize> = HashMap::from([('A', 3), ('B', 5), ('C', 7), ('D', 9)]);
    let costs: HashMap<char, i32> = HashMap::from([('A', 1), ('B', 10), ('C', 100), ('D', 1000)]);
    let input_state = State {
        positions,
        score: 0,
    };
    let mut dp = HashMap::new();
    explore(input_state, extended, &mut dp, &type_dest, &costs)
}
fn explore(
    state: State,
    extended: bool,
    dp: &mut HashMap<State, i32>,
    type_dest: &HashMap<char, usize>,
    costs: &HashMap<char, i32>,
) -> i32 {
    let len = if !extended { 8 } else { 16 };
    const HIGHWAY: usize = 1;
    const OUTER: usize = 2;
    const ENTRANCES: [usize; 4] = [3, 5, 7, 9];

    if dp.contains_key(&state) {
        return *dp.get(&state).unwrap();
    }

    if state
        .positions
        .iter()
        .all(|(c, x, y)| *y != HIGHWAY && (*c == ' ' || type_dest.get(c).unwrap() == x))
    {
        return state.score;
    }

    let mut sub_results = Vec::new();
    for i in 0..len {
        let (c, x, y) = state.positions[i];
        // Already in the right spot
        if type_dest.get(&c).unwrap() == &x
            && y >= OUTER
            && state
                .positions
                .iter()
                .all(|(cc, xx, _yy)| *cc == c || *xx != x)
        {
            continue;
        }

        let destinations = get_possible_destinations(state.positions, i, extended);
        for dest in destinations {
            if dest.1 == HIGHWAY {
                // Don't make multiple stops on the highway
                if y == HIGHWAY {
                    continue;
                }
                // Don't stop in front of entrances
                if ENTRANCES.contains(&dest.0) {
                    continue;
                }
            } else {
                // Only move to your lane
                if type_dest.get(&c).unwrap() != &dest.0 {
                    continue;
                }
                // Wait for other amphipods to evacuate
                let mut valid = true;
                let depth = if extended { 5 } else { 3 };
                for a in OUTER..=depth {
                    let inner_c = get_char_at(state.positions, (dest.0, a));
                    if inner_c.is_some() && inner_c.unwrap() != c {
                        valid = false;
                        break;
                    }
                }
                if !valid {
                    continue;
                }
                // Always fill to the back of the lane
                for a in (OUTER..=depth).rev() {
                    let inner_c = get_char_at(state.positions, (dest.0, a));
                    if inner_c.is_none() {
                        if dest.1 != a {
                            valid = false;
                        }
                        break;
                    }
                }
                if !valid {
                    continue;
                }
            }

            let mut new_positions = state.positions.clone();
            new_positions[i] = (c, dest.0, dest.1);
            let mut dist = i32::abs(x as i32 - dest.0 as i32);
            if dist == 0 {
                dist += i32::abs(y as i32 - dest.1 as i32);
            } else {
                dist +=
                    i32::abs(y as i32 - HIGHWAY as i32) + i32::abs(dest.1 as i32 - HIGHWAY as i32);
            }
            let score = state.score + dist * costs[&c];
            let new_state = State {
                positions: new_positions,
                score,
            };
            let sub_result = explore(new_state, extended, dp, type_dest, costs);
            sub_results.push(sub_result);
        }
    }
    let ret = if sub_results.is_empty() {
        i32::MAX
    } else {
        *sub_results.iter().min().unwrap()
    };
    dp.insert(state, ret);
    ret
}

fn get_possible_destinations(
    positions: [(char, usize, usize); 16],
    index: usize,
    extended: bool,
) -> Vec<(usize, usize)> {
    let depth = if !extended { 3 } else { 5 };
    let mut ret: Vec<(usize, usize)> = Vec::new();
    let mut open_set: Vec<(usize, usize)> = Vec::new();
    open_set.push((positions[index].1, positions[index].2));
    while let Some(pos) = open_set.pop() {
        if pos != (positions[index].1, positions[index].2) {
            ret.push(pos);
        }
        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)] {
            let x = (pos.0 as i32 + dir.0) as usize;
            let y = (pos.1 as i32 + dir.1) as usize;
            let neighbor = (x, y);
            if x >= 1
                && x <= 11
                && y >= 1
                && (y <= 1 || (y <= depth && (x == 3 || x == 5 || x == 7 || x == 9)))
            {
                if get_char_at(positions, neighbor).is_none()
                    && !ret.contains(&neighbor)
                    && !open_set.contains(&neighbor)
                {
                    open_set.push(neighbor);
                }
            }
        }
    }
    ret
}

fn get_char_at(positions: [(char, usize, usize); 16], pos: (usize, usize)) -> Option<char> {
    for (c, x, y) in positions {
        if x == pos.0 && y == pos.1 {
            return Some(c);
        }
    }
    None
}

#[derive(Clone, Eq, PartialEq, Hash, Debug)]
struct State {
    positions: [(char, usize, usize); 16],
    score: i32,
}
