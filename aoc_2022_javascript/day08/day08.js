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
  let directions = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1]
  ]

  let visibleSet = new Set();
  let part2 = 0;
  for (let y = 0; y < lines.length; y++) {
    for (let x = 0; x < lines[0].length; x++) {
      let scenic = 1;
      for ([dirX, dirY] of directions) {
        for (let i = 1;; i++) {
          let xx = x + dirX * i;
          let yy = y + dirY * i;
          if (xx < 0 || xx >= lines[0].length || yy < 0 || yy >= lines.length) {
            visibleSet.add(y * lines.length + x);
            scenic *= (i - 1);
            break;
          }
          if (lines[yy][xx] >= lines[y][x]) {
            scenic *= i;
            break;
          }
        }
      }
      part2 = Math.max(part2, scenic);
    }
  }
  let part1 = visibleSet.size;
  
  return [part1, part2];
}