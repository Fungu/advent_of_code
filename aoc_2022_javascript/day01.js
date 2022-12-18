main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day01.txt", { encoding: "utf-8" })
    .split("\n");
  let start = Date.now();
  solution = solve(lines);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(lines) {
  let elves = [];
  let current = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() != "") {
      current += parseInt(lines[i]);
    } else {
      elves.push(current);
      current = 0;
    }
  }
  elves.push(current);
  elves.sort(function(a, b) { return a - b; }).reverse();
  
  part1 = Math.max(...elves);
  part2 = elves[0] + elves[1] + elves[2];

  return [part1, part2];
}
