import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class Day16 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runRaw(new Day16());
	}

	class Instruction {
		public final int opcode;
		public final int A;
		public final int B;
		public final int C;

		public Instruction(Instruction other) {
			this.opcode = other.opcode;
			this.A = other.A;
			this.B = other.B;
			this.C = other.C;
		}

		public Instruction(String inputLine) {
			opcode = Integer.parseInt(inputLine.split(" ")[0]);
			A = Integer.parseInt(inputLine.split(" ")[1]);
			B = Integer.parseInt(inputLine.split(" ")[2]);
			C = Integer.parseInt(inputLine.split(" ")[3]);
		}
	}

	@Override
	public void solve(String input) {
		String[] splitInput = input.split(System.lineSeparator() + System.lineSeparator() + System.lineSeparator() + System.lineSeparator());
		String input1 = splitInput[0];
		String input2 = splitInput[1];
		Map<String, Predicate<?>> instructionsName = populateInstructions();
		Map<Integer, Predicate<?>> instructionsId = new HashMap<>();
		Map<String, Set<Integer>> possibleMatches = new HashMap<>();

		int result = 0;
		String[] inputArray = input1.split(System.lineSeparator());
		for (int i = 0; i < inputArray.length; i += 4) {
			String beforeString = inputArray[i].replace("Before: ", "").replace("[", "").replace("]", "").trim();
			Instruction instruction = new Instruction(inputArray[i + 1]);
			String afterString = inputArray[i + 2].replace("After: ", "").replace("[", "").replace("]", "").trim();

			ArrayList<Integer> after = stringToList(afterString);
			int possibleInstructions = 0;
			for (Entry<String, Predicate<?>> entry : instructionsName.entrySet()) {
				Predicate<?> predicate = entry.getValue();
				ArrayList<Integer> before = stringToList(beforeString);
				predicate.apply(instruction, before);
				if (before.equals(after)) {
					possibleInstructions++;

					String name = entry.getKey();
					if (possibleMatches.containsKey(name) == false) {
						possibleMatches.put(name, new HashSet<Integer>());
					}
					possibleMatches.get(name).add(instruction.opcode);
				}
			}
			if (possibleInstructions >= 3) {
				result++;
			}
		}
		
		while (possibleMatches.values().stream().anyMatch(v -> v.size() > 1)) {
			for (Entry<String, Set<Integer>> entry : possibleMatches.entrySet()) {
				if (entry.getValue().size() == 1) {
					Integer solvedValue = entry.getValue().stream().findFirst().get();
					for (Entry<String, Set<Integer>> otherEntry : possibleMatches.entrySet()) {
						if (otherEntry.getKey().equals(entry.getKey())) {
							continue;
						}
						otherEntry.getValue().remove(solvedValue);
					}
				}
			}
		}
		
		for (Entry<String, Set<Integer>> entry : possibleMatches.entrySet()) {
			instructionsId.put(entry.getValue().stream().findFirst().get(), instructionsName.get(entry.getKey()));
		}

		String[] inputArray2 = input2.split(System.lineSeparator());
		ArrayList<Integer> registers = new ArrayList<>();
		registers.add(0);
		registers.add(0);
		registers.add(0);
		registers.add(0);
		for (String s : inputArray2) {
			Instruction instruction = new Instruction(s);
			instructionsId.get(instruction.opcode).apply(instruction, registers);
		}

		System.out.println("Part 1: " + result);
		System.out.println("Part 2: " + registers.get(0));
	}
	
	private ArrayList<Integer> stringToList(String s) {
		ArrayList<Integer> result = new ArrayList<>();
		result.add(Integer.parseInt(s.split(", ")[0]));
		result.add(Integer.parseInt(s.split(", ")[1]));
		result.add(Integer.parseInt(s.split(", ")[2]));
		result.add(Integer.parseInt(s.split(", ")[3]));
		return result;
	}

	interface Predicate<T> {
		void apply(Instruction instruction, ArrayList<Integer> registers);
	}

	private Map<String, Predicate<?>> populateInstructions() {
		Map<String, Predicate<?>> instructionsName = new HashMap<>();

		// Addition:
		// addr (add register) stores into register C the result of adding register A and register B.
		instructionsName.put("addr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) + registers.get(instruction.B)));
		// addi (add immediate) stores into register C the result of adding register A and value B.
		instructionsName.put("addi", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) + instruction.B));

		// Multiplication:
		// mulr (multiply register) stores into register C the result of multiplying register A and register B.
		instructionsName.put("mulr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) * registers.get(instruction.B)));
		// muli (multiply immediate) stores into register C the result of multiplying register A and value B.
		instructionsName.put("muli", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) * instruction.B));

		// Bitwise AND:
		// banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
		instructionsName.put("banr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) & registers.get(instruction.B)));
		// bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
		instructionsName.put("bani", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) & instruction.B));

		// Bitwise OR:
		// borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
		instructionsName.put("borr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) | registers.get(instruction.B)));
		// bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
		instructionsName.put("bori", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) | instruction.B));

		// Assignment:
		// setr (set register) copies the contents of register A into register C. (Input B is ignored.)
		instructionsName.put("setr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A)));
		// seti (set immediate) stores value A into register C. (Input B is ignored.)
		instructionsName.put("seti", (instruction, registers) -> registers.set(instruction.C, instruction.A));

		// Greater-than testing:
		// gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtir", (instruction, registers) -> registers.set(instruction.C, (instruction.A > registers.get(instruction.B)) ? 1 : 0));
		// gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
		instructionsName.put("gtri", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) > instruction.B) ? 1 : 0));
		// gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtrr", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) > registers.get(instruction.B)) ? 1 : 0));

		// Equality testing:
		// eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqir", (instruction, registers) -> registers.set(instruction.C, (instruction.A == registers.get(instruction.B)) ? 1 : 0));
		// eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
		instructionsName.put("eqri", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) == instruction.B) ? 1 : 0));
		// eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqrr", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) == registers.get(instruction.B)) ? 1 : 0));

		return instructionsName;
	}

}
