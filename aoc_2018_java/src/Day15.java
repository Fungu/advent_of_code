import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

public class Day15 implements AocSolver {

	public static void main(String[] args) throws IOException, InterruptedException {
		Aoc.runLines(new Day15());
	}

	boolean[][] terrain;
	ArrayList<Unit> units;

	@Override
	public void solve(List<String> inputLines) {
		int part1 = play(inputLines, 3);

		Integer part2 = null;
		int elfAttack = 4;
		while (part2 == null) {
			int result = play(inputLines, elfAttack);
			if (units.stream().noneMatch(u -> u.elf && u.hp <= 0)) {
				part2 = result;
			}
			elfAttack++;
		}

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	private int play(List<String> inputLines, int elfAttack) {
		int width = inputLines.get(0).length();
		int height = inputLines.size();

		terrain = new boolean[height][width];
		units = new ArrayList<>();
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				if (inputLines.get(y).charAt(x) == '#') {
					terrain[y][x] = true;
				} else if (inputLines.get(y).charAt(x) == 'E') {
					Unit unit = new Unit(x, y, true);
					unit.attack = elfAttack;
					units.add(unit);
				} else if (inputLines.get(y).charAt(x) == 'G') {
					units.add(new Unit(x, y, false));
				}
			}
		}

		int round = 0;
		boolean hasElfs = true;
		boolean hasGoblins = true;
		while (hasElfs && hasGoblins) {
			// print();
			units.sort(unitComparator);
			for (Unit unit : units) {
				if (unit.hp <= 0) {
					continue;
				}
				hasElfs = units.stream().anyMatch(u -> u.elf && u.hp > 0);
				hasGoblins = units.stream().anyMatch(u -> !u.elf && u.hp > 0);
				if (!hasElfs || !hasGoblins) {
					round--;
					break;
				}

				move(unit);
				attack(unit);
			}

			round++;
		}

