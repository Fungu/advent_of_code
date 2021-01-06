package advent2018;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

public class Advent18 {

	public static void main(String[] args) throws Exception {
		boolean debug = false;

		debug = true;

		new Advent18(readFile("input18"), debug);
//		new Advent18(readFile("input18_example"), debug);
	}

	private static String readFile(String fileName) throws IOException {
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}

	final char OPEN = '.';
	final char TREE = '|';
	final char LUMBER = '#';

	int maxX = Integer.MIN_VALUE;
	int maxY = Integer.MIN_VALUE;
	char[][] grid;

	public Advent18(String input, boolean debug) throws Exception {
		setup(input);

		execute();
		teardown();
	}

	public void setup(String input) {
		String[] inputArray = input.split("\r\n");
		maxX = inputArray[0].length();
		maxY = inputArray.length;
		grid = new char[maxX][maxY];

		for (int x = 0; x < maxX; x++) {
			for (int y = 0; y < maxY; y++) {
				grid[x][y] = inputArray[y].charAt(x);
			}
		}
	}

	public void execute() throws Exception {
		long startTime = System.currentTimeMillis();
		int iterations = 10;
		iterations = 1000;
		char[][] nextGrid;

		for (int i = 0; i < iterations; i++) {
//			System.out.println(i);
//			print();
			nextGrid = new char[maxX][maxY];
			for (int x = 0; x < maxX; x++) {
				for (int y = 0; y < maxY; y++) {
					nextGrid[x][y] = grid[x][y];

					// An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
					if (grid[x][y] == OPEN && countBordering(x, y, TREE) >= 3) {
						nextGrid[x][y] = TREE;
					}

					// An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
					if (grid[x][y] == TREE && countBordering(x, y, LUMBER) >= 3) {
						nextGrid[x][y] = LUMBER;
					}

					//	An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.
					if (grid[x][y] == LUMBER && (countBordering(x, y, LUMBER) < 1 || countBordering(x, y, TREE) < 1)) {
						nextGrid[x][y] = OPEN;
					}
				}
			}
			grid = nextGrid;
			System.out.println("Iteration: " + i + ", Score: " + (count(TREE) * count(LUMBER)));
		}
		System.out.println(iterations);
		print();

		System.out.println("Time: " + (System.currentTimeMillis() - startTime) + "ms");
	}

	private int countBordering(int x, int y, char c) {
		int result = 0;
		if (x > 0 && y > 0 && grid[x - 1][y - 1] == c) {
			result++;
		}
		if (x > 0 && grid[x - 1][y] == c) {
			result++;
		}
		if (x > 0 && y < maxY - 1 && grid[x - 1][y + 1] == c) {
			result++;
		}
		if (x < maxX - 1 && y > 0 && grid[x + 1][y - 1] == c) {
			result++;
		}
		if (x < maxX - 1 && grid[x + 1][y] == c) {
			result++;
		}
		if (x < maxX - 1 && y < maxY - 1 && grid[x + 1][y + 1] == c) {
			result++;
		}
		if (y > 0 && grid[x][y - 1] == c) {
			result++;
		}
		if (y < maxY - 1 && grid[x][y + 1] == c) {
			result++;
		}
		return result;
	}
	
	private int count(char c) {
		int result = 0;
		for (int x = 0; x < maxX; x++) {
			for (int y = 0; y < maxY; y++) {
				if (grid[x][y] == c) {
					result++;
				}
			}
		}
		return result;
	}

	private void print() {
		if (maxY != 0)
			return;
		for (int y = 0; y < maxY; y++) {
			for (int x = 0; x < maxX; x++) {
				System.out.print(grid[x][y]);
			}
			System.out.println();
		}
		System.out.println();

//		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\output\\Advent_17_output.txt");
//		try {
//			FileWriter fw = new FileWriter(file);
//			for (int y = 0; y < maxY; y++) {
//				for (int x = minX; x < maxX; x++) {
//					fw.write(grid[x - minX][y]);
//				}
//				fw.write("\r\n");
//			}
//			fw.close();
//		} catch (IOException e) {
//			e.printStackTrace();
//		}
	}

	public void teardown() {
	}

}
