class Face {
  constructor(pos, grid) {
    this.pos = pos;
    this.grid = grid;
    this.connections = new Map();
  }

  toString() {
    return `Face(${this.pos.x},${this.pos.y})`;
  }
}

class Cube {
  constructor(grid) {
    this.faces = [];
    this.cubeWidth = 50;
    for (let y = 0; y < grid.length; y += this.cubeWidth) {
      for (let x = 0; x < grid[y].length; x += this.cubeWidth) {
        if (grid[y][x] != " ") {
          let faceGrid = [];
          for (let a = 0; a < this.cubeWidth; a++) {
            faceGrid.push(grid[y + a].slice(x, x + this.cubeWidth));
          }
          this.faces.push(new Face({x: x / this.cubeWidth, y: y / this.cubeWidth}, faceGrid));
        }
      }
    }
    let max = this.cubeWidth - 1;
    for (let fa of this.faces) {
      for (let fb of this.faces) {
        if (fa == fb) {
          continue;
        }
        if (fa.pos.y == fb.pos.y) {
          if (fa.pos.x + 1 == fb.pos.x) { // Right
            fa.connections.set("[1,0]", {
              face: fb,
              dirChange: {x: 1, y: 0},
              posChange: function(pos) {return {x: 0, y: pos.y};}
            });
          } else if (fa.pos.x - 1 == fb.pos.x) { // Left
            fa.connections.set("[-1,0]", {
              face: fb,
              dirChange: {x: -1, y: 0},
              posChange: function(pos) {return {x: max, y: pos.y};}
            });
          }
        } else if (fa.pos.x == fb.pos.x) {
          if (fa.pos.y + 1 == fb.pos.y) { // Down
            fa.connections.set("[0,1]", {
              face: fb,
              dirChange: {x: 0, y: 1},
              posChange: function(pos) {return {x: pos.x, y: 0};}
            });
          } else if (fa.pos.y - 1 == fb.pos.y) { // Up
            fa.connections.set("[0,-1]", {
              face: fb,
              dirChange: {x: 0, y: -1},
              posChange: function(pos) {return {x: pos.x, y: max};}
            });
          }
        }
      }
    }

    // Hard coded connections
    this.getFace(1,0).connections.set("[0,-1]", {
      face: this.getFace(0,3),
      dirChange: {x: 1, y: 0},
      posChange: function(pos) {return {x: 0, y: pos.x};}
    });
    this.getFace(1,0).connections.set("[-1,0]", {
      face: this.getFace(0,2),
      dirChange: {x: 1, y: 0},
      posChange: function(pos) {return {x: 0, y: max - pos.y};}
    });

    this.getFace(2,0).connections.set("[0,-1]", {
      face: this.getFace(0,3),
      dirChange: {x: 0, y: -1},
      posChange: function(pos) {return {x: pos.x, y: max};}
    });
    this.getFace(2,0).connections.set("[0,1]", {
      face: this.getFace(1,1),
      dirChange: {x: -1, y: 0},
      posChange: function(pos) {return {x: max, y: pos.x};}
    });
    this.getFace(2,0).connections.set("[1,0]", {
      face: this.getFace(1,2),
      dirChange: {x: -1, y: 0},
      posChange: function(pos) {return {x: max, y: max - pos.y};}
    });

    this.getFace(1,1).connections.set("[-1,0]", {
      face: this.getFace(0,2),
      dirChange: {x: 0, y: 1},
      posChange: function(pos) {return {x: pos.y, y: 0};}
    });
    this.getFace(1,1).connections.set("[1,0]", {
      face: this.getFace(2,0),
      dirChange: {x: 0, y: -1},
      posChange: function(pos) {return {x: pos.y, y: max};}
    });

    this.getFace(1,2).connections.set("[1,0]", {
      face: this.getFace(2,0),
      dirChange: {x: -1, y: 0},
      posChange: function(pos) {return {x: max, y: max - pos.y};}
    });
    this.getFace(1,2).connections.set("[0,1]", {
      face: this.getFace(0,3),
      dirChange: {x: -1, y: 0},
      posChange: function(pos) {return {x: max, y: pos.x};}
    });

    this.getFace(0,2).connections.set("[0,-1]", {
      face: this.getFace(1,1),
      dirChange: {x: 1, y: 0},
      posChange: function(pos) {return {x: 0, y: pos.x};}
    });
    this.getFace(0,2).connections.set("[-1,0]", {
      face: this.getFace(1,0),
      dirChange: {x: 1, y: 0},
      posChange: function(pos) {return {x: 0, y: max - pos.y};}
    });

    this.getFace(0,3).connections.set("[-1,0]", {
      face: this.getFace(1,0),
      dirChange: {x: 0, y: 1},
      posChange: function(pos) {return {x: pos.y, y: 0};}
    });
    this.getFace(0,3).connections.set("[1,0]", {
      face: this.getFace(1,2),
      dirChange: {x: 0, y: -1},
      posChange: function(pos) {return {x: pos.y, y: max};}
    });
    this.getFace(0,3).connections.set("[0,1]", {
      face: this.getFace(2,0),
      dirChange: {x: 0, y: 1},
      posChange: function(pos) {return {x: pos.x, y: 0};}
    });
  }

