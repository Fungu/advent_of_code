main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day23.txt", { encoding: "utf-8" })
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
  let elves = [];
  let directions = ["N", "S", "W", "E"];
  for (let y = 0; y < lines.length; y++) {
    for (let x = 0; x < lines[y].length; x++) {
      if (lines[y][x] == "#") {
        elves.push([x, y]);
      }
    }
  }
  let part1;
  let part2;
  for (let round = 0;; round++) {
    let propositions = new Map();
    for (let elf of elves) {
      let hasNeighbor = false;
      for (let otherElf of elves) {
        if (elf != otherElf && Math.abs(elf[0] - otherElf[0]) <= 1 && Math.abs(elf[1] - otherElf[1]) <= 1) {
          hasNeighbor = true;
          break;
        }
      }
      if (hasNeighbor) {
        for (let d of directions) {
          if (d == "N") {
            if (!has(elves, elf[0] - 1, elf[1] - 1) && !has(elves, elf[0], elf[1] - 1) && !has(elves, elf[0] + 1, elf[1] - 1)) {
              propositions.set(elf, [elf[0], elf[1] - 1]);
              break;
            }
          } else if (d == "S") {
            if (!has(elves, elf[0] - 1, elf[1] + 1) && !has(elves, elf[0], elf[1] + 1) && !has(elves, elf[0] + 1, elf[1] + 1)) {
              propositions.set(elf, [elf[0], elf[1] + 1]);
              break;
            }
          } else if (d == "W") {
            if (!has(elves, elf[0] - 1, elf[1] - 1) && !has(elves, elf[0] - 1, elf[1]) && !has(elves, elf[0] - 1, elf[1] + 1)) {
              propositions.set(elf, [elf[0] - 1, elf[1]]);
              break;
            }
          } else if (d == "E") {
            if (!has(elves, elf[0] + 1, elf[1] - 1) && !has(elves, elf[0] + 1, elf[1]) && !has(elves, elf[0] + 1, elf[1] + 1)) {
              propositions.set(elf, [elf[0] + 1, elf[1]]);
              break;
            }
          }
        }
      }
    }
    for (let [key, value] of propositions) {
      let hasConflict = false;
      for (let [innerKey, innerValue] of propositions) {
        if (key != innerKey && value[0] == innerValue[0]  && value[1] == innerValue[1]) {
          hasConflict = true;
          break;
        }
      }
      if (!hasConflict) {
        key[0] = value[0];
        key[1] = value[1];
      }
    }
    if (round == 10) {
      let minX = Math.min(...elves.map(a => a[0]));
      let maxX = Math.max(...elves.map(a => a[0]));
      let minY = Math.min(...elves.map(a => a[1]));
      let maxY = Math.max(...elves.map(a => a[1]));
      part1 = (maxX - minX + 1) * (maxY - minY + 1) - elves.length;
    }
    if (propositions.size == 0) {
      part2 = round + 1;
      break;
    }
    let d = directions.shift();
    directions.push(d);
  }

  return [part1, part2];
}

function has(elves, x, y) {
  for (let elf of elves) {
    if (elf[0] == x && elf[1] == y) {
      return true;
    }
  }
  return false;
}