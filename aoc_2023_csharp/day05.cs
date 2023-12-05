using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day05
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day05.txt");
        var stopwatch = Stopwatch.StartNew();

        long[] ids = input[0].Split(": ")[1].Split(" ").Select(long.Parse).ToArray();
        var levels = new List<List<(long, long, long)>>();
        var level = new List<(long, long, long)>();
        for (int i = 3; i < input.Length;)
        {
            long destinationStart = long.Parse(input[i].Split(" ")[0]);
            long sourceStart = long.Parse(input[i].Split(" ")[1]);
            long rangeLength = long.Parse(input[i].Split(" ")[2]);
            level.Add((destinationStart, sourceStart, rangeLength));
            i++;
            if (i >= input.Length || input[i] == "")
            {
                i += 2;
                level.Sort((x, y) => x.Item2.CompareTo(y.Item2));
                levels.Add(level);
                level = [];
            }
        }

        long part1 = ids.Min();
        var part1Results = new List<long>();
        for (int i = 0; i < ids.Length; i++)
            part1Results.Add(Search(levels, 0, 0, ids[i], ids[i]));
        part1 = part1Results.Min();

        var part2Results = new List<long>();
        for (int i = 0; i <  ids.Length; i+=2) {
            part2Results.Add(Search(levels, 0, 0, ids[i], ids[i] + ids[i + 1] - 1));
        }
        long part2 = part2Results.Min() - 1;

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static long Search(List<List<(long, long, long)>> levels, int level, int index, long start, long end)
    {
        if (level >= levels.Count)
            return start;
        else if (index >= levels[level].Count)
            return Search(levels, level + 1, 0, start, end);
        long destination = levels[level][index].Item1;
        long source = levels[level][index].Item2;
        long length = levels[level][index].Item3;
        long offset = destination - source;
        // --##--
        // AA----
        if (end < source)
            return Search(levels, level + 1, 0, start, end);
        // --##--
        // ----AA
        else if (start > source + length)
            return Search(levels, level, index + 1, start, end);
        // -####-
        // --AA--
        else if (start >= source && end <= source + length)
            return Search(levels, level + 1, 0, start + offset, end + offset);
        // --##--
        // -ABBC-
        else if (start < source && end > source + length)
        {
            long a = Search(levels, level, index, start, source - 1);
            long b = Search(levels, level, index, source, source + length);
            long c = Search(levels, level, index, source + length + 1, end);
            return long.Min(a, long.Min(b, c));
        }
        // --##--
        // -AB---
        else if (start < source)
        {
            long a = Search(levels, level, index, start, source - 1);
            long b = Search(levels, level, index, source, end);
            return long.Min(a, b);
        }
        // --##--
        // ---AB-
        else if (end > source + length)
        {
            long a = Search(levels, level, index, start, source + length);
            long b = Search(levels, level, index, source + length + 1, end);
            return long.Min(a, b);
        }
        else
            throw new Exception("Unhandled scenario");
    }
}
