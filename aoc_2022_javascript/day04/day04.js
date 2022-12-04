main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input.txt", { encoding: "utf-8" })
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
    let elfs = lines[i].split(",");
    elfs[0] = elfs[0].split("-").map(x => parseInt(x));
    elfs[1] = elfs[1].split("-").map(x => parseInt(x));

    for (let a = 0; a < 2; a++) {
      let b = Math.abs(a - 1);
      // a is within b
      if (elfs[a][0] >= elfs[b][0] && elfs[a][1] <= elfs[b][1]) {
        part1 += 1;
        break;
      }
    }
    for (let a = 0; a < 2; a++) {
      let b = Math.abs(a - 1);
      // a and b overlap
      if ((elfs[a][0] >= elfs[b][0] && elfs[a][0] <= elfs[b][1]) ||
          (elfs[a][1] >= elfs[b][0] && elfs[a][1] <= elfs[b][1])) {
        part2 += 1;
        break;
      }
    }
  }
  
  return [part1, part2];
}
