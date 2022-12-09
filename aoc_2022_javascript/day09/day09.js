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
  let part1 = slither(lines, 2);
  let part2 = slither(lines, 10);
  
  return [part1, part2];
}

function slither(lines, length) {
  let snek = [];
  for (let i = 0; i < length; i++) {
    snek.push([0, 0]);
  }
  let tailVisited = new Set();
  tailVisited.add(0 + "," + 0);
  for (line of lines) {
    [direction, steps] = line.split(" ");
    steps = parseInt(steps);
    for (let s = 0; s < steps; s++) {
      snek[0][0] += directions[direction][0];
      snek[0][1] += directions[direction][1];
      for (let i = 0; i < length - 1; i++) {
        diff = [
          snek[i][0] - snek[i + 1][0], 
          snek[i][1] - snek[i + 1][1]];
        if (Math.abs(diff[0]) >= 2 || Math.abs(diff[1]) >= 2) {
          for (let xy = 0; xy < 2; xy++) {
            if (diff[xy] != 0) {
              snek[i + 1][xy] += (diff[xy] / Math.abs(diff[xy]));
            }
          }
        }
      }
      tailVisited.add(snek[length - 1][0] + "," + snek[length - 1][1]);
    }
  }
  return tailVisited.size;
}