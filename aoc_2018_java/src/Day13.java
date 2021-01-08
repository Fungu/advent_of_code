import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Day13 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day13());
	}

	enum Turn {
		LEFT, STRAIGHT, RIGHT
	}

	class Cart {
		final int[] DIRS_X = { 1, 0, -1, 0 };
		final int[] DIRS_Y = { 0, 1, 0, -1 };
		final char[] DIRS_CHAR = { '>', 'v', '<', '^' };
		int posX, posY;
		int dir;
		Turn nextTurn = Turn.LEFT;
		boolean crashed = false;

		public Cart(int posX, int posY, char dirChar) {
			this.posX = posX;
			this.posY = posY;
			this.dir = Arrays.binarySearch(DIRS_CHAR, dirChar);
			this.dir = IntStream.range(0, DIRS_CHAR.length).filter(i -> dirChar == DIRS_CHAR[i]).findFirst().getAsInt();
		}

		public void move(char[][] grid, ArrayList<Cart> cartList) {
			if (crashed) {
				return;
			}
			posX += DIRS_X[dir];
			posY += DIRS_Y[dir];

			List<Cart> crashedCarts = cartList.stream().filter(c -> c != this && c.posX == posX && c.posY == posY).collect(Collectors.toList());
			if (crashedCarts.size() == 1) {
				crashed = true;
				crashedCarts.get(0).crashed = true;
				return;
			}

			char c = grid[posY][posX];
			if (c == '+') {
				if (nextTurn == Turn.LEFT) {
					changeDir(-1);
					nextTurn = Turn.STRAIGHT;
				} else if (nextTurn == Turn.STRAIGHT) {
					nextTurn = Turn.RIGHT;
				} else if (nextTurn == Turn.RIGHT) {
					changeDir(1);
					nextTurn = Turn.LEFT;
				}

			} else if (c == '/') {
				if (dir == 0 || dir == 2) {
					changeDir(-1);
				} else {
					changeDir(1);
				}
			} else if (c == '\\') {
				if (dir == 1 || dir == 3) {
					changeDir(-1);
				} else {
					changeDir(1);
				}
			}
		}

		private void changeDir(int delta) {
			dir += delta;
			if (dir < 0) {
				dir += 4;
			}
			if (dir > 3) {
				dir -= 4;
			}
		}
	}

	@Override
	public void solve(List<String> inputLines) {
		char[][] grid = new char[inputLines.size()][inputLines.get(0).length()];
		ArrayList<Cart> cartList = new ArrayList<>();
		for (int y = 0; y < inputLines.size(); y++) {
			for (int x = 0; x < inputLines.get(0).length(); x++) {
				char c = inputLines.get(y).charAt(x);
				if (c == '<' || c == '>') {
					grid[y][x] = '-';
					cartList.add(new Cart(x, y, c));
				} else if (c == '^' || c == 'v') {
					grid[y][x] = '|';
					cartList.add(new Cart(x, y, c));
				} else {
					grid[y][x] = c;
				}
			}
		}

		String part1 = null;
		while (cartList.size() > 1) {
			// print(grid, cartList);
			cartList.sort((a, b) -> (a.posX != b.posX ? a.posX - b.posX : a.posY - b.posY));
			for (Cart cart : cartList) {
				cart.move(grid, cartList);
				if (cart.crashed && part1 == null) {
					part1 = cart.posX + "," + cart.posY;
				}
			}
			cartList.removeIf(c -> c.crashed);
		}

		String part2 = cartList.get(0).posX + "," + cartList.get(0).posY;

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}

	@SuppressWarnings("unused")
	private void print(char[][] grid, ArrayList<Cart> cartList) {
		System.out.println();
		for (int y = 0; y < grid.length; y++) {
			for (int x = 0; x < grid[0].length; x++) {
				int X = x;
				int Y = y;
				List<Cart> carts = cartList.stream().filter(c -> c.posX == X && c.posY == Y).collect(Collectors.toList());
				if (carts.size() > 1) {
					System.out.print("X");
				} else if (carts.size() == 1) {
					System.out.print(carts.get(0).DIRS_CHAR[carts.get(0).dir]);
				} else {
					System.out.print(grid[y][x]);
				}
			}
			System.out.println();
		}
	}
}
