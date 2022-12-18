let shapes = [
  [[0, 0], [1, 0], [2, 0], [3, 0]],
  [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],
  [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],
  [[0, 0], [0, 1], [0, 2], [0, 3]],
  [[0, 0], [1, 0], [0, 1], [1, 1]]
];
let shapeWidths = [4, 3, 3, 1, 2];
main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day17.txt", { encoding: "utf-8" })
    .trim()
    .split("");
  let start = Date.now();
  solution = solve(input);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(jets) {
  let currentShape = 0;
  let currentJet = 0;
  let grid = [createRow("#")];
  let part1 = 0;
  let part2 = 0;
  let gridHistory = [];
  let scoreHistory = [];
  for (let i = 0; part1 == 0 || part2 == 0; i++) {
    let x = 2;
    let y = grid.length + 3;
    while (true) {
      let dirX;
      if (jets[currentJet] == "<") {
        dirX = -1;
      } else {
        dirX = 1;
      }
      currentJet++;
      currentJet %= jets.length;
      if (!isColliding(grid, currentShape, x + dirX, y)) {
        x += dirX;
      }
      if (!isColliding(grid, currentShape, x, y - 1)) {
        y--;
      } else {
        for (let [xx, yy] of shapes[currentShape]) {
          while (y + yy >= grid.length) {
            grid.push(createRow("."));
          }
          grid[y + yy][x + xx] = "#";
        }
        let currentRow = grid[grid.length - 1].join("") + " " + currentShape + " " + currentJet;
        let seenIndex = gridHistory.indexOf(currentRow);
        if (seenIndex >= 0) {
          let indexDiff = i - seenIndex;
          let rocksLeft = 1000000000000 - i;
          if (rocksLeft % indexDiff == 0) {
            let scoreDiff = grid.length - 1 - scoreHistory[seenIndex];
            part2 = grid.length - 2 + (rocksLeft / indexDiff) * scoreDiff;
            break;
          }
        }
        gridHistory.push(currentRow);
        scoreHistory.push(grid.length - 1);
        break;
      }
    }
    if (i == 2021) {
      part1 = grid.length - 1;
    }
    
    currentShape++;
    currentShape %= shapes.length;
  }
  return [part1, part2];
}

function isColliding(grid, currentShape, x, y) {
  if (x < 0 || x + shapeWidths[currentShape] > 7) {
    return true;
  }
  if (y < grid.length) {
    for (let [xx, yy] of shapes[currentShape]) {
      if (y + yy < grid.length && grid[y + yy][x + xx] == "#") {
        return true;
      }
    }
  }
  return false;
}

function createRow(c) {
  return [c, c, c, c, c, c, c];
}