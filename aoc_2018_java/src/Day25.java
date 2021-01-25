import java.util.Arrays;
import java.util.List;

public class Day25 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day25());
	}

	@Override
	public void solve(List<String> inputLines) {
		int[] xPoints = new int[inputLines.size()];
		int[] yPoints = new int[inputLines.size()];
		int[] zPoints = new int[inputLines.size()];
		int[] tPoints = new int[inputLines.size()];
		Integer[] constellation = new Integer[inputLines.size()];

		for (int i = 0; i < inputLines.size(); i++) {
			String[] a = inputLines.get(i).split(",");
			xPoints[i] = Integer.parseInt(a[0]);
			yPoints[i] = Integer.parseInt(a[1]);
			zPoints[i] = Integer.parseInt(a[2]);
			tPoints[i] = Integer.parseInt(a[3]);
			constellation[i] = null;
		}

		Integer currentConstellation = 0;
		while (Arrays.stream(constellation).anyMatch(c -> c == null)) {
			currentConstellation++;
			boolean constellationInitialized = false;
			boolean stateChanged = true;
			while (stateChanged) {
				stateChanged = false;
				for (int i = 0; i < inputLines.size(); i++) {
					if (!constellationInitialized && constellation[i] == null) {
						constellation[i] = currentConstellation;
						constellationInitialized = true;
					}
					if (constellation[i] == currentConstellation) {
						for (int j = 0; j < inputLines.size(); j++) {
							if (constellation[j] == null) {
								int distance = Math.abs(xPoints[i] - xPoints[j]) + Math.abs(yPoints[i] - yPoints[j]) + Math.abs(zPoints[i] - zPoints[j]) + Math.abs(tPoints[i] - tPoints[j]);
								if (distance <= 3) {
									constellation[j] = currentConstellation;
									stateChanged = true;
								}
							}
						}
					}
				}
			}
		}

		System.out.println("Part 1: " + currentConstellation);
		System.out.println("Part 2: Done!");
	}

}
