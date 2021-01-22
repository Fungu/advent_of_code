import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

public class Day21 implements AocSolver {

	public static void main(String[] args) throws IOException, InterruptedException {
		Aoc.runLines(new Day21());
	}

	class Instruction {
		public final String opname;
		public final int A;
		public final int B;
		public final int C;
		public final Predicate<?> predicate;

		public Instruction(String inputLine) {
			opname = inputLine.split(" ")[0];
			A = Integer.parseInt(inputLine.split(" ")[1]);
			B = Integer.parseInt(inputLine.split(" ")[2]);
			C = Integer.parseInt(inputLine.split(" ")[3]);
			predicate = instructionsName.get(opname);
		}

		@Override
		public String toString() {
			return opname + " " + A + " " + B + " " + C;
		}
	}

	interface Predicate<T> {
		void apply(Instruction instruction, long[] registers);
	}

	Map<String, Predicate<?>> instructionsName = new HashMap<>();
	long[] registers = new long[6];

	@Override
	public void solve(List<String> inputLines) {
		populateInstructions();

		long[] registers = new long[6];
		int ipRegister = Integer.parseInt(inputLines.get(0).replace("#ip ", ""));
		Instruction[] instructions = new Instruction[inputLines.size() - 1];
		for (int i = 1; i < inputLines.size(); i++) {
			instructions[i - 1] = new Instruction(inputLines.get(i));
		}

		Long part1 = null;
		Long part2 = null;

		HashSet<Long> seen = new HashSet<>();
		long prev = 0;

		while (registers[ipRegister] < inputLines.size()) {
			// Instruction 28 is the only instruction that reads the input register
			if (registers[ipRegister] == 28) {
				// The first value that register 3 has at instruction 28 is what the input register would have to be
				if (part1 == null) {
					part1 = registers[3];
				}
				// Keep running the program until we start repeating the possible answers
				if (part2 == null && seen.contains(registers[3])) {
					part2 = prev;
				}
				seen.add(registers[3]);
				prev = registers[3];
				if (part1 != null && part2 != null) {
					break;
				}
			}

			Instruction instruction = instructions[(int) registers[ipRegister]];
			instruction.predicate.apply(instruction, registers);
			registers[ipRegister]++;

		}
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	private void populateInstructions() {
		// Addition:
		// addr (add register) stores into register C the result of adding register A and register B.
		instructionsName.put("addr", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] + registers[instruction.B]);
		// addi (add immediate) stores into register C the result of adding register A and value B.
		instructionsName.put("addi", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] + instruction.B);

		// Multiplication:
		// mulr (multiply register) stores into register C the result of multiplying register A and register B.
		instructionsName.put("mulr", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] * registers[instruction.B]);
		// muli (multiply immediate) stores into register C the result of multiplying register A and value B.
		instructionsName.put("muli", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] * instruction.B);

		// Bitwise AND:
		// banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
		instructionsName.put("banr", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] & registers[instruction.B]);
		// bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
		instructionsName.put("bani", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] & instruction.B);

		// Bitwise OR:
		// borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
		instructionsName.put("borr", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] | registers[instruction.B]);
		// bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
		instructionsName.put("bori", (instruction, registers) -> registers[instruction.C] = registers[instruction.A] | instruction.B);

		// Assignment:
		// setr (set register) copies the contents of register A into register C. (Input B is ignored.)
		instructionsName.put("setr", (instruction, registers) -> registers[instruction.C] = registers[instruction.A]);
		// seti (set immediate) stores value A into register C. (Input B is ignored.)
		instructionsName.put("seti", (instruction, registers) -> registers[instruction.C] = instruction.A);

		// Greater-than testing:
		// gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtir", (instruction, registers) -> registers[instruction.C] = (instruction.A > registers[instruction.B]) ? 1 : 0);
		// gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
		instructionsName.put("gtri", (instruction, registers) -> registers[instruction.C] = (registers[instruction.A] > instruction.B) ? 1 : 0);
		// gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtrr", (instruction, registers) -> registers[instruction.C] = (registers[instruction.A] > registers[instruction.B]) ? 1 : 0);

		// Equality testing:
		// eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqir", (instruction, registers) -> registers[instruction.C] = (instruction.A == registers[instruction.B]) ? 1 : 0);
		// eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
		instructionsName.put("eqri", (instruction, registers) -> registers[instruction.C] = (registers[instruction.A] == instruction.B) ? 1 : 0);
		// eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqrr", (instruction, registers) -> registers[instruction.C] = (registers[instruction.A] == registers[instruction.B]) ? 1 : 0);
	}

}
