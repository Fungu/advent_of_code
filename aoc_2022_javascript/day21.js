let operators = new Map([
  ["+", function(a, b) {return a + b;}],
  ["-", function(a, b) {return a - b;}],
  ["*", function(a, b) {return a * b;}],
  ["/", function(a, b) {return a / b;}]
]);
let oppositeOperators = new Map([
  ["+", "-"],
  ["-", "+"],
  ["*", "/"],
  ["/", "*"]
]);
let equations = new Map();
let pathToHumn = ["humn"];
let results = new Map();
main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day21.txt", { encoding: "utf-8" })
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
  for (let line of lines) {
    let [left, right] = line.split(": ");
    if (right.includes(" ")) {
      let {a, operator, b} = right.match(/(?<a>[a-z]+) (?<operator>[\+\-\*/]+) (?<b>[a-z]+)/).groups;
      equations.set(left, {
        isConstant: false,
        a: a,
        operator: operator,
        b: b
      });
    } else {
      equations.set(left, {
        isConstant: true,
        a: parseInt(right)
      });
    }
  }
  let part1 = calculate("root")[0];
  let part2 = findHumn("root", 0);
  
  return [part1, part2];
}

function calculate(variable) {
  let equation = equations.get(variable);
  if (equation.isConstant) {
    results.set(variable, equation.a);
    return [equation.a, variable == "humn"];
  } else {
    let [resultA, isHumnA] = calculate(equation.a);
    let [resultB, isHumnB] = calculate(equation.b);
    let result = operators.get(equation.operator).call(this, resultA, resultB);
    results.set(variable, result);
    if (isHumnA || isHumnB) {
      pathToHumn.push(variable);
    }
    console.assert((isHumnA && isHumnB) == false);
    return [result, isHumnA || isHumnB];
  }
}

function findHumn(variable, humnTarget) {
  let equation = equations.get(variable);
  if (variable == "root") {
    if (pathToHumn.includes(equation.a)) {
      return findHumn(equation.a, results.get(equation.b));
    } else {
      return findHumn(equation.b, results.get(equation.a));
    }
  } else if (variable == "humn") {
    return humnTarget;
  } else {
    let oppositeOperator = operators.get(oppositeOperators.get(equation.operator));
    if (pathToHumn.includes(equation.a)) {
      return findHumn(equation.a, oppositeOperator.call(this, humnTarget, results.get(equation.b)));
    } else {
      if (equation.operator == "-") {
        return findHumn(equation.b, results.get(equation.a) - humnTarget);
      } else if (equation.operator == "/") {
        return findHumn(equation.b, results.get(equation.a) / humnTarget);
      } else {
        return findHumn(equation.b, oppositeOperator.call(this, humnTarget, results.get(equation.a)));
      }
    }
  }
}
