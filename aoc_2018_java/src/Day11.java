
public class Day11 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runRaw(new Day11());
	}

	@Override
	public void solve(String input) {
		int serial = Integer.parseInt(input);

		int bestFuel = 0;
		int bestX = 0;
		int bestY = 0;
		int bestSize = 0;

		int grid[][] = new int[300][300];
		for (int x = 0; x < 300; x++) {
			for (int y = 0; y < 300; y++) {
				grid[x][y] = getFuelValue(x + 1, y + 1, serial);
			}
		}

		for (int x = 0; x < 300 - 2; x++) {
			for (int y = 0; y < 300 - 2; y++) {
				int fuel = 0;
				for (int xx = 0; xx < 3; xx++) {
					for (int yy = 0; yy < 3; yy++) {
						fuel += grid[x + xx][y + yy];
					}
				}

				if (fuel > bestFuel) {
					bestX = x + 1;
					bestY = y + 1;
					bestFuel = fuel;
				}
			}
		}
		String part1 = bestX + "," + bestY;

		bestFuel = 0;
		bestX = 0;
		bestY = 0;
		bestSize = 0;
		for (int x = 0; x < 300; x++) {
			for (int y = 0; y < 300; y++) {
				int maxSize = 300 - Math.max(x, y);

				int fuel = 0;
				for (int size = 1; size <= maxSize; size++) {
					for (int xx = 0; xx < size; xx++) {
						fuel += grid[x + xx][size - 1 + y];
					}
					for (int yy = 0; yy < size - 1; yy++) {
						fuel += grid[size - 1 + x][y + yy];
					}

					if (fuel > bestFuel) {
						bestX = x + 1;
						bestY = y + 1;
						bestFuel = fuel;
						bestSize = size;
					}
				}
			}
		}
		String part2 = bestX + "," + bestY + "," + bestSize;

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	private int getFuelValue(int x, int y, int serial) {
		// Find the fuel cell's rack ID, which is its X coordinate plus 10.
		int result = x + 10;

		// Begin with a power level of the rack ID times the Y coordinate.
		result *= y;

		// Increase the power level by the value of the grid serial number (your puzzle input).
		result += serial;

		// Set the power level to itself multiplied by the rack ID.
		result *= (x + 10);

		// Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers
		// with no hundreds digit become 0).
		result = result % 1000;
		result = (int) Math.floor((double) result / 100.0);

		// Subtract 5 from the power level.
		result -= 5;

		return result;
	}
}
