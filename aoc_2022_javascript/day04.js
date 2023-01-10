main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day04.txt", { encoding: "utf-8" })
    .trim()
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
  let part1 = 0;
  let part2 = 0;

  for (let i = 0; i < lines.length; i++) {
    let elves = lines[i].split(",");
    elves[0] = elves[0].split("-").map(x => parseInt(x));
    elves[1] = elves[1].split("-").map(x => parseInt(x));

    for (let a = 0; a < 2; a++) {
      let b = Math.abs(a - 1);
      // a is within b
      if (elves[a][0] >= elves[b][0] && elves[a][1] <= elves[b][1]) {
        part1 += 1;
        break;
      }
    }
    for (let a = 0; a < 2; a++) {
      let b = Math.abs(a - 1);
      // a and b overlap
      if ((elves[a][0] >= elves[b][0] && elves[a][0] <= elves[b][1]) ||
          (elves[a][1] >= elves[b][0] && elves[a][1] <= elves[b][1])) {
        part2 += 1;
        break;
      }
    }
  }
  
  return [part1, part2];
}
