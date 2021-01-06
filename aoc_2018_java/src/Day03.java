import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day03 implements AocSolver {
    public static void main(String[] args) {
        Aoc.runLines(new Day03());
    }

    @Override
    public void solve(List<String> inputLines) {
    	HashMap<IntTuple, Integer> fabric = new HashMap<>();
    	HashMap<Integer, Integer> xMap = new HashMap<>();
    	HashMap<Integer, Integer> yMap = new HashMap<>();
    	HashMap<Integer, Integer> widthMap = new HashMap<>();
    	HashMap<Integer, Integer> heightMap = new HashMap<>();
    	Pattern pattern = Pattern.compile("#(?<id>[0-9]+) @ (?<x>[0-9]+),(?<y>[0-9]+): (?<width>[0-9]+)x(?<height>[0-9]+)");
    	for (String line : inputLines) {
	        Matcher matcher = pattern.matcher(line);
	        matcher.matches();
	        int id = Integer.parseInt(matcher.group("id"));
	        int x = Integer.parseInt(matcher.group("x"));
	        int y = Integer.parseInt(matcher.group("y"));
	        int width = Integer.parseInt(matcher.group("width"));
	        int height = Integer.parseInt(matcher.group("height"));
	        xMap.put(id, x);
	        yMap.put(id, y);
	        widthMap.put(id, width);
	        heightMap.put(id, height);
	        for (int dy = 0; dy < height; dy++) {
	        	for (int dx = 0; dx < width; dx++) {
	        		IntTuple pos = new IntTuple(x + dx, y + dy);
	        		if (!fabric.containsKey(pos)) {
	        			fabric.put(pos, 0);
	        		}
	        		fabric.put(pos, fabric.get(pos) + 1);
	        	}
	        }
    	}
    	long part1 = fabric.values().stream().filter(n -> n > 1).count();
    	
    	int part2 = -1;
    	for (int id : xMap.keySet()) {
    		boolean foundOverlap = false;
    		for (int dy = 0; dy < heightMap.get(id); dy++) {
	        	for (int dx = 0; dx < widthMap.get(id); dx++) {
	        		IntTuple pos = new IntTuple(xMap.get(id) + dx, yMap.get(id) + dy);
	        		if (fabric.get(pos) != 1) {
	        			foundOverlap = true;
	        		}
	        	}
	        }
    		if (!foundOverlap) {
    			part2 = id;
    		}
    	}

        System.out.println("Part 1: " + part1);
        System.out.println("Part 2: " + part2);
    }
}