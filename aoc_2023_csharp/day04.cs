using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day04
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day04.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        int part2 = 0;
        int index = 0;
        List<int> scratchcardInstances = Enumerable.Repeat(1, input.Length).ToList();
        foreach (string line in input)
        {
            int instances = scratchcardInstances[index++];
            part2 += instances;

            string numbers = line.Split(": ")[1];
            string[] winning = numbers.Split(" | ")[0].Split(" ").Where(s => s.Length > 0).ToArray();
            string[] have = numbers.Split(" | ")[1].Split(" ").Where(s => s.Length > 0).ToArray();
            
            int matches = winning.Where(w => have.Contains(w)).Count();
            if (matches > 0)
                part1 += (int)Math.Pow(2, matches - 1);
            for (int i = 0; i < matches; i++)
                scratchcardInstances[i + index] += instances;
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
