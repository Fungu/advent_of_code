import java.util.List;
import java.util.Set;
import java.util.HashSet;

public class Day01 implements AocSolver {
    public static void main(String[] args) {
        Aoc.runLines(new Day01());
    }

    public void solve(List<String> inputLines) {
        int part1 = 0;
        for (String line : inputLines) {
            part1 += Integer.valueOf(line);
        }

        Integer part2 = null;
        int frequency = 0;
        Set<Integer> seen = new HashSet<>();
        while (part2 == null) {
            for (String line : inputLines) {
                frequency += Integer.valueOf(line);
                if (seen.contains(frequency)) {
                    part2 = frequency;
                    break;
                }
                seen.add(frequency);
            }
        }

        System.out.println("Part 1: " + part1);
        System.out.println("Part 2: " + part2);
    }
}