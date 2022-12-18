main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day12.txt", { encoding: "utf-8" })
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
  ];
  let part1 = Number.MAX_SAFE_INTEGER;
  let part2 = Number.MAX_SAFE_INTEGER;

  let openSet = []
  let closedSet = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].indexOf("E") != -1) {
      openSet.push({
        x: lines[i].indexOf("E"), 
        y: i,
        steps: 0
      });
    }
  }

  while (openSet.length > 0) {
    let current = openSet.shift();
    closedSet.push(current);
    let rawChar = lines[current.y][current.x];
    currentChar = convertChar(rawChar);
    if (currentChar == "a") {
      part2 = Math.min(part2, current.steps);
    }
    if (rawChar == "S") {
      part1 = current.steps;
      break;
    }
    for (let dir of directions) {
      let neighbor = [current.x + dir[0], current.y + dir[1]];
      if (neighbor[0] >= 0 && neighbor[0] < lines[0].length && neighbor[1] >= 0 && neighbor[1] < lines.length) {
        let neighborChar = convertChar(lines[neighbor[1]][neighbor[0]]);
        if (!includesFixed(openSet, neighbor) && !includesFixed(closedSet, neighbor) && currentChar.charCodeAt(0) - neighborChar.charCodeAt(0) <= 1) {
          openSet.push({
            x: neighbor[0],
            y: neighbor[1],
            steps: current.steps + 1
          });
        }
      }
    }
  }
  return [part1, part2];
}

function convertChar(c) {
  if (c == "S") {
    return "a";
  }
  if (c == "E") {
    return "z";
  }
  return c;
}

function includesFixed(array, item) {
  return array.filter(a => a.x == item[0] && a.y == item[1]) != 0;
}