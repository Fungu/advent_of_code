package advent2018;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

import javax.swing.JFrame;

public class Advent15 extends JFrame implements KeyListener, MouseListener {

	public static void main(String[] args) throws IOException, InterruptedException {
		boolean debug = false;
		int result;
		int correct;

//		correct = 27730;
//		result = new Advent15(readFile("input15_example1"), debug).getResult();
//		System.out.println("input15_example1: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 36334;
//		result = new Advent15(readFile("input15_example2"), debug).getResult();
//		System.out.println("input15_example2: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 39514;
//		result = new Advent15(readFile("input15_example3"), debug).getResult();
//		System.out.println("input15_example3: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 27755;
//		result = new Advent15(readFile("input15_example4"), debug).getResult();
//		System.out.println("input15_example4: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 28944;
//		result = new Advent15(readFile("input15_example5"), debug).getResult();
//		System.out.println("input15_example5: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 18740;
//		result = new Advent15(readFile("input15_example6"), debug).getResult();
//		System.out.println("input15_example6: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 248848;
//		result = new Advent15(readFile("input15_community1"), debug).getResult();
//		System.out.println("input15_community1: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 201638;
//		result = new Advent15(readFile("input15_community2"), debug).getResult();
//		System.out.println("input15_community2: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 47296;
//		result = new Advent15(readFile("input15_community3"), debug).getResult();
//		System.out.println("input15_community3: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
//
//		correct = 47296;
//		result = new Advent15(readFile("input15_community4"), debug).getResult();
//		System.out.println("input15_community4: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
		
//		debug = true;
		correct = 191216;
		result = new Advent15(readFile("input15_community_frustrating"), debug).getResult();
		System.out.println("input15_community_frustrating: " + correct + "=" + result + (correct != result ? " Wrong" : ""));

//		debug = true;
//		result = new Advent15(readFile("input15"), debug).getResult();
//		System.out.println("Result: " + result);
		
//		String testInput = "#######\r\n" + 
//				"#######\r\n" + 
//				"#.E..G#\r\n" + 
//				"#.#####\r\n" + 
//				"#G#####\r\n" + 
//				"#######\r\n" + 
//				"#######";
//		testInput = "####\r\n" + 
//				"#GG#\r\n" + 
//				"#.E#\r\n" + 
//				"####";
//		testInput = "########\r\n" + 
//				"#..E..G#\r\n" + 
//				"#G######\r\n" + 
//				"########";
		
//		debug = true;
//		correct = 191216;
//		result = new Advent15(testInput, debug).getResult();
//		System.out.println("test: " + correct + "=" + result + (correct != result ? " Wrong" : ""));
		
		
	}

	private static String readFile(String fileName) throws IOException {
		File file = new File("C:\\Users\\Fungu\\workspace\\AdventOfCode2018\\src\\advent2018\\input\\" + fileName);
		return new String(Files.readAllBytes(file.toPath()));
	}

	private void parseInput(String input) {
		String[] inputArray = input.split("\r\n");
		width = inputArray[0].length();
		height = inputArray.length;
		moveDebugGrid = new int[width][height];

		terrain = new boolean[width][height];
		nrOfUnits = 0;
		units = new ArrayList<>();
		for (int x = 0; x < width; x++) {
			for (int y = 0; y < height; y++) {
				if (inputArray[y].charAt(x) == '#') {
					terrain[x][y] = true;
				} else if (inputArray[y].charAt(x) == 'E') {
					units.add(new Unit(x, y, true));
				} else if (inputArray[y].charAt(x) == 'G') {
					units.add(new Unit(x, y, false));
				}
			}
		}
	}

	class DistPos {
		int x, y, dist;

		public DistPos(int x, int y) {
			this.x = x;
			this.y = y;
		}

		public DistPos(int x, int y, int dist) {
			this.x = x;
			this.y = y;
			this.dist = dist;
		}

