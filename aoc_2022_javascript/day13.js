const number = "number";
const object = "object";
main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day13.txt", { encoding: "utf-8" })
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
  let part1 = 0;
  let packets = [[[2]], [[6]]];
  for (let i = 0; i < lines.length; i += 3) {
    let a = JSON.parse(lines[i]);
    let b = JSON.parse(lines[i + 1]);
    packets.push(a);
    packets.push(b);
    if (compare(a, b) == 1) {
      part1 += (i / 3) + 1;
    }
  }
  packets.sort(function(a, b) { return compare(a, b); }).reverse();
  let part2 = (1 + packets.findIndex(x => arrayEqual(x, [[2]]))) * 
              (1 + packets.findIndex(x => arrayEqual(x, [[6]])));
  return [part1, part2];
}

function compare(a, b) {
  ta = typeof a;
  tb = typeof b;
  
  // If both values are integers, the lower integer should come first. 
  if (ta == number && tb == number) {
    // If the left integer is lower than the right integer, the inputs are in the right order. 
    if (a < b) {
      return 1;
    }
    // If the left integer is higher than the right integer, the inputs are not in the right order. 
    else if (a > b) {
      return -1;
    }
    // Otherwise, the inputs are the same integer; continue checking the next part of the input.
  }
  // If both values are lists, 
  else if (ta == object && tb == object) {
    // compare the first value of each list, then the second value, and so on.
    for (let i = 0;; i++) {
      // If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.
      if (a.length <= i && b.length <= i) {
        break;
      }
      // If the left list runs out of items first, the inputs are in the right order. 
      else if (a.length <= i) {
        return 1;
      }
      // If the right list runs out of items first, the inputs are not in the right order. 
      else if (b.length <= i) {
        return -1;
      } else {
        let subResult = compare(a[i], b[i]);
        if (subResult != 0) {
          return subResult;
        }
      }
    }
  }
  // If exactly one value is an integer,
  else {
    // convert the integer to a list which contains that integer as its only value, then retry the comparison. 
    if (ta == number) {
      a = [a];
    } else {
      b = [b];
    }
    let subResult = compare(a, b);
    if (subResult != 0) {
      return subResult;
    }
  }
  return 0;
}

function arrayEqual(a, b) {
  if (typeof a != typeof b) {
    return false;
  }
  if (typeof a == number) {
    return a == b;
  } else {
    if (a.length != b.length) {
      return false;
    }
    for (let i = 0; i < a.length; i++) {
      if (!arrayEqual(a[i], b[i])) {
        return false;
      }
    }
    return true;
  }
}