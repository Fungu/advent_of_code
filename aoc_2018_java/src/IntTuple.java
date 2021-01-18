import java.util.Arrays;

public class IntTuple {
	public int[] values;

	public IntTuple(int ... values) {
		this.values = values;
	}
	
	public void add(IntTuple otherIntTuple) {
		if (values.length != otherIntTuple.values.length) {
			throw new RuntimeException("IntTuple add requires values of the same length.");
		}
		for (int i = 0; i < values.length; i++) {
			values[i] += otherIntTuple.values[i];
		}
	}
	
	@Override
	public String toString() {
		return Arrays.toString(values);
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
