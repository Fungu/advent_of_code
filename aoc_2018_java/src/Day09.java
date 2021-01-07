import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day09 implements AocSolver {
	public static void main(String[] args) {
		Aoc.runRaw(new Day09());
	}

	class Node {
		int data;
		Node prev;
		Node next;

		public Node(int data) {
			this.data = data;
		}
	}

	class CircularLinkedList {
		Node first = null;

		void insertAfter(Node refNode, Node newNode) {
			newNode.prev = refNode;
			newNode.next = refNode.next;
			newNode.next.prev = newNode;
			refNode.next = newNode;
		}

		void insertAtEnd(Node newNode) {
			if (first == null) {
				first = newNode;
				newNode.next = newNode;
				newNode.prev = newNode;
			} else {
				insertAfter(first.prev, newNode);
			}

		}

		void remove(Node node) {
			if (first.next == first) {
				first = null;
			} else {
				node.prev.next = node.next;
				node.next.prev = node.prev;
				if (first == node) {
					first = node.next;
				}
			}
		}
	}

	@Override
	public void solve(String input) {
		Pattern regex = Pattern.compile("(?<players>[0-9]+) players; last marble is worth (?<points>[0-9]+) points");
		Matcher matcher = regex.matcher(input);
		matcher.matches();
		int playerCount = Integer.parseInt(matcher.group("players"));
		int maxMarble = Integer.parseInt(matcher.group("points"));
		
		long part1 = play(playerCount, maxMarble);
		long part2 = play(playerCount, maxMarble * 100);
		
		System.out.println("Part 1: " + part1);
		System.out.println("Part 2: " + part2);
	}
	
	private long play(int playerCount, int maxMarble) {
		long[] score = new long[playerCount];
		int currentPlayer = 0;
		CircularLinkedList linkedList = new CircularLinkedList();
		Node currentMarble = new Node(0);
		linkedList.insertAtEnd(currentMarble);
		for (int marble = 1; marble <= maxMarble; marble++) {
			currentPlayer++;
			if (currentPlayer == playerCount) {
				currentPlayer = 0;
			}
			if (marble % 23 == 0) {
				score[currentPlayer] += marble;
				for (int i = 0; i < 6; i++) {
					currentMarble = currentMarble.prev;
				}
				score[currentPlayer] += currentMarble.prev.data;
				linkedList.remove(currentMarble.prev);
			} else {
				Node newNode = new Node(marble);
				linkedList.insertAfter(currentMarble.next, newNode);
				currentMarble = newNode;
			}
		}

		return Arrays.stream(score).max().getAsLong();
	}

}