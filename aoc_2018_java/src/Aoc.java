import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class Aoc {
    public static void runLines(AocSolver solver) {
        runLines(solver, solver.getClass().getSimpleName() + ".txt");
    }
    
    public static void runLines(AocSolver solver, String inputFileString) {
        try {
        	long start = System.currentTimeMillis();
            List<String> inputLines = Files.readAllLines(Path.of("input/" + inputFileString));
            solver.solve(inputLines);
            System.out.println("Execution time: " + (System.currentTimeMillis() - start) + " ms");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void runRaw(AocSolver solver) {
    	runRaw(solver, solver.getClass().getSimpleName() + ".txt");
    }
    
    public static void runRaw(AocSolver solver, String inputFileString) {
        try {
            long start = System.currentTimeMillis();
            String inputLines = Files.readString(Path.of("input/" + inputFileString));
            solver.solve(inputLines);
            System.out.println("Execution time: " + (System.currentTimeMillis() - start) + " ms");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private static long prevTime = System.currentTimeMillis();
    public static void timeDiff(String message) {
    	System.out.println(message + " " + (System.currentTimeMillis() - prevTime));
    	prevTime = System.currentTimeMillis();
    }
}