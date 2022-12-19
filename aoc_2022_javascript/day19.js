main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day19.txt", { encoding: "utf-8" })
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
  let blueprints = [];
  for (let line of lines) {
    let [name, right] = line.split(": ");
    let robots = right.split(".");
    let {oreore} = robots[0].match(/costs (?<oreore>[0-9]+) ore/).groups;
    let {clayore} = robots[1].match(/costs (?<clayore>[0-9]+) ore/).groups;
    let {obsidianore, obsidianclay} = robots[2].match(/costs (?<obsidianore>[0-9]+) ore and (?<obsidianclay>[0-9]+) clay/).groups;
    let {geodeore, geodeobsidian} = robots[3].match(/costs (?<geodeore>[0-9]+) ore and (?<geodeobsidian>[0-9]+) obsidian/).groups;
    let blueprint = {
      name: name,
      robots: [],
      mostNeeded: new Map(),
      materialWorths: new Map(),
    };
    blueprint.robots.push({
      produces: "ore",
      cost: new Map([["ore", parseInt(oreore)]])
    });
    blueprint.robots.push({
      produces: "clay",
      cost: new Map([["ore", parseInt(clayore)]])
    });
    blueprint.robots.push({
      produces: "obsidian",
      cost: new Map([["ore", parseInt(obsidianore)], ["clay", parseInt(obsidianclay)]])
    });
    blueprint.robots.push({
      produces: "geode",
      cost: new Map([["ore", parseInt(geodeore)], ["obsidian", parseInt(geodeobsidian)]])
    });
    blueprint.mostNeeded.set("ore", blueprint.robots.reduce((partialMax, robot) => Math.max(partialMax, getOrDefault(robot.cost, "ore", 0)), 0));
    blueprint.mostNeeded.set("clay", blueprint.robots.reduce((partialMax, robot) => Math.max(partialMax, getOrDefault(robot.cost, "clay", 0)), 0));
    blueprint.mostNeeded.set("obsidian", blueprint.robots.reduce((partialMax, robot) => Math.max(partialMax, getOrDefault(robot.cost, "obsidian", 0)), 0));
    blueprint.materialWorths.set("ore",  blueprint.robots[0].cost.get("ore"));
    blueprint.materialWorths.set("clay",  blueprint.robots[1].cost.get("ore"));
    blueprint.materialWorths.set("obsidian",  blueprint.robots[2].cost.get("ore") + blueprint.robots[2].cost.get("clay") * blueprint.clayWorth);
    blueprint.materialWorths.set("geode",  blueprint.robots[3].cost.get("ore") + blueprint.robots[3].cost.get("obsidian") * blueprint.obsidianWorth);
    blueprints.push(blueprint);
  }
  let part1 = 0;
  let part2 = 1;
  
  for (let i = 0; i < blueprints.length; i++) {
    let result = simulate({
      robots: new Map([["ore", 1]]),
      materials: new Map(),
      timeLeft: 24
    }, blueprints[i], new Map(), new Map());
    part1 += result * (i + 1);
  }
  
  for (let i = 0; i < Math.min(3, blueprints.length); i++) {
    let result = simulate({
      robots: new Map([["ore", 1]]),
      materials: new Map(),
      timeLeft: 32
    }, blueprints[i], new Map(), new Map());
    part2 *= result;
  }

  return [part1, part2];
}

function simulate(state, blueprint, dp, bestScoreMap) {
  let currentStateString = state.timeLeft + " " + Array.from(state.robots.values()).join(",") + " " + Array.from(state.materials.values()).join(",");
  if (dp.has(currentStateString)) {
    return dp.get(currentStateString);
  }
  let currentScore = 0;
  for (let [material, amount] of state.robots) {
    currentScore += amount * blueprint.materialWorths.get(material) * state.timeLeft;
  }
  for (let [material, amount] of state.materials) {
    currentScore += amount * blueprint.materialWorths.get(material);
  }
  let bestScore = getOrDefault(bestScoreMap, state.timeLeft, 0);
  if (bestScore > currentScore) {
    bestScoreMap.set(state.timeLeft, currentScore);
    if (state.robots.has("geode")) {
      return 0;
    }
  } else {
    bestScoreMap.set(state.timeLeft, currentScore);
  }

  if (state.timeLeft == 0) {
    return getOrDefault(state.materials, "geode", 0);
  }
  let ret = 0;
  for (let i = blueprint.robots.length - 1; i >= 0 ; i--) {
    let robot = blueprint.robots[i];
    if (i == 0 || getOrDefault(state.robots, blueprint.robots[i - 1].produces, 0) > 0) {
      if (i != blueprint.robots.length - 1 && state.robots.get(robot.produces) >= blueprint.mostNeeded.get(robot.produces)) {
        continue;
      }
      let newState = {
        robots: new Map(state.robots),
        materials: new Map(state.materials),
        timeLeft: state.timeLeft
      };
      let hasRun = false;
      let isBuilding = false;
      while (!hasRun || !isBuilding) {
        hasRun = true;
        newState.timeLeft--;
        // Start building if we have enough materials
        if (hasMaterials(newState.materials, robot.cost)) {
          increaseFromMap(newState.materials, robot.cost, -1);
          isBuilding = true;
        }
        
        // Collect material
        increaseFromMap(newState.materials, newState.robots, 1);
        
        // Finish building
        if (isBuilding) {
          increase(newState.robots, robot.produces, 1);
          ret = Math.max(ret, simulate(newState, blueprint, dp, bestScoreMap));
        }

        if (newState.timeLeft == 0) {
          ret = Math.max(ret, getOrDefault(newState.materials, "geode", 0));
          break;
        }
      }
    }
  }
  if (state.timeLeft > 10) {
    dp.set(currentStateString, ret);
  }
  return ret;
}

function getOrDefault(map, key, defaultValue) {
  if (map.has(key)) {
    return map.get(key);
  } else {
    return defaultValue;
  }
}

function increase(map, key, value) {
  if (map.has(key)) {
    map.set(key, map.get(key) + value);
  } else {
    map.set(key, value);
  }
}

function increaseFromMap(map, otherMap, mult) {
  for (let [key, value] of otherMap) {
    increase(map, key, mult * value);
  }
}

function hasMaterials(materials, cost) {
  for (let [requiredMaterial, amount] of cost) {
    if (getOrDefault(materials, requiredMaterial, 0) < amount) {
      return false;
    }
  }
  return true;
}