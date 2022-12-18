main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day03.txt", { encoding: "utf-8" })
    .split("\n")
    .map(line => line.trim());
  let start = Date.now();
  solution = solve(lines);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(lines) {
  let part1 = 0;
  for (let i = 0; i < lines.length; i++) {
    let middle = lines[i].length / 2;
    let items = find_common([lines[i].slice(0, middle), lines[i].slice(middle)]);
    part1 += get_score(items);
  }

  let part2 = 0;
  for (let i = 0; i < lines.length - 2; i+=3) {
    let items = find_common([lines[i], lines[i + 1], lines[i + 2]])
    part2 += get_score(items);
  }
  
  return [part1, part2];
}

function find_common(buckets) {
  let items = new Set();
  for (let i = 0; i < buckets[0].length; i++) {
    let item = buckets[0][i];
    for (let a = 1; a < buckets.length; a++) {
      if (buckets[a].includes(item)) {
        items.add(item);
      }
    }
  }
  return items;
}

function get_score(items) {
  // Lowercase item types a through z have priorities 1 through 26.
  // Uppercase item types A through Z have priorities 27 through 52.
  let ret = 0;
  for (let value of items) {
    let ascii = value.charCodeAt(0);
    if (ascii >= 97) { // lower case
      ret += ascii - 97 + 1;
    } else { // upper case
      ret += ascii - 65 + 27;
    }
  }
  return ret;
}