import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class Day12 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day12());
	}

	class Operation {
		boolean[] pattern = new boolean[5];
		boolean result;

		public Operation(String line) {
			pattern[0] = line.charAt(0) == '#';
			pattern[1] = line.charAt(1) == '#';
			pattern[2] = line.charAt(2) == '#';
			pattern[3] = line.charAt(3) == '#';
			pattern[4] = line.charAt(4) == '#';
			result = line.split("=> ")[1].equals("#");
		}

		public boolean matches(HashMap<Integer, Boolean> states, int index) {
			return states.getOrDefault(index - 2, false) == pattern[0]
					&& states.getOrDefault(index - 1, false) == pattern[1]
					&& states.getOrDefault(index - 0, false) == pattern[2]
					&& states.getOrDefault(index + 1, false) == pattern[3]
					&& states.getOrDefault(index + 2, false) == pattern[4];
		}

		public boolean getResult() {
			return result;
		}
	}
	
	@Override
	public void solve(List<String> inputLines) {
		String initialState = inputLines.get(0).replace("initial state: ", "");
		List<Operation> operations = new ArrayList<>();
		for (String line : inputLines.subList(2, inputLines.size())) {
			operations.add(new Operation(line));
		}

		HashMap<Integer, Boolean> states = new HashMap<>();
		for (int i = 0; i < initialState.length(); i++) {
			states.put(i, initialState.charAt(i) == '#');
		}

		Integer part1 = null;
		Long part2 = null;
		ArrayList<String> prevStates = new ArrayList<>();
		ArrayList<Integer> prevScores = new ArrayList<>();
		for (int iteration = 0; part1 == null || part2 == null; iteration++) {
			int min = states.entrySet().stream().filter(e -> e.getValue()).map(e -> e.getKey()).min((a, b) -> a.intValue() - b.intValue()).get();
			int max = states.entrySet().stream().filter(e -> e.getValue()).map(e -> e.getKey()).max((a, b) -> a.intValue() - b.intValue()).get();
			int score = states.entrySet().stream().filter(e -> e.getValue()).map(e -> e.getKey()).collect(Collectors.summingInt(Integer::intValue));
			prevScores.add(score);
			String stateString = "";
			for (int i = min; i <= max; i++) {
				stateString += states.getOrDefault(i, false) ? "#" : ".";
			}
			if (prevStates.contains(stateString)) {
				int prevIteration = prevStates.indexOf(stateString);
				int prevScore = prevScores.get(prevIteration);
				int increment = (score - prevScore) / (iteration - prevIteration);
				long iterationsLeft = 50000000000l - iteration;
				part2 = score + increment * iterationsLeft;
			}
			prevStates.add(stateString);
			
			if (iteration == 20) {
				part1 = score;
			}
			
			HashMap<Integer, Boolean> nextStates = new HashMap<>();
			for (int i = min - 2; i <= max + 2; i++) {
				for (Operation operation : operations) {
					if (operation.matches(states, i)) {
						nextStates.put(i, operation.getResult());
					}
				}
			}
			states = nextStates;
		}
		
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
}
