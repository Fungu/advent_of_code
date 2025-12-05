using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day05
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day05.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;

        List<(long, long)> freshRanges = [];
        bool freshRangesDone = false;
        foreach (string line in lines)
        {
            if (line == "")
            {
                freshRangesDone = true;
            }
            else if (!freshRangesDone)
            {
                freshRanges.Add((long.Parse(line.Split("-")[0]), long.Parse(line.Split("-")[1])));
            }
            else
            {
                long id = long.Parse(line);
                part1 += freshRanges.Any(x => id >= x.Item1 && id <= x.Item2) ? 1 : 0;
            }
        }

        bool keepGoing = true;
        while (keepGoing)
        {
            keepGoing = false;
            for (int i = 0; i < freshRanges.Count; i++)
            {
                for (int j = 0; j < freshRanges.Count; j++)
                {
                    if (i == j) continue;
                    if ((freshRanges[i].Item1 >= freshRanges[j].Item1 && freshRanges[i].Item1 <= freshRanges[j].Item2) ||
                        (freshRanges[i].Item2 >= freshRanges[j].Item1 && freshRanges[i].Item2 <= freshRanges[j].Item2))
                    {
                        freshRanges[i] = (Math.Min(freshRanges[i].Item1, freshRanges[j].Item1),
                                        Math.Max(freshRanges[i].Item2, freshRanges[j].Item2));
                        freshRanges.RemoveAt(j);
                        keepGoing = true;
                    }
                }
            }
        }

        long part2 = freshRanges.Sum(x => x.Item2 - x.Item1 + 1);
        

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
