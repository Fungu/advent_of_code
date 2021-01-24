import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class Day24 implements AocSolver {

	public static void main(String[] args) {
		Aoc.runLines(new Day24());
	}

	class Unit {
		String name;
		boolean infection;
		int count;
		int hp;
		int damage;
		String damageType;
		int initiative;
		ArrayList<String> immunities = new ArrayList<>();
		ArrayList<String> weaknesses = new ArrayList<>();
		
		Unit target;
		boolean isTargeted;
		
		public int effectivePower() {
			return count * damage;
		}
		
		public int getDamageReceived(Unit other) {
			if (immunities.contains(other.damageType)) {
				return 0;
			} else if (weaknesses.contains(other.damageType)) {
				return other.effectivePower() * 2;
			} else {
				return other.effectivePower();
			}
		}
		
		public void receiveDamage(Unit other) {
			count -= Math.floorDiv(getDamageReceived(other), hp);
		}
	}
	
	@Override
	public void solve(List<String> inputLines) {
		ArrayList<Unit> units = parseInput(inputLines, 0);
		fight(units);
		long part1 = units.stream().mapToInt(u -> u.count).sum();
		
		int boost = 0;
		while (true) {
			boost++;
			units = parseInput(inputLines, boost);
			boolean validFight = fight(units);
			if (validFight && !units.get(0).infection) {
				break;
			}
		}
		long part2 = units.stream().mapToInt(u -> u.count).sum();

		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
	
	private ArrayList<Unit> parseInput(List<String> inputLines, int boost) {
		Pattern pattern = Pattern.compile("(?<count>[0-9]*) units each with (?<hp>[0-9]*) hit points.* with an attack that does (?<damage>[0-9]*) (?<damageType>[a-z]*) damage at initiative (?<initiative>[0-9]*)");
		Pattern immunePattern = Pattern.compile("immune to [a-z, ]*[\\;)]");
		Pattern weakPattern = Pattern.compile("weak to [a-z, ]*[\\;)]");
		ArrayList<Unit> units = new ArrayList<>();
		boolean infection = false;
		int index = 1;
		for (String line : inputLines) {
			if (line.equals("Immune System:") || line.isBlank()) {
				continue;
			}
			if (line.equals("Infection:")) {
				infection = true;
				index = 1;
				continue;
			}
			Matcher matcher = pattern.matcher(line);
			matcher.matches();
			Unit unit = new Unit();
			unit.name = ((infection ? "Infection " : "Immune System ") + index);
			index++;
			unit.infection = infection;
			unit.count = Integer.parseInt(matcher.group("count"));
			unit.hp = Integer.parseInt(matcher.group("hp"));
			unit.damage = Integer.parseInt(matcher.group("damage")) + (infection ? 0 : boost);
			unit.damageType = matcher.group("damageType");
			unit.initiative = Integer.parseInt(matcher.group("initiative"));
			matcher = immunePattern.matcher(line);
			if (matcher.find()) {
				for (String s : matcher.group().replace("immune to ", "").replace(")", "").replace(";", "").split(",")) {
					unit.immunities.add(s.strip());
				}
			}
			matcher = weakPattern.matcher(line);
			if (matcher.find()) {
				for (String s : matcher.group().replace("weak to ", "").replace(")", "").replace(";", "").split(",")) {
					unit.weaknesses.add(s.strip());
				}
			}
			units.add(unit);
		}
		return units;
	}
	
	private boolean fight(ArrayList<Unit> units) {
		PriorityQueue<Unit> unitsToTarget = new PriorityQueue<>((a, b) -> (a.effectivePower() != b.effectivePower() ? b.effectivePower() - a.effectivePower() : b.initiative - a.initiative));
		PriorityQueue<Unit> unitsToAttack = new PriorityQueue<>((a, b) -> (b.initiative - a.initiative));
		boolean hasInfection = true;
		boolean hasImmuneSystem = true;
		boolean stateChanged = true;
		
		while (hasInfection && hasImmuneSystem && stateChanged) {
			stateChanged = false;
			units.stream().forEach(u -> u.isTargeted = false);
			
			unitsToTarget.addAll(units);
			while (!unitsToTarget.isEmpty()) {
				Unit unit = unitsToTarget.poll();
				List<Unit> possibleTargets = units.stream().filter(u -> u.infection != unit.infection && !u.isTargeted).collect(Collectors.toList());
				Unit target = null;
				for (Unit possibleTarget : possibleTargets) {
					if (possibleTarget.getDamageReceived(unit) == 0) {
						continue;
					}
					if (target == null) {
						target = possibleTarget;
						continue;
					}
					// The attacking group chooses to target the group in the enemy army to which it would deal the most damage
					if (possibleTarget.getDamageReceived(unit) > target.getDamageReceived(unit)) {
						target = possibleTarget;
					} else if (possibleTarget.getDamageReceived(unit) == target.getDamageReceived(unit)) {
						// If an attacking group is considering two defending groups to which it would deal equal damage, it chooses to target the defending group with the largest effective power;
						if (possibleTarget.effectivePower() > target.effectivePower()) {
							target = possibleTarget;
						} else if (possibleTarget.effectivePower() == target.effectivePower()) {
							// if there is still a tie, it chooses the defending group with the highest initiative.
							if (possibleTarget.initiative > target.initiative) {
								target = possibleTarget;
							}
						}
					}
				}
				unit.target = target;
				if (target != null) {
					target.isTargeted = true;
				}
			}

			unitsToAttack.addAll(units);
			while (!unitsToAttack.isEmpty()) {
				Unit unit = unitsToAttack.poll();
				if (unit.target != null) {
					stateChanged = true;
					unit.target.receiveDamage(unit);
					if (unit.target.count <= 0) {
						unitsToAttack.remove(unit.target);
						units.remove(unit.target);
					}
				}
			}
			
			hasInfection = units.stream().anyMatch(u -> u.infection);
			hasImmuneSystem = units.stream().anyMatch(u -> !u.infection);
		}
		return stateChanged;
	}


}
