let directions = {
  "R": [1, 0],
  "L": [-1, 0],
  "U": [0, 1],
  "D": [0, -1],
};
main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input.txt", { encoding: "utf-8" })
    .trim()
    .split("\r\n");
  let start = Date.now();
  solution = solve(lines);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(lines) {
  let instructionTimes = {
    "addx": 2,
    "noop": 1,
  };
  let width = 40;
  let height = 6;
  let interestingCycles = [20, 60, 100, 140, 180, 220];
  let maxCycle = width * height;
  let instructionPointer = 0;
  let currentInstruction = "";
  let currentValue = 0;
  let cooldown = 0;
  let register = 1;
  let part1 = 0;
  let part2 = "";
  let crtLine = "";
  let scanPos = 0;
  for (let cycle = 1; cycle <= maxCycle; cycle++) {
    if (interestingCycles.includes(cycle)) {
      part1 += cycle * register;
    }
    if (Math.abs(scanPos - register) <= 1) {
      crtLine += "#";
    } else {
      crtLine += " ";
    }
    scanPos++;
    if (scanPos == width) {
      part2 += "\n" + crtLine;
      crtLine = "";
      scanPos = 0;
    }
    if (instructionPointer >= lines.length) {
      continue;
    }
    if (currentInstruction == "") {
      let {instruction, value} = lines[instructionPointer].match(/(?<instruction>[a-z]+) ?(?<value>-?[0-9]+)?/).groups;
      cooldown = instructionTimes[instruction];
      currentInstruction = instruction;
      currentValue = parseInt(value);
    }
    cooldown--;
    if (cooldown == 0) {
      switch (currentInstruction) {
        case "addx":
          register += currentValue;
          break;
        case "noop":
          break;
        default:
          break;
      }
      currentInstruction = "";
      instructionPointer++;
    }
  }
  return [part1, part2];
}