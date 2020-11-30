package advent2018;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

public class Advent21 {

	private static String readFile(String fileName) throws IOException {
		System.out.println("readFile " + fileName);
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}
	
	public static void main(String[] args) throws IOException, InterruptedException {
		boolean debug = false;

		debug = true;
		new Advent21(readFile("input21"), debug);
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

	public Advent21(String input, boolean debug) {
		populateInstructions();
		
		System.out.println();
		
		String[] inputArray = input.split("\r\n");
		int ipRegister = Integer.parseInt(inputArray[0].replace("#ip ", ""));

		Instruction[] instructions = new Instruction[inputArray.length - 1];
		for (int i = 1; i < inputArray.length; i++) {
			instructions[i - 1] = new Instruction(inputArray[i]);
		}
		
		registers[0] = 14414686;
//		registers = new long[] { 3, 10551292, 3, 9052529, 2, 2 };
		long startTime = System.currentTimeMillis();
		final int iterationsMax = 1000000000;
		HashSet<Long> closedSet = new HashSet<>();
		for (int i = 0; i < 1; i++) {
//			registers = new long[6];
//			registers[0] = i;
			int iteration = 0;
			while (registers[ipRegister] < inputArray.length) {
//				if (iteration++ > iterationsMax) {
//					break;
//				}

				Instruction instruction = instructions[(int) registers[ipRegister]];

				if (registers[ipRegister] == 28) {
					if (closedSet.contains(registers[3]) == false) {
						System.out.println("registers[3]: " + registers[3]);
						closedSet.add(registers[3]);
					}
				}
//				System.out.println(instruction + "\t " + Arrays.toString(registers));

				instruction.predicate.apply(instruction, registers);
				registers[ipRegister]++;

			}
			if (iteration > iterationsMax) {
				System.out.println("Nope " + i);
			} else {
				System.out.println("Yey " + i);
				System.out.println("iteration " + iteration);
			}
		}
		System.out.println("Time: " + (System.currentTimeMillis() - startTime) + "ms");
		System.out.println(Arrays.toString(registers));
		
		// 14414686 - too high
		// 1949 - too low
		// 2792537 - correct
		// part2: 10721810 - correct
	}

	private void populateInstructions() {
//		Addition:
//		addr (add register) stores into register C the result of adding register A and register B.
		instructionsName.put("addr", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] + registers[instruction.B]);
//		addi (add immediate) stores into register C the result of adding register A and value B.
		instructionsName.put("addi", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] + instruction.B);

//		Multiplication:
//		mulr (multiply register) stores into register C the result of multiplying register A and register B.
		instructionsName.put("mulr", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] * registers[instruction.B]);
//		muli (multiply immediate) stores into register C the result of multiplying register A and value B.
		instructionsName.put("muli", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] * instruction.B);

//		Bitwise AND:
//		banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
		instructionsName.put("banr", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] & registers[instruction.B]);
//		bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
		instructionsName.put("bani", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] & instruction.B);

//		Bitwise OR:
//		borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
		instructionsName.put("borr", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] | registers[instruction.B]);
//		bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
		instructionsName.put("bori", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A] | instruction.B);

//		Assignment:
//		setr (set register) copies the contents of register A into register C. (Input B is ignored.)
		instructionsName.put("setr", (instruction, registers) -> registers[instruction.C] =  registers[instruction.A]);
//		seti (set immediate) stores value A into register C. (Input B is ignored.)
		instructionsName.put("seti", (instruction, registers) -> registers[instruction.C] =  instruction.A);

//		Greater-than testing:
//		gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtir", (instruction, registers) -> registers[instruction.C] =  (instruction.A > registers[instruction.B]) ? 1 : 0);
//		gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
		instructionsName.put("gtri", (instruction, registers) -> registers[instruction.C] =  (registers[instruction.A] > instruction.B) ? 1 : 0);
//		gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
		instructionsName.put("gtrr", (instruction, registers) -> registers[instruction.C] =  (registers[instruction.A] > registers[instruction.B]) ? 1 : 0);

//		Equality testing:
//		eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqir", (instruction, registers) -> registers[instruction.C] =  (instruction.A == registers[instruction.B]) ? 1 : 0);
//		eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
		instructionsName.put("eqri", (instruction, registers) -> registers[instruction.C] =  (registers[instruction.A] == instruction.B) ? 1 : 0);
//		eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
		instructionsName.put("eqrr", (instruction, registers) -> registers[instruction.C] =  (registers[instruction.A] == registers[instruction.B]) ? 1 : 0);
	}

}
