import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day23 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day23());
	}

	class Nanobot {
		long x, y, z, r;

		public Nanobot(long x, long y, long z, long r) {
			this.x = x;
			this.y = y;
			this.z = z;
			this.r = r;
		}

		public boolean inRange(Nanobot other) {
			long distance = Math.abs(x - other.x) + Math.abs(y - other.y) + Math.abs(z - other.z);
			return distance <= r;
		}

		public boolean inRange(long x, long y, long z) {
			long distance = Math.abs(x - this.x) + Math.abs(y - this.y) + Math.abs(z - this.z);
			return distance <= r;
		}
	}

	@Override
	public void solve(List<String> inputLines) {
		Pattern pattern = Pattern.compile("pos=<(?<x>-?[0-9]*),(?<y>-?[0-9]*),(?<z>-?[0-9]*)>, r=(?<r>[0-9]*)");
		ArrayList<Nanobot> nanoBots = new ArrayList<>();
		for (String line : inputLines) {
			Matcher matcher = pattern.matcher(line);
			matcher.matches();
			long x = Integer.parseInt(matcher.group("x"));
			long y = Integer.parseInt(matcher.group("y"));
			long z = Integer.parseInt(matcher.group("z"));
			long r = Integer.parseInt(matcher.group("r"));
			nanoBots.add(new Nanobot(x, y, z, r));
		}

		Nanobot bestBot = nanoBots.stream().max((a, b) -> (int) (a.r - b.r)).get();
		long part1 = nanoBots.stream().filter(n -> bestBot.inRange(n)).count();

		long xMin = nanoBots.stream().map(n -> n.x).min((a, b) -> (int) (a - b)).get();
		long yMin = nanoBots.stream().map(n -> n.y).min((a, b) -> (int) (a - b)).get();
		long zMin = nanoBots.stream().map(n -> n.z).min((a, b) -> (int) (a - b)).get();
		long xMax = nanoBots.stream().map(n -> n.x).max((a, b) -> (int) (a - b)).get();
		long yMax = nanoBots.stream().map(n -> n.y).max((a, b) -> (int) (a - b)).get();
		long zMax = nanoBots.stream().map(n -> n.z).max((a, b) -> (int) (a - b)).get();
		long cellCount = 2;
		long cellSize = (long) Math.ceil(Math.max(xMax - xMin, Math.max(yMax - yMin, zMax - zMin)) / cellCount);
		long part2 = search(nanoBots, cellSize, cellCount, xMin, yMin, zMin);

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	private long search(ArrayList<Nanobot> nanoBots, long cellSize, long cellCount, long xMin, long yMin, long zMin) {
		if (cellSize < 1) {
			cellSize = 1;
		}
		long score = 0;
		long xBest = 0;
		long yBest = 0;
		long zBest = 0;
		for (long z = zMin - cellSize; z <= zMin + cellSize * cellCount + cellSize; z += cellSize) {
			for (long y = yMin - cellSize; y <= yMin + cellSize * cellCount + cellSize; y += cellSize) {
				for (long x = xMin - cellSize; x <= xMin + cellSize * cellCount + cellSize; x += cellSize) {
					long newScore = 0;
					for (Nanobot nanoBot : nanoBots) {
						if (nanoBot.inRange(x, y, z)) {
							newScore++;
						}
					}
					if (newScore > score) {
						score = newScore;
						xBest = x;
						yBest = y;
						zBest = z;
					} else if (newScore == score && (Math.abs(x) + Math.abs(y) + Math.abs(z)) < (Math.abs(xBest) + Math.abs(yBest) + Math.abs(zBest))) {
						xBest = x;
						yBest = y;
						zBest = z;
					}
				}
			}
		}
		if (cellSize == 1) {
			return Math.abs(xBest) + Math.abs(yBest) + Math.abs(zBest);
		} else {
			return search(nanoBots, (int) Math.ceil(cellSize / cellCount), cellCount, xBest, yBest, zBest);
		}
	}

}