  getFace(x, y) {
    for (let face of this.faces) {
      if (face.pos.x == x && face.pos.y == y) {
        return face;
      }
    }
    console.log(`Can't find face at ${x},${y}`)
  }

  move(face, pos, dir, steps, ignoreWalls=false) {
    let retPos = {x: pos.x, y: pos.y};
    let nextPos = {x: pos.x, y: pos.y};
    let nextFace = face;
    let nextDir = dir;
    for (let i = 0; i < steps; i++) {
      nextPos.x += nextDir.x;
      nextPos.y += nextDir.y;
      if (nextPos.y < 0 || nextPos.x < 0 || nextPos.y >= this.cubeWidth || nextPos.x >= this.cubeWidth) {
        let connection;
        if (nextPos.y < 0) {
          connection = nextFace.connections.get("[0,-1]");
        } else if (nextPos.x < 0) {
          connection = nextFace.connections.get("[-1,0]");
        } else if (nextPos.y >= this.cubeWidth) {
          connection = nextFace.connections.get("[0,1]");
        } else if (nextPos.x >= this.cubeWidth) {
          connection = nextFace.connections.get("[1,0]");
        }
        nextFace = connection.face;
        nextPos = connection.posChange.call(this, nextPos);
        nextDir = connection.dirChange;
      }
      if (nextFace.grid[nextPos.y][nextPos.x] == "#" && !ignoreWalls) {
        return [face, retPos, dir];
      }
      retPos.x = nextPos.x;
      retPos.y = nextPos.y;
      dir = nextDir;
      face = nextFace;
    }
    return [face, retPos, dir];
  }

  validateConnections() {
    for (let face of this.faces) {
      console.assert(face.connections.size == 4, `Face ${face.pos.x},${face.pos.y} does not have 4 connections: ${face.connections.size}`);
    }
    for (let face of this.faces) {
      let pos = {x: 1, y: 1};
      let dir = {x: 0, y: -1};
      let [faceA, posA, dirA] = this.move(face, pos, dir, 3, true);
      let [faceB, posB, dirB] = this.move(faceA, posA, rotate(dirA, "L"), 3, true);
      let [faceC, posC, dirC] = this.move(faceB, posB, rotate(dirB, "L"), 3, true);
      dirC = rotate(dirC, "L");
      console.assert(pos.x == posC.x && pos.y == posC.y, `Pos ${pos.x},${pos.y} | ${posC.x},${posC.y}`);
      console.assert(dir.x == dirC.x && dir.y == dirC.y, `Dir ${dir.x},${dir.y} | ${dirC.x},${dirC.y}`);
      console.assert(face == faceC, `Face ${face.pos.x},${face.pos.y} | ${faceC.pos.x},${faceC.pos.y}`);
    }
  }
}

main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day22.txt", { encoding: "utf-8" })
    .split("\r\n");
  let start = Date.now();
  solution = solve(input);
  let end = Date.now();
  console.log(`Execution time: ${end - start} ms`);
  console.log(`Part 1: ${solution[0]}`);
  console.log(`Part 2: ${solution[1]}`);
}

