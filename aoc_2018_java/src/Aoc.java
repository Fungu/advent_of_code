import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.time.LocalTime;

public class Aoc {
    public static void runLines(AocSolver solver) {
        runLines(solver, solver.getClass().getSimpleName() + ".txt");
    }
    
    public static void runLines(AocSolver solver, String inputFileString) {
        try {
            LocalTime start = LocalTime.now();
            List<String> inputLines = Files.readAllLines(Path.of("input/" + inputFileString));
            solver.solve(inputLines);
            System.out.println("Execution time: " + LocalTime.now().compareTo(start) + " ms");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void runRaw(AocSolver solver) {
    	runRaw(solver, solver.getClass().getSimpleName() + ".txt");
    }
    
    public static void runRaw(AocSolver solver, String inputFileString) {
        try {
            LocalTime start = LocalTime.now();
            String inputLines = Files.readString(Path.of("input/" + inputFileString));
            solver.solve(inputLines);
            System.out.println("Execution time: " + LocalTime.now().compareTo(start) + " ms");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private static LocalTime prevTime = LocalTime.now();
    public static void timeDiff(String message) {
    	System.out.println(message + " " + LocalTime.now().compareTo(prevTime));
    	prevTime = LocalTime.now();
    }
}