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

fn solve(lines: Vec<String>) -> (usize, usize) {
    let binary = convert_to_binary_from_hex(&lines[0]);
    let mut index = 0;

    let temp = parse_packet(&binary, &mut index);
    let part1 = temp.0;
    let part2 = temp.1;

    (part1, part2)
}

// Returns (Sum of all version numbers, Evaluated packet value)
fn parse_packet(binary: &String, index: &mut usize) -> (usize, usize) {
    let mut ret = (0, 0);

    // the first three bits encode the packet version,
    let packet_version = to_decimal(&pop(&binary, index, 3));
    ret.0 += packet_version;

    // the next three bits encode the packet type ID.
    let packet_type_id = to_decimal(&pop(&binary, index, 3));

    let mut sub_values: Vec<usize> = Vec::new();
    // An operator packet (any packet with a type ID other than 4) contains one or more packets.
    if packet_type_id != 4 {
        // An operator packet can use one of two modes indicated by the bit immediately after the packet header;
        // this is called the length type ID:
        let length_type_id = pop(&binary, index, 1);
        // If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet.
        if length_type_id == "0" {
            let total_length_of_sub_packet = to_decimal(&pop(&binary, index, 15));
            let end_index = *index + total_length_of_sub_packet;
            while *index < end_index {
                let temp = parse_packet(binary, index);
                ret.0 += temp.0;
                sub_values.push(temp.1);
            }
        }
        // If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet.
        else if length_type_id == "1" {
            let number_of_sub_packets = to_decimal(&pop(&binary, index, 11));
            for _i in 0..number_of_sub_packets {
                let temp = parse_packet(binary, index);
                ret.0 += temp.0;
                sub_values.push(temp.1);
            }
        }
    }

    ret.1 = match packet_type_id {
        // Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        0 => sub_values.iter().sum::<usize>(),
        // Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        1 => sub_values.iter().product::<usize>(),
        // Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        2 => *sub_values.iter().min().unwrap(),
        // Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        3 => *sub_values.iter().max().unwrap(),
        // Packets with type ID 4 represent a literal value
        4 => parse_literal(&binary, index),
        // Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        5 => {
            if sub_values.get(0) > sub_values.get(1) {
                1
            } else {
                0
            }
        }
        // Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        6 => {
            if sub_values.get(0) < sub_values.get(1) {
                1
            } else {
                0
            }
        }
        // Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        7 => {
            if sub_values.get(0) == sub_values.get(1) {
                1
            } else {
                0
            }
        }
        _ => panic!(),
    };
    ret
}

fn parse_literal(binary: &String, index: &mut usize) -> usize {
    // Literal value packets encode a single binary number.
    // To do this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then it is broken into groups of four bits.
    // Each group is prefixed by a 1 bit except the last group, which is prefixed by a 0 bit. These groups of five bits immediately follow the packet header.
    let mut literal = "".to_string();
    loop {
        let prefix = pop(&binary, index, 1);
        let value = pop(&binary, index, 4);
        literal += &value;
        if prefix == "0" {
            break;
        }
    }
    to_decimal(&literal)
}

fn pop(s: &String, index: &mut usize, amount: usize) -> String {
    let ret = &s[*index..*index + amount];
    *index += amount;
    ret.to_string()
}

fn to_decimal(binary: &str) -> usize {
    isize::from_str_radix(binary, 2).unwrap() as usize
}

fn convert_to_binary_from_hex(hex: &str) -> String {
    hex.chars().map(to_binary).collect()
}

fn to_binary(c: char) -> &'static str {
    match c {
        '0' => "0000",
        '1' => "0001",
        '2' => "0010",
        '3' => "0011",
        '4' => "0100",
        '5' => "0101",
        '6' => "0110",
        '7' => "0111",
        '8' => "1000",
        '9' => "1001",
        'A' => "1010",
        'B' => "1011",
        'C' => "1100",
        'D' => "1101",
        'E' => "1110",
        'F' => "1111",
        _ => "",
    }
}
