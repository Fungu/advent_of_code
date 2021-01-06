package advent2018;

import java.awt.Point;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Advent20 {

	private static String readFile(String fileName) throws IOException {
		System.out.println("readFile " + fileName);
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}

	public static void main(String[] args) throws IOException, InterruptedException {
		boolean debug = false;

		debug = true;
		new Advent20(readFile("input20"), debug);
//		new Advent20(readFile("input20_example1"), debug); // Part 1: 3
//		new Advent20(readFile("input20_example2"), debug); // Part 1: 10
//		new Advent20(readFile("input20_example3"), debug); // Part 1: 18
//		new Advent20(readFile("input20_example4"), debug); // Part 1: 23
//		new Advent20(readFile("input20_example5"), debug); // Part 1: 31
//		new Advent20(readFile("input20_community1"), debug); // Part 1: 8
//		new Advent20(readFile("input20_community2"), debug); // Part 1: 4
	}
	
	final int radius = 106;
//	final int radius = 20;

	final char[] inputArray;

	// ^WWSWNNWNENWWSSSESWSSWWWWSSESSWNWSWSESSSSWWNENWWNE(NNNNE(NNWWWNWNENEENNWSWWSWNNNWWNWWWNWNENWWSWNNWNNNWNENESEENNW(S|NWSWNWSSWWWSSEE(NWES|)SES

	public Advent20(String input, boolean debug) {
//		System.out.println(input);
		inputArray = input.toCharArray();
		initGrid();
		
		parse(0, 0, 0);
		
//		parseDeluxe(new Room(0, 0, 0));

		printGrid();

		floodFill();
		
//		floodFillDeluxe();
		
		// 3929 - too low
		// 3933 - too high
		// 3930 - correct
		// Part 2
		// 8238 - too low
		// 8239 - too low
		// 8240 - correct
	}
	/*
	class Room {
		int x;
		int y;
		int index;

		public Room(int x, int y, int index) {
			this.x = x;
			this.y = y;
			this.index = index;
		}
		
		@Override
		public boolean equals(Object o) {
			Room other = (Room) o;
			return other.x == x && other.y == y;
		}

		@Override
		public String toString() {
			return x + ", " + y;
		}

		@Override
		public int hashCode() {
			return y * 99999 + x;
		}
	}
	
	HashSet<Room> open = new HashSet<>();
	
	private void parseDeluxe(Room room) {
		boolean loop = true;
		int closeRemaining;
		while (loop) {
			room.index++;
			switch (inputArray[room.index]) {
			case '(':
				parse(room.x, room.y, room.index);
				closeRemaining = 0;
				for (int i = index + 1; ; i++) {
					if (inputArray[i] == ')') {
						closeRemaining--;
					} else if (inputArray[i] == '(') {
						closeRemaining++;
					} else if (inputArray[i] == '|' && closeRemaining == 0) {
						index = i;
						break;
					}
				}
				parse(x, y, index);
				loop = false;
				break;
			case ')':
				break;
			case '|':
				closeRemaining = 1;
				for (int i = index; ; i++) {
					if (inputArray[i] == ')') {
						closeRemaining--;
					} else if (inputArray[i] == '(') {
						closeRemaining++;
					}
					if (closeRemaining == 0) {
						index = i;
						break;
					}
				}
				break;
			case '$':
				loop = false;
				break;
			case 'E':
				x++;
				setGrid(x, y);
				x++;
				setGrid(x, y);
				break;
			case 'W':
				x--;
				setGrid(x, y);
				x--;
				setGrid(x, y);
				break;
			case 'S':
				y++;
				setGrid(x, y);
				y++;
				setGrid(x, y);
				break;
			case 'N':
				y--;
				setGrid(x, y);
				y--;
				setGrid(x, y);
				break;
			default:
			}
			
			switch (inputArray[index]) {
			case 'E':
			case 'W':
			case 'S':
			case 'N':
				Point p = new Point(x, y);
				if (closed.contains(p)) {
					System.out.println("leaving " + p + " by " + index + " " + inputArray[index]);
					loop = false;
					break;
				}
				System.out.println("Add " + p);
				closed.add(p);
			}
		}
//		System.out.println("Stopping");
	}*/
	
	
	
	
	////////////////////////////

	int loopLevel = 0;

	// ^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
	// ^(SSS|EEESSSWWW)ENNES$
	// ^N(E|W)N$
	Set<Point> closed = new HashSet<>();
	Set<Point> closed2 = new HashSet<>();
	Set<Point> closed3 = new HashSet<>();
	int activeThreads = 0;
	private void parse(int x, int y, int index) {
//		System.out.println("Starting " + (activeThreads++) + " " + index);
		boolean loop = true;
		int closeRemaining;
		int secondChance = 1;
		while (loop) {
			index++;
			boolean wasOpen = false;
			
			
			switch (inputArray[index]) {
			case '(':
				setChar(x, y, '.');
				parse(x, y, index);
				closeRemaining = 0;
				for (int i = index + 1; ; i++) {
					if (inputArray[i] == ')') {
						closeRemaining--;
					} else if (inputArray[i] == '(') {
						closeRemaining++;
					} else if (inputArray[i] == '|' && closeRemaining == 0) {
						index = i;
						break;
					}
				}
				parse(x, y, index);
				loop = false;
				break;
			case ')':
				break;
			case '|':
				closeRemaining = 1;
				for (int i = index; ; i++) {
					if (inputArray[i] == ')') {
						closeRemaining--;
					} else if (inputArray[i] == '(') {
						closeRemaining++;
					}
					if (closeRemaining == 0) {
						index = i;
						break;
					}
				}
				break;
			case '$':
				loop = false;
				break;
			case 'E':
				x++;
				wasOpen |= setOpen(x, y);
				x++;
				setOpen(x, y);
				break;
			case 'W':
				x--;
				wasOpen |= setOpen(x, y);
				x--;
				setOpen(x, y);
				break;
			case 'S':
				y++;
				wasOpen |= setOpen(x, y);
				y++;
				setOpen(x, y);
				break;
			case 'N':
				y--;
				wasOpen |= setOpen(x, y);
				y--;
				setOpen(x, y);
				break;
			default:
			}
			
			if (wasOpen) {
				secondChance--;
//				System.out.print("wasOpen " + x + " " + y + " " + index + " |\t ");
//				for (int i = index - 5; i <= index; i++) {
//					System.out.print(inputArray[i]);
//				}
//				System.out.println();
				if (secondChance == 0) {
					loop = false;
					break;
				}
			}
			
//			switch (inputArray[index]) {
//			case 'E':
//			case 'W':
//			case 'S':
//			case 'N':
//				Point p = new Point(x, y);
//				if (closed.contains(p)) {
//					System.out.println("leaving " + p + " by " + index + " " + inputArray[index]);
//					loop = false;
//					break;
//				}
//				System.out.println("Add " + p);
//				closed.add(p);
//			}
		}
//		System.out.println("Stopping");
	}

	char[][] grid = new char[radius * 2 + 1][radius * 2 + 1];

	private void initGrid() {
		for (int y = -radius; y < radius; y++) {
			for (int x = -radius; x < radius; x++) {
				setChar(x, y, '#');
			}
		}
	}
	private boolean setOpen(int x, int y) {
		if (grid[x + radius][y + radius] == '.') {
			System.err.println("oops");
		}
		boolean wasOpen = grid[x + radius][y + radius] == ' ';
		grid[x + radius][y + radius] = ' ';
		return wasOpen;
	}
	
	private void setChar(int x, int y, char c) {
		grid[x + radius][y + radius] = c;
	}

	private boolean getOpen(int x, int y) {
		return grid[x + radius][y + radius] != '#';
	}
	
	private char getChar(int x, int y) {
		return grid[x + radius][y + radius];
	}

	private void printGrid() {
//		if (grid.length != 0) {
//			return;
//		}
		for (int y = -radius; y < radius; y++) {
			for (int x = -radius; x < radius; x++) {
				if (x == 0 && y == 0) {
					System.out.print("X");
				} else {
//					System.out.print(getGrid(x, y) ? " " : "#");
					System.out.print(getChar(x, y));
				}
			}
			System.out.println();
		}
	}
	

	int[][] floodFillGrid = new int[radius * 2 + 1][radius * 2 + 1];
	private void floodFill() {
		Deque<Point> open = new ArrayDeque<>();
		Set<Point> closed = new HashSet<>();
		Map<Point, Integer> distances = new HashMap<>();

		open.add(new Point(0, 0));
		distances.put(new Point(0, 0), 0);

		int nearby = 0;
		Point lastPos = null;
		while (!open.isEmpty()) {
			Point currentPos = open.poll();
			lastPos = currentPos;
			int distance = distances.get(currentPos);
			if (distance >= 2000) {
				nearby++;
			}

			Point[] neighbors = new Point[] { new Point(currentPos.x + 1, currentPos.y), new Point(currentPos.x - 1, currentPos.y), 
					new Point(currentPos.x, currentPos.y + 1), new Point(currentPos.x, currentPos.y - 1) };
			for (Point neighbor : neighbors) {
				if (open.contains(neighbor) == false && closed.contains(neighbor) == false && getOpen(neighbor.x, neighbor.y)) {
					open.add(neighbor);
					distances.put(neighbor, distance + 1);
				}
			}
			closed.add(currentPos);
		}
		System.out.println("Part 1: " + (distances.get(lastPos) / 2));
		System.out.println("Part 2: " + (nearby / 2));
	}
	
}
