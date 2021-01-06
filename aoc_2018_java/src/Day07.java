import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day07 implements AocSolver {
	public static void main(String[] args) {
		Aoc.runLines(new Day07());
	}

	@Override
	public void solve(List<String> inputLines) {
		String part1 = "";
		{
			HashMap<String, List<String>> blockers = parseBlockers(inputLines);
			ArrayList<String> steps = new ArrayList<>(blockers.keySet());
			Collections.sort(steps);
			while (!steps.isEmpty()) {
				for (String key : steps) {
					if (blockers.get(key).isEmpty()) {
						part1 += key;
						for (List<String> blockList : blockers.values()) {
							blockList.remove(key);
						}
						steps.remove(key);
						break;
					}
				}
			}
		}

		int part2 = 0;
		{
			int workerCount = 5;
			HashMap<Integer, String> workerJobs = new HashMap<>();
			HashMap<Integer, Integer> workerTimeLeft = new HashMap<>();
			HashMap<String, List<String>> blockers = parseBlockers(inputLines);
			ArrayList<String> steps = new ArrayList<>(blockers.keySet());
			Collections.sort(steps);
			while (!steps.isEmpty() || workerJobs.values().stream().anyMatch(s -> s != null)) {
				part2++;
				for (int stepIndex = 0; stepIndex < steps.size(); stepIndex++) {
					String key = steps.get(stepIndex);
					if (blockers.get(key).isEmpty()) {
						for (int i = 0; i < workerCount; i++) {
							if (workerJobs.get(i) == null) {
								steps.remove(key);
								stepIndex--;
								workerJobs.put(i, key);
								workerTimeLeft.put(i, 61 + (key.charAt(0) - (int) 'A'));
								break;
							}
						}
					}
				}
				for (int i = 0; i < workerCount; i++) {
					if (workerJobs.get(i) != null) {
						workerTimeLeft.put(i, workerTimeLeft.get(i) - 1);
						if (workerTimeLeft.get(i) == 0) {
							String key = workerJobs.get(i);
							for (List<String> blockList : blockers.values()) {
								blockList.remove(key);
							}
							workerJobs.put(i, null);
						}
					}
				}
			}
		}

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	private HashMap<String, List<String>> parseBlockers(List<String> inputLines) {
		Pattern pattern = Pattern.compile("Step (?<a>[A-Z]) must be finished before step (?<b>[A-Z]) can begin.");
		HashMap<String, List<String>> blockers = new HashMap<>();
		for (String line : inputLines) {
			Matcher matcher = pattern.matcher(line);
			matcher.matches();
			String a = matcher.group("a");
			String b = matcher.group("b");
			if (!blockers.containsKey(a)) {
				blockers.put(a, new ArrayList<>());
			}
			if (!blockers.containsKey(b)) {
				blockers.put(b, new ArrayList<>());
			}
			blockers.get(b).add(a);
		}
		return blockers;
	}

}