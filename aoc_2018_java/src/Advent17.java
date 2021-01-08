import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;

import javax.swing.JFrame;

public class Advent17 {

	public static void main(String[] args) throws Exception {
		boolean debug = false;

		debug = true;

		new Advent17(readFile("input17"), debug);
//		new Advent17(readFile("input17_example"), debug);
	}

	private static String readFile(String fileName) throws IOException {
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}

	final char CLAY = '#';
	final char SAND = '.';
	final char FLOW = '|';
	final char STILL = '~';
	final char SOURCE = '+';

	int minX = 0;
	int maxX = Integer.MIN_VALUE;
	int maxY = Integer.MIN_VALUE;
	int minY = 0;
	char[][] grid;
	boolean keepGoing = false;
	int totalFilled = 0;

	class AdventFrame extends JFrame implements KeyListener {
		int cellWidth = 6;
		int cellHeight = 8;
		int offsetY = 50;

		public AdventFrame() {
			super("Advent 17");
			setVisible(true);
			setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			setSize(2000, 2000);
			addKeyListener(this);
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

		public void renderOffScreen(final Graphics g) {
			for (int x = 0; x < maxX - minX; x++) {
				for (int y = 0; y < maxY; y++) {
					switch (grid[x][y]) {
					case CLAY:
						g.setColor(Color.BLACK);
						break;
					case SAND:
						g.setColor(Color.GRAY);
						break;
					case FLOW:
						g.setColor(Color.CYAN);
						break;
					case STILL:
						g.setColor(Color.GREEN);
						break;
					case SOURCE:
						g.setColor(Color.RED);
						break;
					}
					g.fillRect(x * cellWidth, offsetY + y * cellHeight, cellWidth, cellHeight);
//					g.drawString(grid[x][y] + "", x * cellWidth, offsetY + y * cellHeight);
				}
			}
		}

		@Override
		public void keyPressed(KeyEvent e) {
			if (e.getKeyCode() == KeyEvent.VK_ENTER) {
				int springX = 500 - minX;
				int springY = 0;
				flowDown(springX, springY);
			} else if (e.getKeyCode() == KeyEvent.VK_DOWN) {
				offsetY -= 100;
			} else if (e.getKeyCode() == KeyEvent.VK_UP) {
				offsetY += 100;
			}
			repaint();
		}

		@Override
		public void keyReleased(KeyEvent e) {
		}

		@Override
		public void keyTyped(KeyEvent e) {
		}

	}

	AdventFrame adventFrame;

	public Advent17(String input, boolean debug) throws Exception {
		setup(input);

		adventFrame = new AdventFrame();

		execute();
		teardown();
	}

	public void setup(String input) {
		String[] inputArray = input.split("\r\n");

		minX = 249;
		maxX = 557 + 1;
		maxY = 1644;
		minY = 5;

//		minX = 495;
//		maxX = 506;
//		maxY = 13;

		minX--;
		maxX++;
		maxY++;
		minX--;
		maxX++;
		grid = new char[maxX - minX][maxY];
		for (int x = minX; x < maxX; x++) {
			for (int y = 0; y < maxY; y++) {
				grid[x - minX][y] = '.';
			}
		}
		int biggestX = 500;
		int smallestX = 500;
		int biggestY = 0;
		int smallestY = 9999;
		for (String s : inputArray) {
			String first = s.split(", ")[0].trim();
			String second = s.split(", ")[1].trim();
			String secondStart = second.split("=")[1].split("[.][.]")[0];
			String secondEnd = second.split("=")[1].split("[.][.]")[1];
			if (first.startsWith("x")) {
				int x = Integer.parseInt(first.replace("x=", ""));
				int yStart = Integer.parseInt(secondStart.replace("y=", ""));
				int yEnd = Integer.parseInt(secondEnd);
				for (int y = yStart; y <= yEnd; y++) {
					grid[x - minX][y] = '#';
					if (x > biggestX)
						biggestX = x;
					if (y > biggestY)
						biggestY = y;
					if (x < smallestX)
						smallestX = x;
					if (y < smallestY)
						smallestY = y;
				}
			} else {
				int y = Integer.parseInt(first.replace("y=", ""));
				int xStart = Integer.parseInt(secondStart.replace("x=", ""));
				int xEnd = Integer.parseInt(secondEnd);
				for (int x = xStart; x <= xEnd; x++) {
					grid[x - minX][y] = '#';
					if (x > biggestX)
						biggestX = x;
					if (y > biggestY)
						biggestY = y;
					if (x < smallestX)
						smallestX = x;
					if (y < smallestY)
						smallestY = y;
				}
			}
		}
		System.out.println("biggestX " + biggestX);
		System.out.println("smallestX " + smallestX);
		System.out.println("biggestY " + biggestY);
		System.out.println("smallestY " + smallestY);
		int springX = 500;
		int springY = 0;
		grid[springX - minX][springY] = '+';
	}