		int totalHp = units.stream().map(u -> u.hp).filter(h -> h > 0).reduce((a, b) -> a + b).get();
		return (round * totalHp);
	}

	private void attack(Unit unit) {
		Unit bestEnemy = null;
		for (Unit enemy : units) {
			if (unit.elf != enemy.elf && enemy != unit && enemy.hp > 0) {
				if (Math.abs(enemy.pos.x - unit.pos.x) + Math.abs(enemy.pos.y - unit.pos.y) == 1) {
					if (bestEnemy == null) {
						bestEnemy = enemy;
					}
					if ((enemy.hp < bestEnemy.hp) || (enemy.hp == bestEnemy.hp && enemy.pos.y < bestEnemy.pos.y) || (enemy.hp == bestEnemy.hp && enemy.pos.y == bestEnemy.pos.y && enemy.pos.x < bestEnemy.pos.x)) {
						bestEnemy = enemy;
					}
				}
			}
		}
		if (bestEnemy != null) {
			bestEnemy.hp -= unit.attack;
		}
	}

	private void move(Unit unit) {
		PriorityQueue<DistPos> open = new PriorityQueue<DistPos>(readingOrderComparator);
		Set<DistPos> closed = new HashSet<>();
		Map<DistPos, DistPos> sources = new HashMap<>();

		unit.pos.dist = 0;
		open.add(unit.pos);
		sources.put(unit.pos, null);

		DistPos bestSquare = null;

		while (!open.isEmpty() && (bestSquare == null || open.peek().dist == bestSquare.dist)) {
			DistPos currentPos = open.poll();
			if (isAdjacent(currentPos, !unit.elf)) {
				if (bestSquare == null || currentPos.y < bestSquare.y || (currentPos.y == bestSquare.y && currentPos.x < bestSquare.x)) {
					bestSquare = currentPos;
				}
			}

			for (DistPos neighbor : currentPos.getNeighbors()) {
				if (!closed.contains(neighbor) && isEmpty(neighbor)) {
					if (!open.contains(neighbor)) {
						open.add(neighbor);
					}
					DistPos source = sources.get(currentPos);
					if (source == null) {
						source = neighbor;
					}
					if (!sources.containsKey(neighbor) || readingOrderComparator.compare(sources.get(neighbor), source) > 0) {
						sources.put(neighbor, source);
					}
				}
			}
			closed.add(currentPos);
		}

		if (bestSquare != null) {
			DistPos nextPos = sources.get(bestSquare);
			if (nextPos != null) {
				unit.pos = sources.get(bestSquare);
			}
		}
	}

	private boolean isAdjacent(DistPos pos, boolean elf) {
		for (Unit unit : units) {
			if (unit.hp > 0 && unit.elf == elf) {
				if (unit.pos.x == pos.x && Math.abs(unit.pos.y - pos.y) == 1) {
					return true;
				} else if (unit.pos.y == pos.y && Math.abs(unit.pos.x - pos.x) == 1) {
					return true;
				}
			}
		}
		return false;
	}

	private boolean isEmpty(DistPos pos) {
		if (terrain[pos.y][pos.x]) {
			return false;
		}
		for (Unit unit : units) {
			if (unit.hp > 0 && unit.pos.x == pos.x && unit.pos.y == pos.y) {
				return false;
			}
		}
		return true;
	}

	@SuppressWarnings("unused")
	private void print() {
		System.out.println();
		for (int y = 0; y < terrain.length; y++) {
			for (int x = 0; x < terrain[0].length; x++) {
				boolean isUnit = false;
				for (Unit unit : units) {
					if (unit.hp > 0 && unit.pos.x == x && unit.pos.y == y) {
						System.out.print(unit.elf ? "E" : "G");
						isUnit = true;
					}
				}
				if (!isUnit) {
					System.out.print(terrain[y][x] ? '#' : '.');
				}
			}
			System.out.print("   ");
			boolean first = true;
			for (int x = 0; x < terrain[0].length; x++) {
				for (Unit unit : units) {
					if (unit.hp > 0 && unit.pos.y == y && unit.pos.x == x) {
						System.out.print((first ? "" : ", ") + (unit.elf ? "E" : "G") + "(" + unit.hp + ")");
						first = false;
					}
				}
			}
			System.out.println();
		}
	}

	class DistPos {
		int x, y, dist;

		public DistPos(int x, int y) {
			this.x = x;
			this.y = y;
		}

		public DistPos(int x, int y, int dist) {
			this.x = x;
			this.y = y;
			this.dist = dist;
		}

		public DistPos[] getNeighbors() {
			DistPos[] neighbors = new DistPos[4];
			neighbors[0] = new DistPos(x, y - 1, dist + 1);
			neighbors[1] = new DistPos(x - 1, y, dist + 1);
			neighbors[2] = new DistPos(x + 1, y, dist + 1);
			neighbors[3] = new DistPos(x, y + 1, dist + 1);
			return neighbors;
		}

		@Override
		public boolean equals(Object o) {
			DistPos other = (DistPos) o;
			return other.x == x && other.y == y;
		}

		@Override
		public int hashCode() {
			return y * 99999 + x;
		}
	}

	class Unit {
		DistPos pos;
		boolean elf;
		int hp = 200;
		int attack = 3;

		public Unit(int x, int y, boolean elf) {
			pos = new DistPos(x, y);
			this.elf = elf;
		}
	}

	private final Comparator<Unit> unitComparator = new Comparator<Unit>() {
		@Override
		public int compare(Unit o1, Unit o2) {
			return o1.pos.y != o2.pos.y ? o1.pos.y - o2.pos.y : o1.pos.x - o2.pos.x;
		}
	};

	private final Comparator<DistPos> readingOrderComparator = new Comparator<DistPos>() {
		@Override
		public int compare(DistPos o1, DistPos o2) {
			if (o1.dist != o2.dist) {
				return o1.dist - o2.dist;
			}
			return (o1.y != o2.y ? o1.y - o2.y : o1.x - o2.x);
		}
	};
}
