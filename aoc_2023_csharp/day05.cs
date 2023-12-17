using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day05
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day05.txt");
        var stopwatch = Stopwatch.StartNew();

        long[] ids = input[0].Split(": ")[1].Split(" ").Select(long.Parse).ToArray();
        var levels = new List<List<(long destination, long source, long length)>>();
        var level = new List<(long destination, long source, long length)>();
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
                levels.Add(level);
                level = [];
            }
        }

        long part1 = ids.Min();
        var part1Results = new List<long>();
        for (int i = 0; i < ids.Length; i++)
            part1Results.Add(Search(levels, 0, 0, (ids[i], ids[i] + 1)));
        part1 = part1Results.Min();

        var part2Results = new List<long>();
        for (int i = 0; i <  ids.Length; i += 2) {
            part2Results.Add(Search(levels, 0, 0, (ids[i], ids[i] + ids[i + 1])));
        }
        long part2 = part2Results.Min();

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static long Search(List<List<(long destination, long source, long length)>> levels, int level, int index, (long start, long end) range)
    {
        if (level >= levels.Count)
            return range.start;
        else if (index >= levels[level].Count)
            return Search(levels, level + 1, 0, range);

        long sourceStart = levels[level][index].source;
        long sourceEnd = levels[level][index].length + sourceStart;
        long offset = levels[level][index].destination - sourceStart;

        List<long> result = [];

        (long start, long end) before = (range.start, long.Min(range.end, sourceStart));
        (long start, long end) overlap = (long.Max(range.start, sourceStart), long.Min(range.end, sourceEnd));
        (long start, long end) after = (long.Max(range.start, sourceEnd), range.end);

        if (before.end > before.start)
            result.Add(Search(levels, level, index + 1, before));
        if (overlap.end > overlap.start)
            result.Add(Search(levels, level + 1, 0, (overlap.start + offset, overlap.end + offset)));
        if (after.end > after.start)
            result.Add(Search(levels, level, index + 1, after));
        
        return result.Min();
    }
}
