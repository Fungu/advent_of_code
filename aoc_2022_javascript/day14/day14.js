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
  console.log(`Part 1: ${solution[0]}`);  // 873
  console.log(`Part 2: ${solution[1]}`);  // 24813
}

function solve(lines) {
  let source = {
    x: 500,
    y: 0,
  }
  
  let walls = lines.map(
    line => line.split(" -> ").map(
      pointsString => pointsString.split(",").map(
        pointString => parseInt(pointString))));
  
  let floorY = 2 + walls.reduce(
    (totalOuter, points) => Math.max(totalOuter, points.reduce(
      (totalInner, point) => Math.max(totalInner, point[1]),
      0)),
    0);
  
  let minX = source.x - floorY - 1;
  let maxX = source.x + floorY + 1;
  console.assert(minX >= 0);
  let grid = [];
  for (let y = 0; y <= floorY; y++) {
    let g = []
    for (let x = 0; x <= maxX; x++) {
      g.push(".");
    }
    grid.push(g);
  }
  for (let points of walls) {
    for (let i = 0; i < points.length - 1; i++) {
      let s = points[i];
      let e = points[i + 1];
      while (!arrayEqual(s, e)) {
        grid[s[1]][s[0]] = "#";
        for (let j = 0; j < 2; j++) {
          let d = e[j] - s[j];
          if (d != 0) {
            s[j] += d / Math.abs(d);
          }
        }
      }
      grid[s[1]][s[0]] = "#";
    }
  }
  for (let x = 0; x < grid[0].length; x++) {
    grid[floorY][x] = "F";
  }
  let part1 = 0;
  let part2 = 0;
  let firstPartDone = false;
  let keepGoing = true;
  while (keepGoing) {
    let sand = {
      x: source.x,
      y: source.y,
    }
    while (true) {
      if (sand.x < 0 || sand.x >= grid[0].length) {
        console.log(sand);
        keepGoing = false;
        break;
      }
      if (grid[sand.y + 1][sand.x] == ".") {
        sand.y++;
      } else if (grid[sand.y + 1][sand.x - 1] == ".") {
        sand.y++;
        sand.x--;
      } else if (grid[sand.y + 1][sand.x + 1] == ".") {
        sand.y++;
        sand.x++;
      } else {
        grid[sand.y][sand.x] = "O";
        if (sand.y + 1 == floorY) {
          firstPartDone = true;
        }
        if (!firstPartDone) {
          part1++;
        }
        part2++;
        if (sand.x == source.x && sand.y == source.y) {
          keepGoing = false;
        }
        break;
      }
    }
  }
  
  return [part1, part2];
}

function arrayEqual(a, b) {
  return a[0] == b[0] && a[1] == b[1];
}