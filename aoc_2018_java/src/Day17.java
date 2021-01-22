import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day17 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day17());
	}

	final char CLAY = '#';
	final char SAND = '.';
	final char FLOW = '|';
	final char STILL = '~';
	final char SOURCE = '+';

	char[][] grid;
	int totalFilled = 0;
	int minY = Integer.MAX_VALUE;
	int sourceX = 500;
	int sourceY = 0;

	@Override
	public void solve(List<String> inputLines) {
		parseInput(inputLines);

		while (flowDown(sourceX, sourceY)) {
		}


		int part2 = 0;
		for (int y = 0; y < grid.length; y++) {
			for (int x = 0; x < grid[0].length; x++) {
				if (grid[y][x] == STILL) {
					part2++;
				}
			}
		}
		
		System.out.println("Part 1: " + totalFilled);
		System.out.println("Part 2: " + part2);
	}
	
	public void parseInput(List<String> inputLines) {
		Pattern pattern = Pattern.compile("(?<firstDimension>x|y)=(?<firstValue>[0-9]*), (?<secondDimension>x|y)=(?<secondValueStart>[0-9]*)\\.\\.(?<secondValueEnd>[0-9]*)");
		String[] firstDimension = new String[inputLines.size()];
		int[] firstValue = new int[inputLines.size()];
		String[] secondDimension = new String[inputLines.size()];
		int[] secondValueStart = new int[inputLines.size()];
		int[] secondValueEnd = new int[inputLines.size()];
		int maxX = Integer.MIN_VALUE;
		int maxY = Integer.MIN_VALUE;
		for (int i = 0; i < inputLines.size(); i++) {
			String line = inputLines.get(i);
			Matcher matcher = pattern.matcher(line);
			matcher.matches();
			firstDimension[i] = matcher.group("firstDimension");
			firstValue[i] = Integer.parseInt(matcher.group("firstValue"));
			secondDimension[i] = matcher.group("secondDimension");
			secondValueStart[i] = Integer.parseInt(matcher.group("secondValueStart"));
			secondValueEnd[i] = Integer.parseInt(matcher.group("secondValueEnd"));
			if (firstDimension[i].equals("x")) {
				maxX = Math.max(maxX, firstValue[i]);
				maxY = Math.max(maxY, secondValueStart[i]);
				maxY = Math.max(maxY, secondValueEnd[i]);
				minY = Math.min(minY, secondValueStart[i]);
				minY = Math.min(minY, secondValueEnd[i]);
			} else {
				maxY = Math.max(maxY, firstValue[i]);
				maxX = Math.max(maxX, secondValueStart[i]);
				maxX = Math.max(maxX, secondValueEnd[i]);
				minY = Math.min(minY, firstValue[i]);
			}
		}
		maxX += 2;
		maxY += 2;
		minY++;
		
		grid = new char[maxY][maxX];
		for (int y = 0; y < grid.length; y++) {
			for (int x = 0; x < grid[0].length; x++) {
				grid[y][x] = '.';
			}
		}
		for (int i = 0; i < inputLines.size(); i++) {
			if (firstDimension[i].equals("x")) {
				int x = firstValue[i];
				int yStart = secondValueStart[i];
				int yEnd = secondValueEnd[i];
				for (int y = yStart; y <= yEnd; y++) {
					grid[y][x] = CLAY;
				}
			} else {
				int y = firstValue[i];
				int xStart = secondValueStart[i];
				int xEnd = secondValueEnd[i];
				for (int x = xStart; x <= xEnd; x++) {
					grid[y][x] = CLAY;
				}
			}
		}
		grid[sourceY][sourceX] = SOURCE;
	}

	private boolean flowDown(int x, int y) {
		boolean keepGoing = false;
		while (isFree(x, y + 1)) {
			y++;
			if (grid[y][x] == SAND && y > minY) {
				totalFilled++;
				keepGoing = true;
			}
			grid[y][x] = FLOW;
			if (y + 1 >= grid.length) {
				break;
			}
		}
		if (y + 1 < grid.length) {
			keepGoing |= flowSideways(x, y);
		}
		return keepGoing;
	}

	private boolean flowSideways(int x, int y) {
		boolean levelStill = true;
		boolean keepGoing = false;

		int leftX = x;
		while (isFree(leftX - 1, y)) {
			leftX--;
			if (isSand(leftX, y)) {
				totalFilled++;
			}
			if (isFree(leftX, y + 1)) {
				levelStill = false;
				keepGoing |= flowDown(leftX, y);
				break;
			}
		}
		int rightX = x;
		while (isFree(rightX + 1, y)) {
			rightX++;
			if (isSand(rightX, y)) {
				totalFilled++;
			}
			if (isFree(rightX, y + 1)) {
				levelStill = false;
				keepGoing |= flowDown(rightX, y);
				break;
			}
		}

		for (int i = leftX; i <= rightX; i++) {
			grid[y][i] = (levelStill ? STILL : FLOW);
			if (levelStill) {
				keepGoing = true;
			}
		}
		return keepGoing;
	}

	private boolean isFree(int x, int y) {
		return !isClay(x, y) && !isStill(x, y);
	}

	private boolean isSand(int x, int y) {
		return grid[y][x] == SAND;
	}

	private boolean isClay(int x, int y) {
		return grid[y][x] == CLAY;
	}

	private boolean isStill(int x, int y) {
		return grid[y][x] == STILL;
	}
}
