import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map.Entry;

public class Day06 implements AocSolver {
	public static void main(String[] args) {
		Aoc.runLines(new Day06());
	}

	@Override
	public void solve(List<String> inputLines) {
		HashMap<IntTuple, Integer> grid = new HashMap<>();
		HashMap<Integer, ArrayList<IntTuple>> openSets = new HashMap<>();
		int[] areaSizes = new int[inputLines.size()];
		ArrayList<Integer> xArray = new ArrayList<>();
		ArrayList<Integer> yArray = new ArrayList<>();
		for (int i = 0; i < inputLines.size(); i++) {
			String line = inputLines.get(i);
			int x = Integer.parseInt(line.split(",")[0].trim());
			int y = Integer.parseInt(line.split(",")[1].trim());
			ArrayList<IntTuple> set = new ArrayList<>();
			set.add(new IntTuple(x, y));
			openSets.put(i, set);
			xArray.add(x);
			yArray.add(y);
		}
		
		int[] dirX = {1, 0, -1, 0};
		int[] dirY = {0, 1, 0, -1};
		
		int iterations = Math.max(Collections.max(xArray) - Collections.min(xArray), Collections.max(yArray) - Collections.min(yArray));
		iterations = (int) Math.ceil(iterations / 2);
		for (int i = 0; i < iterations; i++) {
			HashMap<Integer, ArrayList<IntTuple>> nextOpenSets = new HashMap<>();
			for (Entry<Integer, ArrayList<IntTuple>> entry : openSets.entrySet()) {
				ArrayList<IntTuple> openSet = entry.getValue();
				ArrayList<IntTuple> nextOpenSet = new ArrayList<>();
				for (IntTuple pos : openSet) {
					boolean inOtherOpen = openSets.entrySet().stream().anyMatch(e -> e.getKey() != entry.getKey() && e.getValue().contains(pos));
					// Check if the pos was added to another open set in the last iteration
					if (grid.containsKey(pos)) {
						continue;
					}
					if (inOtherOpen) {
						grid.put(pos, -1);
						continue;
					}
					grid.put(pos, entry.getKey());
					areaSizes[entry.getKey()]++;
					for (int iDir = 0; iDir < dirX.length; iDir++) {
						IntTuple otherPos = new IntTuple(pos.values[0] + dirX[iDir], pos.values[1] + dirY[iDir]);
						if (!grid.containsKey(otherPos)) {
							nextOpenSet.add(otherPos);
						}
					}
				}
				nextOpenSets.put(entry.getKey(), nextOpenSet);
			}
			openSets = nextOpenSets;
		}
		int part1 = areaSizes[openSets.entrySet().stream().max((a, b) -> (a.getValue().isEmpty() ? areaSizes[a.getKey()] : 0) - (b.getValue().isEmpty() ? areaSizes[b.getKey()] : 0)).get().getKey()];
		
		int maxDistance = 10000;
		ArrayDeque<IntTuple> openSet = new ArrayDeque<>();
		ArrayDeque<IntTuple> closedSet = new ArrayDeque<>();
		for (int i = 0; i < xArray.size(); i++) {
			IntTuple pos = new IntTuple(xArray.get(i), yArray.get(i));
			if (getDistance(pos, xArray, yArray) < maxDistance) {
				openSet.add(new IntTuple(xArray.get(i), yArray.get(i)));
				break;
			}
		}
		while (!openSet.isEmpty()) {
			IntTuple pos = openSet.pop();
			closedSet.add(pos);
			for (int iDir = 0; iDir < dirX.length; iDir++) {
				IntTuple otherPos = new IntTuple(pos.values[0] + dirX[iDir], pos.values[1] + dirY[iDir]);
				if (!closedSet.contains(otherPos) && !openSet.contains(otherPos) && getDistance(otherPos, xArray, yArray) < maxDistance) {
					openSet.add(otherPos);
				}
			}
		}
		int part2 = closedSet.size();
		
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
	
	private int getDistance(IntTuple pos, ArrayList<Integer> xArray, ArrayList<Integer> yArray) {
		int distance = 0;
		for (int i = 0; i < xArray.size(); i++) {
			distance += Math.abs(pos.values[0] - xArray.get(i));
			distance += Math.abs(pos.values[1] - yArray.get(i));
		}
		return distance;
	}
}