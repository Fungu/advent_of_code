main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day18.txt", { encoding: "utf-8" })
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
  let points = [];
  for (let line of lines) {
    points.push(line.split(",").map(x => parseInt(x)));
  }
  let maxDistance = 0;
  for (let point of points) {
    maxDistance = Math.max(maxDistance, Math.abs(point[0]));
    maxDistance = Math.max(maxDistance, Math.abs(point[1]));
    maxDistance = Math.max(maxDistance, Math.abs(point[2]));
  }
  let directions = [
    [1, 0, 0],
    [-1, 0, 0],
    [0, 1, 0],
    [0, -1, 0],
    [0, 0, 1],
    [0, 0, -1],
  ];
  let trappedCells = [];
  let part1 = 0;
  let part2 = 0;
  for (let point of points) {
    for (let dir of directions) {
      let cellFace = [point[0] + dir[0], point[1] + dir[1], point[2] + dir[2]];
      if (!contains(points, cellFace)) {
        part1++;
        let trapped = true;
        let openSet = [cellFace];
        let closedSet = [];
        while (openSet.length > 0) {
          currentCell = openSet.pop();
          closedSet.push(currentCell);
          if (contains(trappedCells, currentCell)) {
            break;
          }
          if (Math.abs(currentCell[0]) > maxDistance || Math.abs(currentCell[1]) > maxDistance || Math.abs(currentCell[2]) > maxDistance) {
            trapped = false;
            break;
          }
          for (let dirInner of directions) {
            let neighbor = [currentCell[0] + dirInner[0], currentCell[1] + dirInner[1], currentCell[2] + dirInner[2]];
            if (!contains(openSet, neighbor) && !contains(closedSet, neighbor) && !contains(points, neighbor)) {
              openSet.push(neighbor);
            }
          }
        }
        if (trapped) {
          for (let closed of closedSet) {
            if (!contains(trappedCells, closed)) {
              trappedCells.push(closed);
            }
          }
        } else {
          part2++;
        }
      }
    }
  }
  
  return [part1, part2];
}

function contains(array, element) {
  return array.filter(x => arrayEquals(x, element)).length > 0;
}

function arrayEquals(a, b) {
  return a[0] == b[0] && a[1] == b[1] && a[2] == b[2];
}