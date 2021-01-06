import java.util.Arrays;

public class IntTuple {
	public int[] values;

	public IntTuple(int ... values) {
		this.values = values;
	}
	
	@Override
	public int hashCode() {
		return Arrays.hashCode(values);
	}
	
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		IntTuple other = (IntTuple) obj;
		if (!Arrays.equals(values, other.values))
			return false;
		return true;
	}
}