function solve(lines) {
  let pos = {x: 0, y: 0};
  let dir = {x: 1, y: 0};
  for (let i = 0; i < lines[0].length; i++) {
    if (lines[0][i] == ".") {
      pos.x = i;
      break;
    }
  }
  let instructions = lines[lines.length - 1];
  let instructionIndex = 0;
  let grid = lines.slice(0, lines.length - 2);
  while (instructionIndex < instructions.length) {
    let [instruction, i] = getNextInstruction(instructions, instructionIndex);
    instructionIndex = i;
    if (instruction == "R" || instruction == "L") {
      dir = rotate(dir, instruction);
    } else {
      pos = move(grid, pos, dir, instruction);
    }
  }

  let part1 = getScore(pos, dir);

  let cube = new Cube(grid);
  cube.validateConnections();
  let face = cube.getFace(1, 0);
  pos = {x: 0, y: 0};
  dir = {x: 1, y: 0};
  instructionIndex = 0;
  while (instructionIndex < instructions.length) {
    let [instruction, i] = getNextInstruction(instructions, instructionIndex);
    instructionIndex = i;
    if (instruction == "R" || instruction == "L") {
      dir = rotate(dir, instruction);
    } else {
      let [faceA, posA, dirA] = cube.move(face, pos, dir, instruction);
      face = faceA;
      pos = posA;
      dir = dirA;
    }
  }
  let part2 = getScore({x: pos.x + face.pos.x * cube.cubeWidth, y: pos.y + face.pos.y * cube.cubeWidth}, dir);

  return [part1, part2];
}

function move(grid, pos, dir, steps) {
  let nextPos = {x: pos.x, y: pos.y};
  for (let i = 0; i < steps; i++) {
    nextPos.x += dir.x;
    nextPos.y += dir.y;
    if (nextPos.y < 0 || nextPos.y >= grid.length || nextPos.x < 0 || nextPos.x >= grid[nextPos.y].length || grid[nextPos.y][nextPos.x] == " ") {
      nextPos = wrap(grid, nextPos, dir);
    } 
    if (grid[nextPos.y][nextPos.x] == "#") {
      return pos;
    }
    pos.x = nextPos.x;
    pos.y = nextPos.y;
  }
  return nextPos;
}

function getNextInstruction(instructions, index) {
  let instruction;
  if (instructions[index] == "R" || instructions[index] == "L") {
    instruction = instructions[index];
    index++;
  } else {
    let b = index + 1;
    while (b < instructions.length) {
      if (instructions[b] == "R" || instructions[b] == "L") {
        break;
      }
      b++;
    }
    instruction = parseInt(instructions.slice(index, b));
    index = b;
  }
  return [instruction, index];
}

function rotate(dir, rotation) {
  if (rotation == "R") {
    // [1, 0] -> [0, 1] -> [-1, 0] -> [0, -1]
    return {x: -dir.y, y: dir.x};
  } else {
    // [1, 0] -> [0, -1] -> [-1, 0] -> [0, 1]
    return {x: dir.y, y: -dir.x};
  }
}

function wrap(grid, pos, dir) {
  pos.x -= dir.x;
  pos.y -= dir.y;
  while (pos.y >= 0 && pos.y < grid.length && pos.x >= 0 && pos.x < grid[pos.y].length && grid[pos.y][pos.x] != " ") {
    pos.x -= dir.x;
    pos.y -= dir.y;
  }
  pos.x += dir.x;
  pos.y += dir.y;
  return pos;
}

function getScore(pos, dir) {
  let facingScoreX = new Map([[-1, 2], [0, 0], [1, 0]]);
  let facingScoreY = new Map([[-1, 3], [0, 0], [1, 2]]);
  return 1000 * (pos.y + 1) + 4 * (pos.x + 1) + facingScoreX.get(dir.x) + facingScoreY.get(dir.y);
}

function print(grid, pos, dir) {
  for (let y = 0; y < grid.length; y++) {
    let row = "";
    for (let x = 0; x < grid[y].length; x++) {
      if (x == pos.x && y == pos.y) {
        row += "X";
      } else {
        row += grid[y][x];
      }
    }
    console.log(row);
  }
}