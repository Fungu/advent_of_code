main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day15.txt", { encoding: "utf-8" })
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
  let sensors = [];
  for (let line of lines) {
    let {sx, sy, bx, by} = line.match(/Sensor at x=(?<sx>-?[0-9]+), y=(?<sy>-?[0-9]+): closest beacon is at x=(?<bx>-?[0-9]+), y=(?<by>-?[0-9]+)/).groups;
    sensors.push({
      x: parseInt(sx),
      y: parseInt(sy),
      distance: Math.abs(parseInt(sx) - parseInt(bx)) + Math.abs(parseInt(sy) - parseInt(by)) 
    });
  }

  let sections = [];
  for (let sensor of sensors) {
    let d = sensor.distance - Math.abs(sensor.y - 2000000);
    if (d >= 0) {
      let minX = sensor.x - d;
      let maxX = sensor.x + d;
      mergeRanges(sections, [minX, maxX]);
    }
  }
  let part1 = sections.reduce((total, section) => total + (section[1] - section[0]), 0)

  let part2 = 0;
  for (let i = 0; i <= 4000000; i++) {
    sections = [];
    for (let sensor of sensors) {
      let d = sensor.distance - Math.abs(sensor.y - i);
      if (d >= 0) {
        let minX = sensor.x - d;
        let maxX = sensor.x + d;
        mergeRanges(sections, [minX, maxX]);
      }
    }
    if (sections.length > 1) {
      let x = 0;
      if (sections[0][0] < sections[1][0]) {
        x = sections[0][1] + 1;
      } else {
        x = sections[1][1] + 1;
      }
      part2 = i + 4000000 * x;
      break;
    }
  }

  return [part1, part2];
}

function mergeRanges(rangeList, input) {
  let modifiedIndex = -1;
  for (let i = 0; i < rangeList.length; i++) {
    let section = rangeList[i];
    if (section[0] <= input[0] && input[1] <= section[1]) {
      // Input is within another range
      return;
    } else if (input[0] <= section[0] && section[1] <= input[1]) {
      // Another range is within input.
      if (modifiedIndex >= 0) {
        rangeList.splice(i, 1);
        i--;
      } else {
        section[0] = input[0];
        section[1] = input[1];
        modifiedIndex = i;
      }
    } else if (input[0] >= section[0] && input[0] <= section[1]) {
      if (modifiedIndex >= 0) {
        rangeList[modifiedIndex][0] = section[0];
        rangeList.splice(i, 1);
        i--;
      } else {
        section[1] = input[1];
        input = section;
        modifiedIndex = i;
      }
    } else if (input[1] >= section[0] && input[1] <= section[1]) {
      if (modifiedIndex >= 0) {
        rangeList[modifiedIndex][1] = section[1];
        rangeList.splice(i, 1);
        i--;
      } else {
        section[0] = input[0];
        input = section;
        modifiedIndex = i;
      }
    }
  }
  if (modifiedIndex == -1) {
    rangeList.push(input);
  }
}
