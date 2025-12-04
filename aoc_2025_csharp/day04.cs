using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day04
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day04.txt");
        var stopwatch = Stopwatch.StartNew();

        bool[,] grid = new bool[lines.Length, lines[0].Length];
        for (int y = 0; y < lines.Length; y++)
            for (int x = 0; x < lines[y].Length; x++)
                grid[y, x] = lines[y][x] == '@';
        
        int part1 = ConsiderDiagram(grid, false);
        
        int part2 = 0;
        int rollsRemoved = -1;
        while (rollsRemoved != 0)
        {
            rollsRemoved = ConsiderDiagram(grid, true);
            part2 += rollsRemoved;
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static int ConsiderDiagram(bool[,] grid, bool allowRemove)
    {
        int accessibleRolls = 0;
        for (int y = 0; y < grid.GetLength(0); y++)
        {
            for (int x = 0; x < grid.GetLength(1); x++)
            {
                if (!IsPaper(grid, x, y)) continue;
                int PaperNeighbors = 0;
                for (int yy = -1; yy <= 1; yy++)
                {
                    for (int xx = -1; xx <= 1; xx++)
                    {
                        if (xx == 0 && yy == 0) continue;
                        PaperNeighbors += IsPaper(grid, x + xx, y + yy) ? 1 : 0;
                    }
                }
                if (PaperNeighbors < 4)
                {
                    accessibleRolls++;
                    if (allowRemove)
                    {
                        grid[y, x] = false;
                    }
                }
            }
        }
        return accessibleRolls;
    }

    static bool IsPaper(bool[,] grid, int x, int y)
    {
        if (x < 0 || y < 0 || x >= grid.GetLength(1) || y >= grid.GetLength(0))
        {
            return false;
        }
        return grid[y, x];
    }
}
