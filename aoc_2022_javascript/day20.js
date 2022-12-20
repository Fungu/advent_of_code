class Node {
  constructor(data, next = null, prev = null) {
    this.data = data;
    this.next = next;
    this.prev = prev;
  }
}

class CircularLinkedList {
  constructor() {
    this.first = null;
    this.list = [];
  }
  
  insertFirst(data) {
    const node = new Node(data, this.first);
    this.first = node;
  }

  insertAfter(refNode, newNode) {
    newNode.prev = refNode;
    newNode.next = refNode.next;
    newNode.next.prev = newNode;
    refNode.next = newNode;
  }

  insertAtEnd(newNode) {
    if (this.first == null) {
      this.first = newNode;
      newNode.next = newNode;
      newNode.prev = newNode;
    } else {
      this.insertAfter(this.first.prev, newNode);
    }
    this.list.push(newNode);
  }

  remove(node) {
    if (this.first.next == this.first) {
      this.first = null;
    } else {
      node.prev.next = node.next;
      node.next.prev = node.prev;
      if (this.first == node) {
        this.first = node.next;
      }
    }
  }

  print() {
    let node = this.first;
    for (let i = 0; i < this.list.length; i++) {
      console.log(node.data);
      node = node.next;
    }
  }
}

main();

function main() {
  const fs = require("fs");
  const input = fs
    .readFileSync("input/day20.txt", { encoding: "utf-8" })
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
  let part1 = decrypt(lines, true);
  let part2 = decrypt(lines, false);
  
  return [part1, part2];
}

function decrypt(lines, firstPart) {
  let list = new CircularLinkedList();
  let nodeZero = null;
  let decryptionKey = 811589153;
  if (firstPart) {
    decryptionKey = 1;
  }
  for (let line of lines) {
    let n = new Node((parseInt(line) * decryptionKey));
    list.insertAtEnd(n);
    if (n.data == 0) {
      nodeZero = n;
    }
  }
  let rounds = 10;
  if (firstPart) {
    rounds = 1;
  }
  for (let a = 0; a < rounds; a++) {
    for (let node of list.list) {
      let targetNode = node.prev;
      list.remove(node);
      for (let i = 0; i < Math.abs(node.data) % (list.list.length - 1); i++) {
        if (node.data < 0) {
          targetNode = targetNode.prev;
        } else if (node.data > 0) {
          targetNode = targetNode.next;
        }
      }
      list.insertAfter(targetNode, node);
    }
  }
  
  let ret = 0;
  let node = nodeZero;
  for (let i = 0; i < 3001; i++) {
    if (i == 1000 || i == 2000 || i == 3000) {
      ret += node.data;
    }
    node = node.next;
  }
  return ret;
}