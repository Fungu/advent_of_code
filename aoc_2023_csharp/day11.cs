using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day11
{

    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day11.txt");
        var stopwatch = Stopwatch.StartNew();

        List<(int x, int y)> galaxies = [];
        bool[] isEmptyColumn = Enumerable.Repeat(true, input.Length).ToArray();
        bool[] isEmptyRow = Enumerable.Repeat(true, input[0].Length).ToArray();
        for (int y = 0; y < input.Length; y++)
            for (int x = 0; x < input[0].Length; x++)
                if (input[y][x] == '#')
                {
                    galaxies.Add((x, y));
                    isEmptyColumn[x] = false;
                    isEmptyRow[y] = false;
                }

        long distanceSum = 0;
        long emptySum = 0;
        for (int i = 0; i < galaxies.Count; i++)
            for (int j = i + 1; j < galaxies.Count; j++)
            {
                distanceSum += Math.Abs(galaxies[i].x - galaxies[j].x);
                distanceSum += Math.Abs(galaxies[i].y - galaxies[j].y);

                emptySum += isEmptyColumn.Select((value, index) => new { value, index }).Where(a => a.value && a.index > Math.Min(galaxies[i].x, galaxies[j].x) && a.index < Math.Max(galaxies[i].x, galaxies[j].x)).Count();
                emptySum += isEmptyRow.Select((value, index) => new { value, index }).Where(a => a.value && a.index > Math.Min(galaxies[i].y, galaxies[j].y) && a.index < Math.Max(galaxies[i].y, galaxies[j].y)).Count();
            }
        long part1 = distanceSum + emptySum;
        long part2 = distanceSum + emptySum * (1000000 - 1);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
