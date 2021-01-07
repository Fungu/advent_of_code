import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day08 implements AocSolver {
	public static void main(String[] args) {
		Aoc.runRaw(new Day08());
	}

	@Override
	public void solve(String input) {
		ArrayDeque<Integer> elements = new ArrayDeque<>();
		for (String s : input.split(" ")) {
			elements.add(Integer.parseInt(s));
		}
		Node root = new Node(elements);
		
		System.out.println("Part 1: " + root.calculatePart1());
		System.out.println("Part 2: " + root.calculatePart2());
	}

	class Node {
		ArrayList<Node> children = new ArrayList<>();
		ArrayList<Integer> metadata = new ArrayList<>();
		
		public Node(ArrayDeque<Integer> elements) {
			int childQuantity = elements.pop();
			int metadataQuantity = elements.pop();

			for (int i = 0; i < childQuantity; i++) {
				children.add(new Node(elements));
			}
			for (int i = 0; i < metadataQuantity; i++) {
				metadata.add(elements.pop());
			}
		}
		
		public int calculatePart1() {
			int ret = metadata.stream().mapToInt(Integer::intValue).sum();
			ret += children.stream().map(c -> c.calculatePart1()).mapToInt(Integer::intValue).sum();
			return ret;
		}
		
		public int calculatePart2() {
			int ret = 0;
			if (children.isEmpty()) {
				ret += metadata.stream().mapToInt(Integer::intValue).sum();
			} else {
				for (int meta : metadata) {
					if (meta - 1 < children.size()) {
						ret += children.get(meta - 1).calculatePart2();
					}
				}
			}
			return ret;
		}
	}

}