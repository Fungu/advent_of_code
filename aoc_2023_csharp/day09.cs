using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day09
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day09.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        int part2 = 0;

        foreach (string line in input)
        {
            List<int> values = line.Split(" ").Select(s => int.Parse(s)).ToList();
            (int, int) predictions = RunOasis(values);
            part1 += predictions.Item1;
            part2 += predictions.Item2;
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static (int, int) RunOasis(List<int> input)
    {
        if (input.All(a => a == 0))
            return (0, 0);
        
        List<int> nextList = [];
        for (int i = 0; i < input.Count - 1; i++)
            nextList.Add(input[i + 1] - input[i]);
        
        (int, int) predictions = RunOasis(nextList);
        return (input.Last() + predictions.Item1, input[0] - predictions.Item2);
    }
}