		public DistPos[] getNeighbors() {
			DistPos[] neighbors = new DistPos[4];
			neighbors[0] = new DistPos(x, y - 1, dist + 1);
			neighbors[1] = new DistPos(x - 1, y, dist + 1);
			neighbors[2] = new DistPos(x + 1, y, dist + 1);
			neighbors[3] = new DistPos(x, y + 1, dist + 1);
			return neighbors;
		}

		@Override
		public boolean equals(Object o) {
			DistPos other = (DistPos) o;
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

	static int nrOfUnits = 0;
	class Unit {
		int id;
		DistPos pos;
		boolean elf;
		int hp = 200;
		int attack = 3;

		public Unit(int x, int y, boolean elf) {
			id = nrOfUnits;
			nrOfUnits++;
			pos = new DistPos(x, y);
			this.elf = elf;
		}
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
	
	int cellWidth = 30;
	int cellHeight = 30;
	int offsetY = 50;
	public void renderOffScreen(final Graphics g) {
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				for (Unit unit : units) {
					if (unit.hp > 0 && unit.pos.x == x && unit.pos.y == y) {
						if (unit.elf) {
							g.setColor(Color.GREEN);
						} else {
							g.setColor(Color.RED);
						}
						g.fillOval(x * cellWidth, offsetY + y * cellHeight, cellWidth, cellHeight);
						g.setColor(Color.BLACK);
						g.drawString(unit.id + "", cellWidth / 4 + x * cellWidth, cellHeight / 2 + offsetY + y * cellHeight);
					}
				}
				g.setColor(Color.BLACK);
				if (terrain[x][y]) {
					g.fillRect(x * cellWidth, offsetY + y * cellHeight, cellWidth, cellHeight);
				} else {
					g.drawRect(x * cellWidth, offsetY + y * cellHeight, cellWidth, cellHeight);
				}
				
				if (moveDebugGrid[x][y] != 0) {
					g.setColor(Color.BLACK);
					g.drawString(moveDebugGrid[x][y] + "", cellWidth / 4 + x * cellWidth, cellHeight / 2 + offsetY + y * cellHeight);
				}
			}
		}
	}
	
	int iteration = 0;
	@Override
	public void keyPressed(KeyEvent e) {
		if (e.getKeyCode() == KeyEvent.VK_ENTER) {
			iteration++;
			iterateDebug();
		} else if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE) {
			parseInput(input);
			iteration--;
			if (iteration < 0) iteration = 0;
			for (int i = 0; i < iteration; i++) {
				iterateDebug();
			}
		}
		moveDebugGrid = new int[width][height];
		repaint();
	}
	@Override
	public void keyReleased(KeyEvent e) {
	}
	@Override
	public void keyTyped(KeyEvent e) {
	}
	@Override
	public void mouseClicked(MouseEvent e) {
		moveDebugGrid = new int[width][height];
		for (Unit unit : units) {
			if (e.getX() < unit.pos.x * cellWidth + cellWidth && 
					e.getX() > unit.pos.x * cellWidth && 
					e.getY() < unit.pos.y * cellHeight + cellHeight + offsetY && 
					e.getY() > unit.pos.y * cellHeight + offsetY) {
				moveDebug(unit);
			}
		}
		repaint();
	}
	int[][] moveDebugGrid;
	private void moveDebug(Unit unit) {
		PriorityQueue<DistPos> open = new PriorityQueue<DistPos>(priorityComp);
		Set<DistPos> closed = new HashSet<>();
		Map<DistPos, DistPos> meta = new HashMap<>();

		unit.pos.dist = 0;
		open.add(unit.pos);
		meta.put(unit.pos, null);

		while (!open.isEmpty()) {
			DistPos currentPos = open.poll();
			moveDebugGrid[currentPos.x][currentPos.y] = currentPos.dist;
			if (isAdjacent(currentPos, !unit.elf)) {
				DistPos nextPos = meta.get(currentPos);
				if (nextPos != null) {
					moveDebugGrid[nextPos.x][nextPos.y] = 99;
//					unit.pos = meta.get(currentPos);
				}
				return;
			}

			for (DistPos neighbor : currentPos.getNeighbors()) {
				if (open.contains(neighbor) == false && closed.contains(neighbor) == false && isEmpty(neighbor)) {
					open.add(neighbor);
					DistPos source = meta.get(currentPos);
					if (source == null) {
						source = neighbor;
					}
					meta.put(neighbor, source);
				}
			}
			closed.add(currentPos);
		}
	}
	
	
	
	


