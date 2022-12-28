main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day24.txt", { encoding: "utf-8" })
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
  let upList = [];
  let downList = [];
  let leftList = [];
  let rightList = [];
  for (let y = 1; y < lines.length - 1; y++) {
    leftList.push(new Set());
    rightList.push(new Set());
  }
  for (let x = 1; x < lines[0].length - 1; x++) {
    upList.push(new Set());
    downList.push(new Set());
  }
  for (let y = 1; y < lines.length - 1; y++) {
    for (let x = 1; x < lines[0].length - 1; x++) {
      if (lines[y][x] == "^") {
        upList[x - 1].add(y - 1);
      } else if (lines[y][x] == "v") {
        downList[x - 1].add(y - 1);
      } else if (lines[y][x] == "<") {
        leftList[y - 1].add(x - 1);
      } else if (lines[y][x] == ">") {
        rightList[y - 1].add(x - 1);
      }
    }
  }
  let width = lines[0].length - 2;
  let height = lines.length - 2;
  let startPos = {x: 0, y: -1};
  let targetPos = {x: width - 1, y: height};

  let directions = [
    {x:1, y:0},
    {x:-1, y:0},
    {x:0, y:1},
    {x:0, y:-1},
    {x:0, y:0}
  ];
  let part1 = Number.MAX_SAFE_INTEGER;
  let part2 = 0;
  let openSet = [[startPos, 0, 1]];
  let closedSet = new Set();
  while (openSet.length > 0) {
    let [pos, minute, stage] = openSet.shift();
    
    for (let dir of directions) {
      let neighbor = {x: pos.x + dir.x, y: pos.y + dir.y};
      if (closedSet.has(JSON.stringify([neighbor, minute + 1, stage]))) {
        continue;
      }
      if (neighbor.x == targetPos.x && neighbor.y == targetPos.y) {
        part1 = Math.min(part1, minute);
        closedSet.add(JSON.stringify([neighbor, minute + 1, stage]));
        if (stage == 1) {
          openSet.push([neighbor, minute + 1, 2]);
        } else if (stage == 3) {
          part2 = minute;
          openSet = [];
          break;
        } else {
          openSet.push([neighbor, minute + 1, stage]);
        }
      }
      if (neighbor.x == startPos.x && neighbor.y == startPos.y) {
        closedSet.add(JSON.stringify([neighbor, minute + 1, stage]));
        if (stage == 2) {
          openSet.push([neighbor, minute + 1, 3]);
        } else {
          openSet.push([neighbor, minute + 1, stage]);
        }
      }
      if (neighbor.x < 0 || neighbor.y < 0 || neighbor.x >= width || neighbor.y >= height) {
        continue;
      }
      if (!upList[neighbor.x].has((neighbor.y + minute) % height) && 
          !downList[neighbor.x].has((neighbor.y - minute + height * minute) % height) && 
          !leftList[neighbor.y].has((neighbor.x + minute) % width) && 
          !rightList[neighbor.y].has((neighbor.x - minute + width * minute) % width)) {
        closedSet.add(JSON.stringify([neighbor, minute + 1, stage]));
        openSet.push([neighbor, minute + 1, stage]);
      }
    }
  }
  
  return [part1, part2];
}

function print(upList, downList, leftList, rightList, width, height, minute) {
  for (let y = 0; y < height; y++) {
    let row = "";
    for (let x = 0; x < width; x++) {
      let blizzards = [];
      if (upList[x].has((y + minute) % height)) {
        blizzards.push("^");
      }
      if (downList[x].has((y - minute + height * minute) % height)) {
        blizzards.push("v");
      }
      if (leftList[y].has((x + minute) % width)) {
        blizzards.push("<");
      }
      if (rightList[y].has((x - minute + width * minute) % width)) {
        blizzards.push(">");
      } 
      if (blizzards.length == 1) {
        row += blizzards[0];
      } else if (blizzards.length == 0) {
        row += ".";
      } else {
        row += blizzards.length;
      }
    }
    console.log(row);
  }
}