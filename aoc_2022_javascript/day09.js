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
    .readFileSync("input/day09.txt", { encoding: "utf-8" })
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
  let length = 10;
  let snek = [];
  for (let i = 0; i < length; i++) {
    snek.push([0, 0]);
  }
  let visited1 = new Set(["0,0"]);
  let visited2 = new Set(["0,0"]);

  for (let line of lines) {
    let [direction, steps] = line.split(" ");
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
      visited1.add(snek[1][0] + "," + snek[1][1]);
      visited2.add(snek[length - 1][0] + "," + snek[length - 1][1]);
    }
  }
  return [visited1.size, visited2.size];
}