using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day07
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day07.txt");
        var stopwatch = Stopwatch.StartNew();

        long part1 = 0;
        Dictionary<int, long> tachyonCount = [];
        tachyonCount.Add(lines[0].IndexOf('S'), 1);
        for (int y = 1; y < lines.Length; y++)
        {
            Dictionary<int, long> nextTachyonCount = [];
            foreach (KeyValuePair<int, long> tachyon in tachyonCount.AsEnumerable())
            {
                if (lines[y][tachyon.Key] == '^')
                {
                    AddOrIncrease(nextTachyonCount, tachyon.Key - 1, tachyon.Value);
                    AddOrIncrease(nextTachyonCount, tachyon.Key + 1, tachyon.Value);
                    part1++;
                }
                else
                {
                    AddOrIncrease(nextTachyonCount, tachyon.Key, tachyon.Value);
                }
            }
            tachyonCount = nextTachyonCount;
        }
        long part2 = tachyonCount.Select(a => a.Value).Sum();
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static void AddOrIncrease(Dictionary<int, long> dict, int key, long value)
    {
        if (dict.ContainsKey(key))
        {
            dict[key] += value;
        }
        else
        {
            dict[key] = value;
        }
    }
}
