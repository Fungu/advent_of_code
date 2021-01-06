import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day04 implements AocSolver {
	public static void main(String[] args) {
		Aoc.runLines(new Day04());
	}
	
	enum GuardStatus {
		AWAKE,
		SLEEPING
	}
	
	class Sleep {
		int start;
		int end;
	}
	
	class Guard {
		public int id;
		public GuardStatus guardStatus;
		public ArrayList<Sleep> sleepList = new ArrayList<>();
		
		public Guard(int id) {
			this.id = id;
		}
		
		public void startWorking() {
			guardStatus = GuardStatus.AWAKE;
		}
		
		public void fallAsleep(int time) {
			if (guardStatus == GuardStatus.AWAKE) {
				Sleep sleep = new Sleep();
				sleep.start = time;
				sleepList.add(sleep);
			}
			guardStatus = GuardStatus.SLEEPING;
		}
		
		public void wakeUp(int time) {
			if (guardStatus == GuardStatus.SLEEPING) {
				Sleep sleep = sleepList.get(sleepList.size() - 1);
				sleep.end = time;
			}
			guardStatus = GuardStatus.AWAKE;
		}
		
		public long getLaziness() {
			return sleepList.stream().mapToLong(sleep -> sleep.end - sleep.start).sum();
		}
		
		public Map<Integer, Integer> getSleepPerMinute() {
			HashMap<Integer, Integer> ret = new HashMap<>();
			
			for (int i = 0; i < 60; i++) {
				int tempSleep = 0;
				for (Sleep sleep : sleepList) {
					if (i >= sleep.start && i < sleep.end) {
						tempSleep++;
					}
				}
				ret.put(i, tempSleep);
			}
			
			return ret;
		}
	}
	

	public void solve(List<String> inputLines) {
		Pattern regex = Pattern.compile(".+\\:(?<time>[0-9]+)\\].+");
		Pattern guardRegex = Pattern.compile(".+Guard #(?<id>[0-9]+).+");
		
		HashMap<Integer, Guard> guardMap = new HashMap<>();
		Guard currentGuard = null;
		Collections.sort(inputLines);
		
		for (String line : inputLines) {
			Matcher matcher = regex.matcher(line);
			matcher.matches();
			int time = Integer.parseInt(matcher.group("time"));
			
			if (line.contains("begins shift")) {
				matcher = guardRegex.matcher(line);
				matcher.matches();
				int id = Integer.parseInt(matcher.group("id"));
				if (!guardMap.containsKey(id)) {
					guardMap.put(id, new Guard(id));
				}
				currentGuard = guardMap.get(id);
				currentGuard.startWorking();
				
			} else if (line.contains("falls asleep")) {
				currentGuard.fallAsleep(time);
				
			} else if (line.contains("wakes up")) {
				currentGuard.wakeUp(time);
			}
		}
		
		Guard laziestGuard = guardMap.values().stream().max((a, b) -> (int)(a.getLaziness() - b.getLaziness())).get();
		int laziestMinute = laziestGuard.getSleepPerMinute().entrySet().stream().max((a, b) -> a.getValue() - b.getValue()).get().getKey();
		long part1 = laziestGuard.id * laziestMinute;
		
		laziestGuard = guardMap.values().stream().max((a, b) -> Collections.max(a.getSleepPerMinute().values()) - Collections.max(b.getSleepPerMinute().values())).get();
		laziestMinute = laziestGuard.getSleepPerMinute().entrySet().stream().max((a, b) -> a.getValue() - b.getValue()).get().getKey();
		int part2 = laziestGuard.id * laziestMinute;

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
}