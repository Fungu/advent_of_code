main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day05.txt", { encoding: "utf-8" })
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
  let part1 = "";
  let part2 = "";

  // Init stack1 and stack2
  let stacks1 = [];
  for (let i = 0; i < (lines[0].length + 1) / 4; i++) {
    stacks1.push([]);
  }
  let i = 0;
  for (; i < lines.length; i++) {
    if (lines[i][1] == "1") {
      break;
    }
    for (let a = 0; a < stacks1.length; a++) {
      let c = lines[i][1 + a * 4];
      if (c != " ") {
        stacks1[a].unshift(c);
      }
    }
  }
  let stacks2 = JSON.parse(JSON.stringify(stacks1));

  i += 2;
  for (; i < lines.length; i++) {
    let {amount, from, to} = lines[i].match(/move (?<amount>[0-9]+) from (?<from>[0-9]+) to (?<to>[0-9]+)/).groups;
    amount = parseInt(amount);
    from = parseInt(from);
    to = parseInt(to);

    // Part 1
    for (let a = 0; a < amount; a++) {
      stacks1[to - 1].push(stacks1[from - 1].pop());
    }

    // Part 2
    let elements = []
    for (let a = 0; a < amount; a++) {
      elements.push(stacks2[from - 1].pop())
    }
    for (let a = 0; a < amount; a++) {
      stacks2[to - 1].push(elements.pop());
    }
  }

  for (let a = 0; a < stacks1.length; a++) {
    part1 += stacks1[a].pop();
    part2 += stacks2[a].pop();
  }
  
  return [part1, part2];
}
