main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day25.txt", { encoding: "utf-8" })
    .trim()
    .split("\r\n");
  let start = Date.now();
  solution = solve(input);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(lines) {
  let decimalSum = 0;
  for (let line of lines) {
    decimalSum += decode(line);
  }
  let part1 = encode(decimalSum);
  
  return [part1, "Merry Christmas!"];
}

function decode(snafu) {
  let snafuToDec = new Map([
    ["0", 0],
    ["1", 1],
    ["2", 2],
    ["=", -2],
    ["-", -1]
  ]);
  decimal = 0;
  for (let i = 0; i < snafu.length; i++) {
    decimal *= 5;
    decimal += snafuToDec.get(snafu[i]);
  }
  return decimal;
}

function encode(decimal) {
  let decToSnafu = new Map([
    [0, "0"],
    [1, "1"],
    [2, "2"],
    [3, "="],
    [4, "-"]
  ]);
  let modValue = new Map([
    [0, 0],
    [1, 1],
    [2, 2],
    [3, -2],
    [4, -1]
  ]);
  let snafu = "";
  while (decimal != 0) {
    snafu = decToSnafu.get(decimal % 5) + snafu;
    decimal = (decimal - modValue.get(decimal % 5)) / 5;
  }
  return snafu;
}