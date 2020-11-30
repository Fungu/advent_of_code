package advent2018;

import java.util.ArrayList;
import java.util.List;

public class Advent12 {

	public static void main(String[] args) {
		new Advent12();
	}

//	initial state: #..#.#..##......###...###
//
//	...## => #
//	..#.. => #
//	.#... => #
//	.#.#. => #
//	.#.## => #
//	.##.. => #
//	.#### => #
//	#.#.# => #
//	#.### => #
//	##.#. => #
//	##.## => #
//	###.. => #
//	###.# => #
//	####. => #

	class Operation {
		boolean[] input = new boolean[5];
		boolean result;

		public Operation(String inputString) {
			input[0] = inputString.charAt(0) == '#';
			input[1] = inputString.charAt(1) == '#';
			input[2] = inputString.charAt(2) == '#';
			input[3] = inputString.charAt(3) == '#';
			input[4] = inputString.charAt(4) == '#';
			result = inputString.split("=> ")[1].equals("#");
		}

		public boolean matches(boolean[] states, int index) {
			return states[index - 2] == input[0] && states[index - 1] == input[1] && states[index - 0] == input[2]
					&& states[index + 1] == input[3] && states[index + 2] == input[4];
		}

		public boolean getResult() {
			return result;
		}
	}

	public Advent12() {
		String initialState = "#.#.#...#..##..###.##.#...#.##.#....#..#.#....##.#.##...###.#...#######.....##.###.####.#....#.#..##";
		String operationString = "#...# => #\r\n" + 
				"....# => .\r\n" + 
				"##..# => #\r\n" + 
				".#.## => #\r\n" + 
				"##.## => .\r\n" + 
				"###.# => #\r\n" + 
				"..... => .\r\n" + 
				"...#. => .\r\n" + 
				".#.#. => #\r\n" + 
				"#.##. => #\r\n" + 
				"..#.# => #\r\n" + 
				".#... => #\r\n" + 
				"#.#.. => .\r\n" + 
				"##.#. => .\r\n" + 
				".##.. => #\r\n" + 
				"#..#. => .\r\n" + 
				".###. => .\r\n" + 
				"..#.. => .\r\n" + 
				"#.### => .\r\n" + 
				"..##. => .\r\n" + 
				".#..# => #\r\n" + 
				".##.# => .\r\n" + 
				".#### => .\r\n" + 
				"...## => #\r\n" + 
				"#.#.# => #\r\n" + 
				"..### => .\r\n" + 
				"#..## => .\r\n" + 
				"####. => #\r\n" + 
				"##### => .\r\n" + 
				"###.. => #\r\n" + 
				"##... => #\r\n" + 
				"#.... => .";
		
//		String initialState = "#..#.#..##......###...###";
//		String operationString = "...## => #\r\n" + 
//				"..#.. => #\r\n" + 
//				".#... => #\r\n" + 
//				".#.#. => #\r\n" + 
//				".#.## => #\r\n" + 
//				".##.. => #\r\n" + 
//				".#### => #\r\n" + 
//				"#.#.# => #\r\n" + 
//				"#.### => #\r\n" + 
//				"##.#. => #\r\n" + 
//				"##.## => #\r\n" + 
//				"###.. => #\r\n" + 
//				"###.# => #\r\n" + 
//				"####. => #";

		List<Operation> operations = new ArrayList<>();
		for (String s : operationString.split("\r\n")) {
			operations.add(new Operation(s));
		}

		final int paddingA = 10;
		final int paddingB = 220;
		boolean[] states = new boolean[paddingA + initialState.length() + paddingB];
		for (int i = 0; i < initialState.length(); i++) {
			states[i + paddingA] = initialState.charAt(i) == '#';
		}

//		long iterations = 50000000000;
		int iterations = 200;
		for (int iteration = 0; iteration < iterations; iteration++) {
			int sum = 0;
			int amount = 0;
			System.out.print((iteration < 10 ? " " : "") + iteration + ": ");
			for (int i = 0; i < states.length; i++) {
				System.out.print(states[i] ? "#" : ".");
				if (states[i]) {
					sum += (i - paddingA);
					amount++;
				}
			}
			System.out.println(" " + sum + " " + amount);
			
			boolean[] nextStates = new boolean[paddingA + initialState.length() + paddingB];
			for (int i = 2; i < states.length - 2; i++) {
				for (Operation operation : operations) {
					if (operation.matches(states, i)) {
						nextStates[i] = operation.getResult();
					}
				}
			}
			for (int i = 0; i < states.length; i++) {
				states[i] = nextStates[i];
			}
			
		}
		
		int result = 0;
		System.out.print(iterations + ": ");
		for (int i = 0; i < states.length; i++) {
			System.out.print(states[i] ? "#" : ".");
			if (states[i]) {
				result += (i - paddingA);
			}
		}
		System.out.println(" " + result);
	}
}