	private final Comparator<Unit> unitComp = new Comparator<Unit>() {
		@Override
		public int compare(Unit o1, Unit o2) {
			return (o1.pos.y * 99999 + o1.pos.x) - (o2.pos.y * 99999 + o2.pos.x);
		}
	};
//	private final Comparator<Unit> unitHpComp = new Comparator<Unit>() {
//		@Override
//		public int compare(Unit o1, Unit o2) {
//			if (o1.hp != o2.hp) {
//				return o1.hp - o2.hp;
//			}
//			return (o1.pos.y * 99999 + o1.pos.x) - (o2.pos.y * 99999 + o2.pos.x);
//		}
//	};
	private final Comparator<DistPos> priorityComp = new Comparator<DistPos>() {
		@Override
		public int compare(DistPos o1, DistPos o2) {
			if (o1.dist != o2.dist) {
				return o1.dist - o2.dist;
			}
			return (o1.y * 99999 + o1.x) - (o2.y * 99999 + o2.x);
		}
	};
	
	
	

	boolean[][] terrain;
	int width;
	int height;
	ArrayList<Unit> units;
	int result = -1;
	String input;

	public Advent15(String input, boolean debug) {
		this.input = input;
		parseInput(input);
		
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(1200, 1200);
		addKeyListener(this);
		addMouseListener(this);
//		setVisible(true);
		
//		if (input != null) return;

		int rounds = 0;
//		for (int attack = 3; attack < 100; attack++) {
//			parseInput(input);
//			for (Unit unit : units) {
//				if (unit.elf) {
//					unit.attack = attack;
//				}
//			}
			
			
			print(debug);
			rounds = 0;
			boolean hasElfs = true;
			boolean hasGoblins = true;
			while (hasElfs && hasGoblins) {
				units.sort(unitComp);
				for (Unit unit : units) {
					if (unit.hp > 0) {
						hasElfs = false;
						hasGoblins = false;
						for (Unit unit2 : units) {
							if (unit2.hp > 0 && unit2.elf) {
								hasElfs = true;
							} else if (unit2.hp > 0 && unit2.elf == false) {
								hasGoblins = true;
							}
						}
						if (!hasElfs || !hasGoblins) {
							rounds--;
							break;
						}

						move(unit);
						attack(unit);
					}
				}

				if (debug) {
//				try {
//					Thread.sleep(1000);
//				} catch (InterruptedException e) {
//				}
				}
				print(debug);

				rounds++;
			}
			
//			boolean success = true;
//			for (Unit unit : units) {
//				if (unit.elf && unit.hp <= 0) {
//					success = false;
//				}
//			}
//			if (success) {
//				System.out.println("attack: " + attack);
//				break;
//			}
//		}

		int totalHp = 0;
		for (Unit unit : units) {
			if (unit.hp > 0) {
				totalHp += unit.hp;
			}
		}
		result = (rounds * totalHp);

		if (debug) {
//			System.out.println((hasElfs ? "Elves" : "Goblins") + " wins");
			System.out.println("Rounds: " + rounds);
			System.out.println("Total hp: " + totalHp);
			System.out.println("Combat result: " + result);
		}

		// 190604 - too low
		// 187801 - too low
		// 193407 - nope
		// 194028 - nope
		
		// 191216 - correct
		
		// part 2: 44790 - too low
		// part 2: 48050 - correct
	}
	
	private void iterateDebug() {
		units.sort(unitComp);
		for (Unit unit : units) {
			if (unit.hp > 0) {
				move(unit);
				attack(unit);
			}
		}
	}

	public int getResult() {
		return result;
	}

