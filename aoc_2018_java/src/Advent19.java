import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Image;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import javax.swing.JFrame;

public class Advent19 extends JFrame {

	private static String readFile(String fileName) throws IOException {
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}
	
	public static void main(String[] args) throws IOException, InterruptedException {
		boolean debug = false;

		debug = true;
		new Advent19(readFile("input19"), debug);
	}
	
	Image offScreenImageDrawed = null;
	Graphics offScreenGraphicsDrawed = null;
	@Override
	public void paint(Graphics g) {
		final Dimension d = getSize();
		if (offScreenImageDrawed == null) {
			// Double-buffer: clear the offscreen image.
			offScreenImageDrawed = createImage(d.width, d.height);
		}
		offScreenGraphicsDrawed = offScreenImageDrawed.getGraphics();
		offScreenGraphicsDrawed.setColor(Color.white);
		offScreenGraphicsDrawed.fillRect(0, 0, d.width, d.height);
		/////////////////////
		// Paint Offscreen //
		/////////////////////
		renderOffScreen(offScreenImageDrawed.getGraphics());
		g.drawImage(offScreenImageDrawed, 0, 0, null);

	}

	long[] maxValues = new long[] { 1, Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE, Integer.MAX_VALUE };
	public void renderOffScreen(final Graphics g) {
		for (int i = 0; i < 6; i++) {
			if (registers[i] > maxValues[i]) {
				maxValues[i] = registers[i];
			}
		}
		int cellWidth = 20;
		int totalHeight = 200;
		int offsetY = 400;
		for (int i = 0; i < 6; i++) {
			int height = (int)((registers[i] / maxValues[i]) * totalHeight);
			g.fillRect(30 + i * cellWidth, offsetY - height, 10, height);
			g.drawString(i + "", 30 + i * cellWidth, offsetY + 20);
		}
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

	public Advent19(String input, boolean debug) {
		populateInstructions();
		
		String[] inputArray = input.split("\r\n");
		int ipRegister = Integer.parseInt(inputArray[0].replace("#ip ", ""));

		Instruction[] instructions = new Instruction[inputArray.length - 1];
		for (int i = 1; i < inputArray.length; i++) {
			instructions[i - 1] = new Instruction(inputArray[i]);
		}
		
		registers[0] = 1;
		registers = new long[] { 3, 10551292, 3, 9052529, 2, 2 };
		long startTime = System.currentTimeMillis();
//		final int iterationsMax = 50;
//		int iteration = 0;
		while (registers[ipRegister] < inputArray.length) {
//			if (iteration++ > iterationsMax) {
//				break;
//			}
			
			if (registers[ipRegister] == 3) {
				while (true) {
//					System.out.println(Arrays.toString(registers));
					
					if (registers[3] * registers[5] == registers[1]) {
						registers[0] += registers[5];
					}
					
					if (registers[3] < (registers[1] / registers[5])) {
						registers[3] = (registers[1] / registers[5]);
					} else {
						registers[3] = registers[1];
						registers[3]++;
					}
					
					if (registers[3] > registers[1]) {
						registers[5]++;
						if (registers[5] > registers[1]) {
							registers[ipRegister] = 257 * 257;
							break;
						} else {
							registers[3] = 1;
							registers[4] = registers[5];
						}
					}
				}
			} else {
				Instruction instruction = instructions[(int) registers[ipRegister]];

				System.out.println(instruction + " " + Arrays.toString(registers));

				instruction.predicate.apply(instruction, registers);
				registers[ipRegister]++;
			}
			
			repaint();
		}
		System.out.println("Time: " + (System.currentTimeMillis() - startTime) + "ms");
		System.out.println(Arrays.toString(registers));
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
