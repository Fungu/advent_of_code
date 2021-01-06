public class Day05 implements AocSolver {
	public static void main(String[] args) {
		Aoc.runRaw(new Day05());
	}

	@Override
	public void solve(String input) {
		int part1 = react(input).length();
		
		Integer bestReaction = null;
		for (int ascii = (int) 'a'; ascii <= (int) 'z'; ascii++) {
			String c = "" + (char) ascii;
			String polymer = input;
			polymer = polymer.replace(c, "");
			polymer = polymer.replace(c.toUpperCase(), "");
			polymer = react(polymer);
			if (bestReaction == null || polymer.length() < bestReaction) {
				bestReaction = polymer.length();
			}
		}
		int part2 = bestReaction;

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
	
	private String react(String polymers) {
		int size = 0;
		while (size != polymers.length()) {
			size = polymers.length();
			for (int ascii = (int) 'a'; ascii <= (int) 'z'; ascii++) {
				String c = "" + (char) ascii;
				polymers = polymers.replace(c + c.toUpperCase(), "");
				polymers = polymers.replace(c.toUpperCase() + c, "");
			}
		}
		return polymers.trim();
	}
}