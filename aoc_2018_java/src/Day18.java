import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Day18 implements AocSolver {

	public static void main(String[] args) throws Exception {
		Aoc.runLines(new Day18());
	}

	final char OPEN = '.';
	final char TREE = '|';
	final char LUMBER = '#';

	@Override
	public void solve(List<String> inputLines) {
		int part1 = play(inputLines, 10);
		int part2 = play(inputLines, 1000000000);

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	private int play(List<String> inputLines, int iterations) {
		int maxX = inputLines.get(0).length();
		int maxY = inputLines.size();
		char[][] grid;
		grid = new char[maxY][maxX];

		for (int y = 0; y < maxY; y++) {
			for (int x = 0; x < maxX; x++) {
				grid[y][x] = inputLines.get(y).charAt(x);
			}
		}

		char[][] nextGrid;
		ArrayList<Integer> hashList = new ArrayList<>();

		for (int i = 0; i < iterations; i++) {
			nextGrid = new char[maxY][maxX];
			for (int y = 0; y < maxY; y++) {
				for (int x = 0; x < maxX; x++) {
					nextGrid[y][x] = grid[y][x];

					// An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
					if (grid[y][x] == OPEN && countBordering(grid, x, y, TREE) >= 3) {
						nextGrid[y][x] = TREE;
					}

					// An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
					if (grid[y][x] == TREE && countBordering(grid, x, y, LUMBER) >= 3) {
						nextGrid[y][x] = LUMBER;
					}

					// An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
					if (grid[y][x] == LUMBER && (countBordering(grid, x, y, LUMBER) < 1 || countBordering(grid, x, y, TREE) < 1)) {
						nextGrid[y][x] = OPEN;
					}
				}
			}
			grid = nextGrid;
			int hash = Arrays.deepHashCode(grid);
			if (hashList.contains(hash)) {
				int delta = i - hashList.lastIndexOf(hash);
				iterations = ((iterations - i) % delta);
				i = 0;
				hashList.clear();
			} else {
				hashList.add(hash);
			}
		}
		return count(grid, TREE) * count(grid, LUMBER);
	}

	private int countBordering(char[][] grid, int x, int y, char c) {
		int maxX = grid[0].length;
		int maxY = grid.length;
		int result = 0;
		if (x > 0 && y > 0 && grid[y - 1][x - 1] == c) {
			result++;
		}
		if (x > 0 && grid[y][x - 1] == c) {
			result++;
		}
		if (x > 0 && y < maxY - 1 && grid[y + 1][x - 1] == c) {
			result++;
		}
		if (x < maxX - 1 && y > 0 && grid[y - 1][x + 1] == c) {
			result++;
		}
		if (x < maxX - 1 && grid[y][x + 1] == c) {
			result++;
		}
		if (x < maxX - 1 && y < maxY - 1 && grid[y + 1][x + 1] == c) {
			result++;
		}
		if (y > 0 && grid[y - 1][x] == c) {
			result++;
		}
		if (y < maxY - 1 && grid[y + 1][x] == c) {
			result++;
		}
		return result;
	}

	private int count(char[][] grid, char c) {
		int maxX = grid[0].length;
		int maxY = grid.length;
		int result = 0;
		for (int y = 0; y < maxY; y++) {
			for (int x = 0; x < maxX; x++) {
				if (grid[y][x] == c) {
					result++;
				}
			}
		}
		return result;
	}

}
