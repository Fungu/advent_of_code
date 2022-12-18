main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day11.txt", { encoding: "utf-8" })
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
  let part1 = shenanigans(lines, 20, true);
  let part2 = shenanigans(lines, 10000, false);
  return [part1, part2];
}

function shenanigans(lines, rounds, firstPart) {
  let monkeys = [];
  let multiple = 1;
  for (let i = 0; i < lines.length; i++) {
    let monkey = {
      name: lines[i++].split(" ")[1].replace(":", ""),
      items: lines[i++].split("items: ")[1].split(", ").map(x => parseInt(x)),
      operation: lines[i++].split("Operation: ")[1].replace("new", "item"),
      test: parseInt(lines[i++].split("by ")[1]),
      ifTrue: parseInt(lines[i++].split("to monkey ")[1]),
      ifFalse: parseInt(lines[i++].split("to monkey ")[1]),
      inspects: 0
    };
    multiple *= monkey.test;
    monkeys.push(monkey);
  }
  for (let round = 0; round < rounds; round++) {
    for (let monkey of monkeys) {
      for (let old of monkey.items) {
        monkey.inspects++;
        eval(monkey.operation); // item = old * 19
        if (firstPart) {
          item = Math.floor(item / 3);
        } else {
          item %= multiple;
        }
        if (item % monkey.test == 0) {
          monkeys[monkey.ifTrue].items.push(item);
        } else {
          monkeys[monkey.ifFalse].items.push(item);
        }
      }
      monkey.items = [];
    }
  }
  monkeys.sort((a, b) => b.inspects - a.inspects);

  return monkeys[0].inspects * monkeys[1].inspects;
}