	public void execute() throws Exception {
		int springX = 500 - minX;
		int springY = 0;
		int nrFilled;
		int iteration = 0;
		do {
			keepGoing = false;
			nrFilled = flowDown(springX, springY);
			totalFilled += nrFilled;

			iteration++;
			if (iteration > 1000) {
				keepGoing = false;
			}
			System.out.println(iteration);

			adventFrame.repaint();
		} while (keepGoing);

		// 8138 - too low
		// 37077 - too high
//		totalFilled 37073
//		part2: 29289
	}

	private int flowDown(int x, int y) {
		int nrFilled = 0;
		while (isFree(x, y + 1)) {
			y++;
			if (grid[x][y] == SAND && y >= minY) {
				nrFilled++;
				keepGoing = true;
			}
			grid[x][y] = FLOW;
			if (y + 1 >= maxY) {
				break;
			}
		}
		if (y + 1 < maxY) {
			nrFilled += flowSideways(x, y);
		}
		return nrFilled;
	}

	private int flowSideways(int x, int y) {
		int nrFilled = 0;
		boolean levelStill = true;

		int leftX = x;
		while (isFree(leftX - 1, y)) {
			leftX--;
			if (isSand(leftX, y)) {
				nrFilled++;
			}
			if (isFree(leftX, y + 1)) {
				levelStill = false;
				nrFilled += flowDown(leftX, y);
				break;
			}
		}
		int rightX = x;
		while (isFree(rightX + 1, y)) {
			rightX++;
			if (isSand(rightX, y)) {
				nrFilled++;
			}
			if (isFree(rightX, y + 1)) {
				levelStill = false;
				nrFilled += flowDown(rightX, y);
				break;
			}
		}

		for (int i = leftX; i <= rightX; i++) {
			grid[i][y] = (levelStill ? '~' : '|');
			if (levelStill) {
				keepGoing = true;
			}
		}
		return nrFilled;
	}

	private boolean isFree(int x, int y) {
		return !isClay(x, y) && !isStill(x, y);
	}

	private boolean isSand(int x, int y) {
		return grid[x][y] == SAND;
	}

	private boolean isClay(int x, int y) {
		return grid[x][y] == CLAY;
	}

	private boolean isStill(int x, int y) {
		return grid[x][y] == STILL;
	}

	private void print() {
//	        if (maxY != 0) return;
//	        for (int y = 0; y < maxY/50; y++) {
//	            for (int x = minX; x < maxX; x++) {
//	                System.out.print(grid[x - minX][y]);
//	            }
//	            System.out.println();
//	        }

		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\output\\Advent_17_output.txt");
		try {
			FileWriter fw = new FileWriter(file);
			for (int y = 0; y < maxY; y++) {
				for (int x = minX; x < maxX; x++) {
					fw.write(grid[x - minX][y]);
				}
				fw.write("\r\n");
			}
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void teardown() {
		print();
		System.out.println("totalFilled " + totalFilled);

		int part2 = 0;
		for (int y = 0; y < maxY; y++) {
			for (int x = minX; x < maxX; x++) {
				if (grid[x - minX][y] == STILL) {
					part2++;
				}
			}
		}
		System.out.println("part2: " + part2);
	}

}
