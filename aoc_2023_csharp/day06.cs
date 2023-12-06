using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day06
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day06.txt");
        var stopwatch = Stopwatch.StartNew();

        int[] times = input[0].Split(": ")[1].Split(" ").Where(s => s.Length > 0).Select(int.Parse).ToArray();
        int[] distances = input[1].Split(": ")[1].Split(" ").Where(s => s.Length > 0).Select(int.Parse).ToArray();
        int part1 = 1;
        for (int i = 0; i < times.Length; i++)
        {
            int waysToWin = 0;
            for (int a = 0; a < times[i]; a++)
                if (a * (times[i] - a) > distances[i])
                    waysToWin++;
            part1 *= waysToWin;
        }

        long time = long.Parse(input[0].Split(": ")[1].Replace(" ", ""));
        long distance = long.Parse(input[1].Split(": ")[1].Replace(" ", ""));
        int part2 = 0;
        for (int a = 0; a < time; a++)
            if (a * (time - a) > distance)
                part2++;


        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
