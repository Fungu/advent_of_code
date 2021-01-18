import java.io.IOException;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Day20 implements AocSolver {

	public static void main(String[] args) throws IOException, InterruptedException {
		Aoc.runRaw(new Day20());
	}

	final int gridSize = 2000;
	int maxX = 0;
	int maxY = 0;
	int minX = gridSize;
	int minY = gridSize;
	char[][] grid = new char[gridSize][gridSize];

	char[] inputArray;
	HashSet<String> seenStates = new HashSet<>();

	@Override
	public void solve(String input) {
		inputArray = input.toCharArray();
		initGrid();

		parseRegex(gridSize / 2, gridSize / 2, 0);

		// printGrid();

		bfs();
	}

	private void parseRegex(int x, int y, int index) {
		String key = x + " " + y + " " + index;
		if (seenStates.contains(key)) {
			return;
		}
		seenStates.add(key);
		for (; index < inputArray.length; index++) {
			char c = inputArray[index];

			if (c == '(') {
				parseRegex(x, y, index + 1);
				int parenthesisDepth = 0;
				for (int i = index + 1;; i++) {
					if (inputArray[i] == ')') {
						parenthesisDepth--;
					} else if (inputArray[i] == '(') {
						parenthesisDepth++;
					} else if (inputArray[i] == '|' && parenthesisDepth == 0) {
						parseRegex(x, y, i + 1);
					} else if (parenthesisDepth < 0) {
						return;
					}
				}
			} else if (c == ')') {

			} else if (c == '|') {
				int parenthesisDepth = 1;
				for (int i = index;; i++) {
					if (inputArray[i] == ')') {
						parenthesisDepth--;
					} else if (inputArray[i] == '(') {
						parenthesisDepth++;
					}
					if (parenthesisDepth == 0) {
						index = i;
						break;
					}
				}

			} else if (c == '$') {
				return;

			} else if (c == 'E') {
				x++;
				grid[y][x] = ' ';
				x++;
				grid[y][x] = ' ';
				maxX = Math.max(maxX, x);

			} else if (c == 'W') {
				x--;
				grid[y][x] = ' ';
				x--;
				grid[y][x] = ' ';
				minX = Math.min(minX, x);

			} else if (c == 'S') {
				y++;
				grid[y][x] = ' ';
				y++;
				grid[y][x] = ' ';
				maxY = Math.max(maxY, y);

			} else if (c == 'N') {
				y--;
				grid[y][x] = ' ';
				y--;
				grid[y][x] = ' ';
				minY = Math.min(minY, y);
			}
		}
	}

	private void initGrid() {
		for (int y = 0; y < gridSize; y++) {
			for (int x = 0; x < gridSize; x++) {
				grid[y][x] = '#';
			}
		}
	}

	@SuppressWarnings("unused")
	private void printGrid() {
		for (int y = minY - 1; y <= maxY + 1; y++) {
			for (int x = minX - 1; x <= maxX + 1; x++) {
				if (x == gridSize / 2 && y == gridSize / 2) {
					System.out.print("X");
				} else {
					System.out.print(grid[y][x]);
				}
			}
			System.out.println();
		}
	}
	

	private void bfs() {
		IntTuple[] directions = { new IntTuple(1, 0), new IntTuple(-1, 0), new IntTuple(0, 1), new IntTuple(0, -1) };
		Deque<IntTuple> open = new ArrayDeque<>();
		Set<IntTuple> closed = new HashSet<>();
		Map<IntTuple, Integer> distances = new HashMap<>();

		open.add(new IntTuple(gridSize / 2, gridSize / 2));
		distances.put(new IntTuple(gridSize / 2, gridSize / 2), 0);

		int part2 = 0;
		IntTuple lastPos = null;
		while (!open.isEmpty()) {
			IntTuple currentPos = open.poll();
			lastPos = currentPos;
			int distance = distances.get(currentPos);
			if (distance >= 1000) {
				part2++;
			}

			for (IntTuple dir : directions) {
				IntTuple neighbor = new IntTuple(currentPos.values.clone());
				neighbor.add(dir);
				if (grid[neighbor.values[0]][neighbor.values[1]] != '#') {
					neighbor.add(dir);
					if (open.contains(neighbor) == false && closed.contains(neighbor) == false) {
						open.add(neighbor);
						distances.put(neighbor, distance + 1);
					}
				}
			}
			closed.add(currentPos);
		}
		System.out.println("Part 1: " + distances.get(lastPos));
		System.out.println("Part 2: " + part2);
	}

}
