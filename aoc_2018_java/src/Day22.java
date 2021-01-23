import java.util.List;
import java.util.PriorityQueue;

public class Day22 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day22());
	}
	
	final int ROCKY = 0;
	final int WET = 1;
	final int NARROW = 2;
	
	final int TORCH = 0;
	final int CLIMBING_GEAR = 1;
	final int NEITHER = 2;
	
//		depth: 3879
//		target: 8,713
	int depth = 3879;
	int targetX = 8;
	int targetY = 713;
	
	long[][] geologicIndexGrid = new long[targetY + 1 + 1000][targetX + 1 + 1000];

	@Override
	public void solve(List<String> inputLines) {
		for (int y = 0; y < geologicIndexGrid.length; y++) {
			for (int x = 0; x < geologicIndexGrid[0].length; x++) {
				geologicIndexGrid[y][x] = -1;
			}
		}
		int part1 = 0;
		for (int y = 0; y <= targetY; y++) {
			for (int x = 0; x <= targetX; x++) {
				part1 += getType(x, y);
			}
		}
//		printTypeGrid();
		
		int part2 = aStar();
		
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
	
	@SuppressWarnings("unused")
	private void printTypeGrid() {
		for (int y = 0; y < geologicIndexGrid.length; y++) {
			for (int x = 0; x < geologicIndexGrid[0].length; x++) {
				if (x == 0 && y == 0) {
					System.out.print("M");
				} else if (x == targetX && y == targetY) {
					System.out.print("T");
				} else if (getType(x, y) == 0) {
					System.out.print(".");
				} else if (getType(x, y) == 1) {
					System.out.print("=");
				} else if (getType(x, y) == 2) {
					System.out.print("|");
				} else {
					System.out.print("?");
				}
			}
			System.out.println();
		}
	}

	private long getGeologicIndex(int x, int y) {
		long ret = geologicIndexGrid[y][x];
		if (ret != -1) {
			return ret;
		}
		if (x == 0 && y == 0) {
			ret = 0;
		} else if (x == targetX && y == targetY) {
			ret = 0;
		} else if (y == 0) {
			ret = x * 16807;
		} else if (x == 0) {
			ret = y * 48271;
		} else {
			ret = getErosionLevel(x - 1, y) * getErosionLevel(x, y - 1);
		}
		ret = ret % 20183;
		geologicIndexGrid[y][x] = ret;
		return ret;
	}

	private int getErosionLevel(int x, int y) {
		return (int) ((getGeologicIndex(x, y) + depth) % 20183);
	}


	private int getType(int x, int y) {
		return getErosionLevel(x, y) % 3;
	}
	
	
	private boolean isValid(int tool, int x, int y) {
		long type = getType(x, y);
		if (type == ROCKY) {
			return tool == CLIMBING_GEAR || tool == TORCH;
		} else if (type == WET) {
			return tool == CLIMBING_GEAR || tool == NEITHER;
		} else {
			return tool == TORCH || tool == NEITHER;
		}
	}
	
	class BfsState {
		int tool;
		int x, y;
		
		public BfsState(int tool, int x, int y) {
			this.tool = tool;
			this.x = x;
			this.y = y;
		}
		
		@Override
		public boolean equals(Object object) {
			if (object == null || !(object instanceof BfsState)) {
				return false;
			}
			BfsState other = (BfsState) object;
			return other.x == x && other.y == y && other.tool == tool;
		}
	}
	
	private int h(int x, int y) {
		return Math.abs(targetX - x) + Math.abs(targetY - y);
	}
	
	private int getTool(int x, int y, int currentTool, boolean changeTool) {
		if (!changeTool) {
			return currentTool;
		}
		long type = getType(x, y);
		if (type == ROCKY) {
			if (currentTool == CLIMBING_GEAR) {
				return TORCH;
			} else {
				return CLIMBING_GEAR;
			}
		} else if (type == WET) {
			if (currentTool == CLIMBING_GEAR) {
				return NEITHER;
			} else {
				return CLIMBING_GEAR;
			}
		} else {
			if (currentTool == TORCH) {
				return NEITHER;
			} else {
				return TORCH;
			}
		}
	}
	
	private int aStar() {
		int[] dirX = { 1, 0, -1, 0, 0 };
		int[] dirY = { 0, 1, 0, -1, 0 };
		boolean[] toolChange = { false, false, false, false, true };
		int[] cost = { 1, 1, 1, 1, 7 };
		

	    // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
	    Integer[][][] gScore = new Integer[geologicIndexGrid.length][geologicIndexGrid[0].length][3];
	    for (int y = 0; y < gScore.length; y++) {
	    	for (int x = 0; x < gScore[0].length; x++) {
				for (int t = 0; t < 3; t++) {
					gScore[y][x][t] = Integer.MAX_VALUE;
				}
	    	}
	    }
	    gScore[0][0][TORCH] = 0;

	    // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
	    // how short a path from start to finish can be if it goes through n.
	    int[][][] fScore = new int[geologicIndexGrid.length][geologicIndexGrid[0].length][3];
	    fScore[0][0][TORCH] = h(0, 0);
	    
	    // The set of discovered nodes that may need to be (re-)expanded.
	    // Initially, only the start node is known.
	    PriorityQueue<BfsState> openSet = new PriorityQueue<>((a, b) -> fScore[a.y][a.x][a.tool] - fScore[b.y][b.x][b.tool]);
	    openSet.add(new BfsState(0, 0, TORCH));

	    while (!openSet.isEmpty()) {
	    	BfsState current = openSet.poll();
	    	if (current.x == targetX && current.y == targetY && current.tool == TORCH) {
				return gScore[current.y][current.x][current.tool];
			}

	    	for (int i = 0; i < dirX.length; i++) {
	    		if (current.x + dirX[i] < 0 || current.y + dirY[i] < 0) {
	    			continue;
	    		}
	    		int tool = getTool(current.x + dirX[i], current.y + dirY[i], current.tool, toolChange[i]);
	    		BfsState neighbor = new BfsState(tool, current.x + dirX[i], current.y + dirY[i]);
	    		if (!isValid(tool, neighbor.x, neighbor.y)) {
	    			continue;
	    		}
	    		// d(current,neighbor) is the weight of the edge from current to neighbor
	    		// tentative_gScore is the distance from start to the neighbor through current
	            int tentative_gScore = gScore[current.y][current.x][current.tool] + cost[i];
	            if (tentative_gScore < gScore[neighbor.y][neighbor.x][neighbor.tool]) {
	                // This path to neighbor is better than any previous one. Record it!
	                gScore[neighbor.y][neighbor.x][neighbor.tool] = tentative_gScore;
	                fScore[neighbor.y][neighbor.x][neighbor.tool] = gScore[neighbor.y][neighbor.x][neighbor.tool] + h(neighbor.x, neighbor.y);
	                if (!openSet.contains(neighbor)) {
	                    openSet.add(neighbor);
	                }
	            }
	    	}
	    }
	    
	    return -1;
	}
}
