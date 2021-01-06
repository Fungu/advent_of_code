import java.util.List;

public interface AocSolver {
    public default void solve(List<String> inputLines) {
    	throw new RuntimeException("Not implemented");
    }
    
    public default void solve(String inputBlob) {
    	throw new RuntimeException("Not implemented");
    }
}