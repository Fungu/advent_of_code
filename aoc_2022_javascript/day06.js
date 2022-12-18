main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day06.txt", { encoding: "utf-8" })
    .trim()
    .split("");
  let start = Date.now();
  solution = solve(lines);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(charArray) {
  let part1 = findMarkerPos(charArray, 4);
  let part2 = findMarkerPos(charArray, 14);
  
  return [part1, part2];
}

function findMarkerPos(charArray, size) {
  for (let i = size; i < charArray.length; i++) {
    let s = new Set(charArray.slice(i - size, i));
    if (s.size == size) {
      return i;
    }
  }
}