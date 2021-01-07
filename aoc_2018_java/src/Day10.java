import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day10 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day10());
	}

	class PointOfLight {
		int x, y;
		int velX, velY;
		
		Pattern regex = Pattern.compile("position=< *(?<x>-?[0-9]+), *(?<y>-?[0-9]+)> *velocity=< *(?<velX>-?[0-9]+), *(?<velY>-?[0-9]+)>");
		PointOfLight(String line) {
			Matcher matcher = regex.matcher(line);
			matcher.matches();
			x = Integer.parseInt(matcher.group("x"));
			y = Integer.parseInt(matcher.group("y"));
			velX = Integer.parseInt(matcher.group("velX"));
			velY = Integer.parseInt(matcher.group("velY"));
		}
	}
	
	class Bounds {
		int maxX, minX, maxY, minY, size;
		Bounds(List<PointOfLight> pointList) {
			minX = pointList.stream().min((a, b) -> (a.x - b.x)).get().x;
			maxX = pointList.stream().max((a, b) -> (a.x - b.x)).get().x;
			minY = pointList.stream().min((a, b) -> (a.y - b.y)).get().y;
			maxY = pointList.stream().max((a, b) -> (a.y - b.y)).get().y;
			size = maxX - minX + maxY - minY;
		}
	}

	@Override
	public void solve(List<String> inputLines) {
		List<PointOfLight> pointList = new ArrayList<>();
		for (String line : inputLines) {
			pointList.add(new PointOfLight(line));
		}
		
		String part1 = "";
		int prevSize = Integer.MAX_VALUE;
		int iterations = 0;
		for (; ; iterations++) {
			for (PointOfLight n : pointList) {
				n.x += n.velX;
				n.y += n.velY;
			}

			Bounds bounds = new Bounds(pointList);
			if (bounds.size > prevSize) {
				for (PointOfLight n : pointList) {
					n.x -= n.velX;
					n.y -= n.velY;
				}
				bounds = new Bounds(pointList);
				for (int y = bounds.minY; y <= bounds.maxY; y++) {
					part1 += System.lineSeparator();
					for (int x = bounds.minX; x <= bounds.maxX; x++) {
						int X = x;
						int Y = y;
						if (pointList.stream().anyMatch(n -> n.x == X && n.y == Y)) {
							part1 += "#";
						} else {
							part1 += " ";
						}
					}
				}
				break;
			}
			prevSize = bounds.size;
		}
		
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + iterations);
	}
}
