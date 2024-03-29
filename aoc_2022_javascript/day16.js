let allValves = new Map();
let travelTimes = new Map();
let valvesWithFlow = [];
let dp = new Map();
main();

function main() {
  const fs = require("fs");
  const lines = fs
    .readFileSync("input/day16.txt", { encoding: "utf-8" })
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
  for (let line of lines) {
    let {name, flow, tunnels} = line.match(/Valve (?<name>[A-Z]+) has flow rate=(?<flow>[0-9]+); tunnels? leads? to valves? (?<tunnels>.+)/).groups;
    allValves.set(name, {
      name: name,
      flow: parseInt(flow),
      tunnels: tunnels.split(", ") 
    });
  }
  valvesWithFlow = Array.from(allValves.keys()).filter(k => allValves.get(k).flow > 0);
  console.assert(!valvesWithFlow.includes("AA"));
  valvesWithFlow.push("AA");
  valvesWithFlow.sort();
  for (let i = 0; i < valvesWithFlow.length; i++) {
    for (let j = i + 1; j < valvesWithFlow.length; j++) {
      let openSet = [valvesWithFlow[i]];
      let distances = [0];
      let closedSet = [];
      while (openSet.length > 0) {
        let pos = openSet.shift();
        let distance = distances.shift();
        if (pos == valvesWithFlow[j]) {
          travelTimes.set(valvesWithFlow[i] + "-" + valvesWithFlow[j], distance);
          break;
        }
        closedSet.push(pos);
        for (let neighbor of allValves.get(pos).tunnels) {
          if (!closedSet.includes(neighbor) && !openSet.includes(neighbor)) {
            openSet.push(neighbor);
            distances.push(distance + 1);
          }
        }
      }
    }
  }
  let part1 = search({
    pos: "AA",
    timeLeft: 30,
    openValves: ["AA"],
  }, valvesWithFlow);
  dp = new Map();

  let part2 = searchPart2();

  return [part1, part2];
}

function searchPart2() {
  valvesWithFlow.shift();
  let nrOfValves = valvesWithFlow.length;
  let nrOfStates = Math.pow(2, nrOfValves) / 2;
  let ret = 0;
  for (let i = 0; i < nrOfStates; i++) {
    let binaryString = i.toString(2).padStart(nrOfValves, "0");
    let v1 = valvesWithFlow.filter((element, index) => binaryString[index] == "1");
    let v2 = valvesWithFlow.filter((element, index) => binaryString[index] != "1");
    dp = new Map();
    let subRet = search({
      pos: "AA",
      timeLeft: 26,
      openValves: [],
    }, v1);
    dp = new Map();
    subRet += search({
      pos: "AA",
      timeLeft: 26,
      openValves: [],
    }, v2);
    ret = Math.max(ret, subRet);
    // console.log(i + "/" + nrOfStates + ": " + v1 + " - " + v2 + " - " + ret + " (" + subRet + ")");
  }
  return ret;
}

function search(state, valves) {
  let currentStateString = JSON.stringify(state);
  if (dp.has(currentStateString)) {
    return dp.get(currentStateString);
  }
  
  let startFlow = getFlow(state);
  if (state.timeLeft == 0) {
    return startFlow;
  }
  if (allValves.get(state.pos).flow > 0) {
    state.openValves.push(state.pos);
    state.openValves.sort();
    state.timeLeft--;
  }
  if (state.openValves.length == valves.length) {
    return startFlow + getFlow(state) * (state.timeLeft - 0);
  }
  let flow = getFlow(state);
  let ret = 0;
  for (let dest of valves) {
    if (dest != state.pos && !state.openValves.includes(dest)) {
      let travelTime = travelTimes.get([state.pos, dest].sort().join("-"));
      if (travelTime >= state.timeLeft) {
        ret = Math.max(ret, flow * (state.timeLeft + 0));
      } else {
        let nextState = {
          pos: dest,
          timeLeft: state.timeLeft - travelTime,
          openValves: [...state.openValves]
        };
        ret = Math.max(ret, flow * (travelTime + 0) + search(nextState, valves));
      }
    }
  }
  ret += startFlow;
  dp.set(currentStateString, ret);
  return ret;
}

function getFlow(state) {
  let ret = 0;
  for (let valve of state.openValves) {
    ret += allValves.get(valve).flow;
  }
  return ret;
}
