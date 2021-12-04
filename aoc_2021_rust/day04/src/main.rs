use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let buf_reader = BufReader::new(File::open("input.txt")?);
    let lines = buf_reader
        .lines()
        .map(|line| line.unwrap())
        .collect::<Vec<String>>();

    let values: Vec<i32> = lines[0]
        .split(",")
        .into_iter()
        .map(|f| f.parse::<i32>().unwrap())
        .collect();
    let boards = parse_boards(&lines[2..]);

    println!("Part 1: {}", play(values.clone(), boards.clone()));
    println!(
        "Part 2: {}",
        find_last_board(values.clone(), boards.clone())
    );

    Ok(())
}

fn parse_boards(lines: &[String]) -> Vec<[[i32; 5]; 5]> {
    let mut boards = Vec::new();
    let chunks = lines.chunks(6);
    for chunk in chunks {
        boards.push(parse_board(&chunk));
    }

    boards
}

fn parse_board(lines: &[String]) -> [[i32; 5]; 5] {
    let mut grid = [[0; 5]; 5];
    for y in 0..5 {
        let line = lines[y].replace("  ", " ");
        let line = line.trim();
        let mut a = line.split(" ");
        for x in 0..5 {
            let b = a.next().unwrap();
            grid[y][x] = b.parse::<i32>().unwrap();
        }
    }
    grid
}

fn play(values: Vec<i32>, boards: Vec<[[i32; 5]; 5]>) -> i32 {
    let mut boards = boards.clone();
    for value in values {
        for i in 0..boards.len() {
            for y in 0..5 {
                for x in 0..5 {
                    if boards[i][y][x] == value {
                        boards[i][y][x] = -1;
                    }
                }
            }
            if has_won(boards[i]) {
                return get_score(boards[i], value);
            }
        }
    }
    -1
}

fn find_last_board(values: Vec<i32>, boards: Vec<[[i32; 5]; 5]>) -> i32 {
    let mut boards = boards.clone();
    let mut last_board: [[i32; 5]; 5] = boards[0];
    let mut last_value: i32 = -1;
    let mut eliminated_indexes: Vec<usize> = Vec::new();
    for value in values {
        for i in 0..boards.len() {
            if eliminated_indexes.contains(&i) {
                continue;
            }
            for y in 0..5 {
                for x in 0..5 {
                    if boards[i][y][x] == value {
                        boards[i][y][x] = -1;
                    }
                }
            }
            if has_won(boards[i]) {
                last_board = boards[i];
                last_value = value;
                eliminated_indexes.push(i);
            }
        }
    }
    get_score(last_board, last_value)
}

fn has_won(board: [[i32; 5]; 5]) -> bool {
    for i in 0..5 {
        if (0..5).all(|x| board[x][i] == -1) {
            return true;
        }
        if (0..5).all(|x| board[i][x] == -1) {
            return true;
        }
    }
    false
}

fn get_score(board: [[i32; 5]; 5], last_number: i32) -> i32 {
    let mut score = 0;
    for y in 0..5 {
        for x in 0..5 {
            if board[y][x] != -1 {
                score += board[y][x];
            }
        }
    }
    score * last_number
}
