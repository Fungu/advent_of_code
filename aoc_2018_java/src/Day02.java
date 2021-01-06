import java.util.HashMap;
import java.util.List;

public class Day02 implements AocSolver {
    public static void main(String[] args) {
        Aoc.runLines(new Day02());
    }

    @Override
    public void solve(List<String> inputLines) {
        int nrOfTwo = 0;
        int nrOfThree = 0;
        for (String line : inputLines) {
            HashMap<Character, Long> letters = new HashMap<>();
            for (int ascii = (int) 'a'; ascii <= (int) 'z'; ascii++) {
                char ch = (char) ascii;
                long count = line.chars().filter(stringChar -> stringChar == ch).count();
                letters.put(ch, count);
            }
            if (letters.values().stream().anyMatch(c -> c == 2)) {
                nrOfTwo++;
            } 
            if (letters.values().stream().anyMatch(c -> c == 3)) {
                nrOfThree++;
            }
        }
        int part1 = nrOfTwo * nrOfThree;

        String part2 = null;
        for (String line : inputLines) {
            for (String otherLine : inputLines) {
                if (line == otherLine || line.length() != otherLine.length()) {
                    continue;
                }
                int nrOfDiff = 0;
                int diffIndex = -1;
                for (int i = 0; i < line.length(); i++) {
                    if (line.charAt(i) != otherLine.charAt(i)) {
                        nrOfDiff++;
                        diffIndex = i;
                    }
                }
                if (nrOfDiff == 1) {
                    part2 = line.substring(0, diffIndex) + line.substring(diffIndex + 1);
                }
            }
        }

        System.out.println("Part 1: " + part1);
        System.out.println("Part 2: " + part2);
    }
}