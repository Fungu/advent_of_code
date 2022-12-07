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
  let currentDir = ["root"];
  let dirSizes = new Map();
  
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith("$ cd ")) {
      let dir = lines[i].slice("$ cd ".length)
      if (dir == "/") {
        currentDir = ["root"];
      } else if (dir == "..") {
        currentDir.pop();
      } else {
        currentDir.push(dir);
      }
    } else if (lines[i].startsWith("$ ls")) {
    } else if (!lines[i].startsWith("dir")) {
      let fileSize = parseInt(lines[i].split(" ")[0]);
      for (let k = 1; k <= currentDir.length; k++) {
        let path = currentDir.slice(0, k).join("/");
        if (!dirSizes.has(path)) {
          dirSizes.set(path, 0);
        }
        dirSizes.set(path, dirSizes.get(path) + fileSize);
      }
    }
  }
  
  let part1 = 0;
  dirSizes.forEach(value => {
    if (value <= 100000) {
      part1 += value;
    }
  });

  let diskSize = 70000000;
  let requiredSpace = 30000000;
  let minSizeToDelete = requiredSpace - (diskSize - dirSizes.get("root"));
  let part2 = Number.MAX_SAFE_INTEGER;
  dirSizes.forEach(value => {
    if (value >= minSizeToDelete) {
      part2 = Math.min(part2, value);
    }
  });
  
  return [part1, part2];
}