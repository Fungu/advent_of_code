main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day02.txt", { encoding: "utf-8" })
    .split("\n")
    .map(line => line.trim());
  let start = Date.now();
  solution = solve(lines);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(lines) {
  // A for Rock, B for Paper, and C for Scissors
  let counters = { "A": "C", "B": "A", "C": "B" };
  let countered = { "A": "B", "B": "C", "C": "A" };
  let score_map = { "A": 1, "B": 2, "C": 3 };
  let part_1_mapping = { "X": "A", "Y": "B", "Z": "C" };
  
  let part1 = 0;
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i].split(" ");
    let elf = line[0];
    let you = part_1_mapping[line[1]];
    part1 += score_map[you];
    if (elf == you) {
      part1 += 3;
    } else if (counters[you] == elf) {
      part1 += 6;
    }
  }

  let part2 = 0;
  // X means lose, Y means draw, and Z means win
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i].split(" ");
    let elf = line[0];
    let outcome = line[1];
    if (outcome == "X") {
      part2 += score_map[counters[elf]];
    } else if (outcome == "Y") {
      part2 += score_map[elf] + 3;
    } else {
      part2 += score_map[countered[elf]] + 6;
    }
  }
  
  return [part1, part2];
}