	private void attack(Unit unit) {
		Unit bestEnemy = null;
		for (Unit enemy : units) {
			if (unit.elf != enemy.elf && enemy != unit && enemy.hp > 0) {
				if (Math.abs(enemy.pos.x - unit.pos.x) + Math.abs(enemy.pos.y - unit.pos.y) == 1) {
					if (bestEnemy == null) {
						bestEnemy = enemy;
					}
					if ((enemy.hp < bestEnemy.hp) 
							|| (enemy.hp == bestEnemy.hp && enemy.pos.y < bestEnemy.pos.y)
							|| (enemy.hp == bestEnemy.hp && enemy.pos.y == bestEnemy.pos.y && enemy.pos.x < bestEnemy.pos.x)) {
						bestEnemy = enemy;
					}
				}
			}
		}
		if (bestEnemy != null) {
			bestEnemy.hp -= unit.attack;
		}
	}

	private void move(Unit unit) {
		PriorityQueue<DistPos> open = new PriorityQueue<DistPos>(priorityComp);
		Set<DistPos> closed = new HashSet<>();
		Map<DistPos, DistPos> meta = new HashMap<>();

		unit.pos.dist = 0;
		open.add(unit.pos);
		meta.put(unit.pos, null);

		DistPos bestSquare = null;
		
		while (!open.isEmpty() && (bestSquare == null || open.peek().dist == bestSquare.dist)) {
			DistPos currentPos = open.poll();
			if (isAdjacent(currentPos, !unit.elf)) {
				if (bestSquare == null || currentPos.y < bestSquare.y || (currentPos.y == bestSquare.y && currentPos.x < bestSquare.x)) {
					bestSquare = currentPos;
				}
//				DistPos nextPos = meta.get(currentPos);
//				if (nextPos != null) {
//					unit.pos = meta.get(currentPos);
//				}
//				return;
			}

			for (DistPos neighbor : currentPos.getNeighbors()) {
				if (open.contains(neighbor) == false && closed.contains(neighbor) == false && isEmpty(neighbor)) {
					open.add(neighbor);
					DistPos source = meta.get(currentPos);
					if (source == null) {
						source = neighbor;
					}
					meta.put(neighbor, source);
				}
			}
			closed.add(currentPos);
		}
		
		
		if (bestSquare != null) {
			DistPos nextPos = meta.get(bestSquare);
			if (nextPos != null) {
				unit.pos = meta.get(bestSquare);
			}
		}
	}

	private boolean isAdjacent(DistPos pos, boolean elf) {
		for (Unit unit : units) {
			if (unit.hp > 0 && unit.elf == elf) {
				if (unit.pos.x == pos.x && Math.abs(unit.pos.y - pos.y) == 1) {
					return true;
				} else if (unit.pos.y == pos.y && Math.abs(unit.pos.x - pos.x) == 1) {
					return true;
				}
			}
		}
		return false;
	}

	private boolean isEmpty(DistPos pos) {
		if (terrain[pos.x][pos.y]) {
			return false;
		}
		for (Unit unit : units) {
			if (unit.hp > 0 && unit.pos.x == pos.x && unit.pos.y == pos.y) {
				return false;
			}
		}
		return true;
	}

	private void print(boolean debug) {
		if (!debug)
			return;
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				boolean isUnit = false;
				for (Unit unit : units) {
					if (unit.hp > 0 && unit.pos.x == x && unit.pos.y == y) {
						System.out.print(unit.elf ? "E" : "G");
						isUnit = true;
					}
				}
				if (!isUnit) {
					System.out.print(terrain[x][y] ? '#' : '.');
				}
			}
			System.out.print("   ");
			boolean first = true;
			for (int x = 0; x < width; x++) {
				for (Unit unit : units) {
					if (unit.hp > 0 && unit.pos.y == y && unit.pos.x == x) {
						System.out.print((first ? "" : ", ") + (unit.elf ? "E" : "G") + "(" + unit.hp + ")");
						first = false;
					}
				}
			}
			System.out.println();
		}
		System.out.println();
	}

	@Override
	public void mouseEntered(MouseEvent e) {
	}

	@Override
	public void mouseExited(MouseEvent e) {
	}

	@Override
	public void mousePressed(MouseEvent e) {
	}

	@Override
	public void mouseReleased(MouseEvent e) {
	}
}
