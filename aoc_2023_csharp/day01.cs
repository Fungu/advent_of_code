using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day01
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day01.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        foreach (string line in input)
        {
            List<int> list = [];
            foreach (char c in line)
                if (int.TryParse(c.ToString(), out int i))
                    list.Add(i);
            part1 += list.First() * 10 + list.Last();
        }

        int part2 = 0;
        foreach (string line in input)
        {
            string parsedLine = line;
            parsedLine = parsedLine.Replace("zero", "e0o");
            parsedLine = parsedLine.Replace("one", "o1e");
            parsedLine = parsedLine.Replace("two", "t2o");
            parsedLine = parsedLine.Replace("three", "t3e");
            parsedLine = parsedLine.Replace("four", "4");
            parsedLine = parsedLine.Replace("five", "5e");
            parsedLine = parsedLine.Replace("six", "6");
            parsedLine = parsedLine.Replace("seven", "7");
            parsedLine = parsedLine.Replace("eight", "e8t");
            parsedLine = parsedLine.Replace("nine", "9e");
            List<int> list = [];
            foreach (char c in parsedLine)
                if (int.TryParse(c.ToString(), out int i))
                    list.Add(i);
            part2 += list.First() * 10 + list.Last();
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
