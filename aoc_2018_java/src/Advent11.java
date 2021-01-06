package advent2018;

public class Advent11 {

	public static void main(String[] args) {
		new Advent11();
	}

	private int getFuelValue(int x, int y, int serial) {
//		Find the fuel cell's rack ID, which is its X coordinate plus 10.
		int result = x + 10;

//		Begin with a power level of the rack ID times the Y coordinate.
		result *= y;

//		Increase the power level by the value of the grid serial number (your puzzle input).
		result += serial;

//		Set the power level to itself multiplied by the rack ID.
		result *= (x + 10);

//		Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
		result = result % 1000;
		result = (int) Math.floor((double)result / 100.0);

//		Subtract 5 from the power level.
		result -= 5;

		return result;
	}

	public Advent11() {
//		Fuel cell at  122,79, grid serial number 57: power level -5.
		if (getFuelValue(122, 79, 57) != -5) {
			System.err.println("Oops 1");
		}
		
//		Fuel cell at 217,196, grid serial number 39: power level  0.
		if (getFuelValue(217, 196, 39) != 0) {
			System.err.println("Oops 2");
		}
		
//		Fuel cell at 101,153, grid serial number 71: power level  4.
		if (getFuelValue(101, 153, 71) != 4) {
			System.err.println("Oops 2");
		}
		
		int serial = 2187;
		
//		For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these fuel cells appear in the middle of this 5x5 region:
//		serial = 18;
		
//		For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle of this region:
//		serial = 42;
		
//		For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of 90,269, so its identifier is 90,269,16.
//		serial = 18;
		
//		For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of 232,251, so its identifier is 232,251,12.
//		serial = 42;
		
		int bestFuel = 0;
		int bestX = 0;
		int bestY = 0;
		int bestSize = 0;
		long startTime = System.currentTimeMillis();

		int grid[][] = new int[300][300];
		for (int x = 1; x <= 300; x++) {
			for (int y = 1; y <= 300; y++) {
				grid[x - 1][y - 1] = getFuelValue(x, y, serial);
			}
		}
		
		for (int x = 1; x <= 300; x++) {
			for (int y = 1; y <= 300; y++) {
				int maxSize = 300 - Math.max(x, y);
				
				int fuel = 0;
				for (int size = 1; size <= maxSize; size++) {
					for (int xx = x; xx < x + size; xx++) {
						fuel += grid[xx - 1][size - 1 + y - 1];
					}
					for (int yy = y; yy < y + size - 1; yy++) {
						fuel += grid[size - 1 + x - 1][yy - 1];
					}
					
					if (fuel > bestFuel) {
						bestX = x;
						bestY = y;
						bestFuel = fuel;
						bestSize = size;
					}
				}

			}
		}
		
		System.out.println("time: " + (System.currentTimeMillis() - startTime) + "ms");
		System.out.println(bestX + "," + bestY + "," + bestSize + ": " + bestFuel);
	}
}
