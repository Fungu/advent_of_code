import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

public class Advent16 {

	public static void main(String[] args) throws IOException, InterruptedException {
		boolean debug = false;
		int result;

		debug = true;
		result = new Advent16(readFile("input16a"), readFile("input16b"), debug).getResult();
		System.out.println("Result: " + result);
	}

	private static String readFile(String fileName) throws IOException {
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}

	int result = 0;

	public int getResult() {
		return result;
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

	Map<String, Predicate<?>> instructionsName = new HashMap<>();
	Map<Integer, Predicate<?>> instructionsId = new HashMap<>();

	public Advent16(String input, String input2, boolean debug) {
		populateInstructions();
		
		Map<String, Set<Integer>> possibleMatches = new HashMap<>();
		
		String[] inputArray = input.split("\r\n");
		for (int i = 0; i < inputArray.length; i += 4) {
			String beforeString = inputArray[i].replace("Before: ", "").replace("[", "").replace("]", "").trim();
			Instruction instruction = new Instruction(inputArray[i + 1]);
			String afterString = inputArray[i + 2].replace("After: ", "").replace("[", "").replace("]", "").trim();
			
			ArrayList<Integer> after = stringToList(afterString);
			int possibleInstructions = 0;
			for (String key : instructionsName.keySet()) {
				Predicate<?> predicate = instructionsName.get(key);
				ArrayList<Integer> before = stringToList(beforeString);
				predicate.apply(instruction, before);
				if (before.equals(after)) {
					possibleInstructions++;
					
					if (possibleMatches.containsKey(key) == false) {
						possibleMatches.put(key, new HashSet<Integer>());
					}
					possibleMatches.get(key).add(instruction.opcode);
				}
			}
			if (possibleInstructions >= 3) {
				result++;
			}
		}
		for (Entry<String, Set<Integer>> entry : possibleMatches.entrySet()) {
			System.out.print(entry.getKey());
			for (Integer opcode : entry.getValue()) {
				System.out.print(", " + opcode);
			}
			System.out.println();
		}
		
//		eqrr, 4
		instructionsId.put(4, instructionsName.get("eqrr"));
//		borr, 11
		instructionsId.put(11, instructionsName.get("borr"));
//		setr, 6
		instructionsId.put(6, instructionsName.get("setr"));
//		addi, 2
		instructionsId.put(2, instructionsName.get("addi"));
//		gtir, 10
		instructionsId.put(10, instructionsName.get("gtir"));
//		bori, 7
		instructionsId.put(7, instructionsName.get("bori"));
//		eqri, 9
		instructionsId.put(9, instructionsName.get("eqri"));
//		banr, 15
		instructionsId.put(15, instructionsName.get("banr"));
//		seti, 3
		instructionsId.put(3, instructionsName.get("seti"));
//		gtri, 8
		instructionsId.put(8, instructionsName.get("gtri"));
//		bani, 1
		instructionsId.put(1, instructionsName.get("bani"));
//		muli, 0
		instructionsId.put(0, instructionsName.get("muli"));
//		eqir, 5
		instructionsId.put(5, instructionsName.get("eqir"));
//		addr, 12
		instructionsId.put(12, instructionsName.get("addr"));
//		gtrr, 13
		instructionsId.put(13, instructionsName.get("gtrr"));
//		mulr, 14
		instructionsId.put(14, instructionsName.get("mulr"));
		
		String[] inputArray2 = input2.split("\r\n");
		ArrayList<Integer> registers = new ArrayList<>();
		registers.add(0);
		registers.add(0);
		registers.add(0);
		registers.add(0);
		for (String s : inputArray2) {
			Instruction instruction = new Instruction(s);
			instructionsId.get(instruction.opcode).apply(instruction, registers);
		}
		System.out.println("Part 2: " + registers);
	}

	private void populateInstructions() {
//		Addition:
//		addr (add register) stores into register C the result of adding register A and register B.
		instructionsName.put("addr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) + registers.get(instruction.B)));
//		addi (add immediate) stores into register C the result of adding register A and value B.
		instructionsName.put("addi", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) + instruction.B));

//		Multiplication:
//		mulr (multiply register) stores into register C the result of multiplying register A and register B.
		instructionsName.put("mulr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) * registers.get(instruction.B)));
//		muli (multiply immediate) stores into register C the result of multiplying register A and value B.
		instructionsName.put("muli", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) * instruction.B));

//		Bitwise AND:
//		banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
		instructionsName.put("banr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) & registers.get(instruction.B)));
//		bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
		instructionsName.put("bani", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) & instruction.B));

//		Bitwise OR:
//		borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
		instructionsName.put("borr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) | registers.get(instruction.B)));
//		bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
		instructionsName.put("bori", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A) | instruction.B));

//		Assignment:
//		setr (set register) copies the contents of register A into register C. (Input B is ignored.)
		instructionsName.put("setr", (instruction, registers) -> registers.set(instruction.C, registers.get(instruction.A)));
//		seti (set immediate) stores value A into register C. (Input B is ignored.)
		instructionsName.put("seti", (instruction, registers) -> registers.set(instruction.C, instruction.A));

//		Greater-than testing:
//		gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtir", (instruction, registers) -> registers.set(instruction.C, (instruction.A > registers.get(instruction.B)) ? 1 : 0));
//		gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
		instructionsName.put("gtri", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) > instruction.B) ? 1 : 0));
//		gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtrr", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) > registers.get(instruction.B)) ? 1 : 0));

//		Equality testing:
//		eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqir", (instruction, registers) -> registers.set(instruction.C, (instruction.A == registers.get(instruction.B)) ? 1 : 0));
//		eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
		instructionsName.put("eqri", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) == instruction.B) ? 1 : 0));
//		eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqrr", (instruction, registers) -> registers.set(instruction.C, (registers.get(instruction.A) == registers.get(instruction.B)) ? 1 : 0));
	}

}
