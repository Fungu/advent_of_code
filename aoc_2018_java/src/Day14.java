import java.util.ArrayList;
import java.util.stream.Collectors;

public class Day14 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runRaw(new Day14());
	}

	@Override
	public void solve(String input) {
		int part1Target = Integer.parseInt(input);
		ArrayList<Integer> part2Target = new ArrayList<>();
		for (char c : input.toCharArray()) {
			part2Target.add(c - '0');
		}
		
		ArrayList<Integer> recipes = new ArrayList<>();
		recipes.add(3);
		recipes.add(7);
		int[] indexes = {0, 1};
		
		String part1 = null;
		Integer part2 = null;
		while (part1 == null || part2 == null) {
			int newRecipe = recipes.get(indexes[0]) + recipes.get(indexes[1]);
			if (newRecipe >= 10) {
				recipes.add(Math.floorDiv(newRecipe, 10));
				part1 = checkPart1(part1, recipes, part1Target);
				part2 = checkPart2(part2, recipes, part2Target);
			}
			recipes.add(newRecipe % 10);
			part1 = checkPart1(part1, recipes, part1Target);
			part2 = checkPart2(part2, recipes, part2Target);
			for (int a = 0; a < 2; a++) {
				indexes[a] += recipes.get(indexes[a]) + 1;
				indexes[a] = Aoc.wrap(indexes[a], 0, recipes.size());
			}
		}
		
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
	
	private String checkPart1(String part1, ArrayList<Integer> recipes, int part1Target) {
		if (part1 == null && recipes.size() >= part1Target + 10) {
			return recipes.subList(part1Target, recipes.size()).stream().map(r -> r + "").collect(Collectors.joining());
		}
		return part1;
	}
	
	private Integer checkPart2(Integer part2, ArrayList<Integer> recipes, ArrayList<Integer> target) {
		if (part2 == null && recipes.size() > target.size() && recipes.subList(recipes.size() - target.size() - 1, recipes.size() - 1).equals(target)) {
			return recipes.size() - target.size() - 1;
		}
		return part2;
	}
}
