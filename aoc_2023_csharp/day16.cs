using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day16
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day16.txt");
        var stopwatch = Stopwatch.StartNew();

        int gridWidth = input[0].Length;
        int gridHeight = input.Length;

        int part1 = Simulate(input, (0, 0), (1, 0));
        int part2 = 0;
        for (int x = 0; x < gridWidth; x++)
        {
            part2 = Math.Max(part2, Simulate(input, (x, 0), (0, 1)));
            part2 = Math.Max(part2, Simulate(input, (x, gridHeight - 1), (0, -1)));
        }
        for (int y = 0; y < gridHeight; y++)
        {
            part2 = Math.Max(part2, Simulate(input, (0, y), (1, 0)));
            part2 = Math.Max(part2, Simulate(input, (gridWidth - 1, y), (-1, 0)));
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static int Simulate(string[] input, (int x, int y) startPos, (int x, int y) startDir)
    {
        HashSet<(int, int)> energized = [];
        HashSet<((int, int), (int, int))> closedSet = [];
        List<(int x, int y)> pos = [startPos];
        List<(int x, int y)> dir = [startDir];

        while (pos.Count > 0)
        {
            if (closedSet.Contains((pos[0], dir[0])))
            {
                pos.RemoveAt(0);
                dir.RemoveAt(0);
                continue;
            }
            energized.Add(pos[0]);
            char c = input[pos[0].y][pos[0].x];
            if (c != '.')
                closedSet.Add((pos[0], dir[0]));

            if (c == '/')
            {
                dir[0] = (-dir[0].y, -dir[0].x);
            }
            else if (c == '\\')
            {
                dir[0] = (dir[0].y, dir[0].x);
            }
            else if (c == '|' && dir[0].x != 0)
            {
                dir[0] = (0, -1);
                dir.Add((0, 1));
                pos.Add((pos[0].x, pos[0].y));
            }
            else if (c == '-' && dir[0].y != 0)
            {
                dir[0] = (-1, 0);
                dir.Add((1, 0));
                pos.Add((pos[0].x, pos[0].y));
            }

            (int nx, int ny) = (pos[0].x + dir[0].x, pos[0].y + dir[0].y);
            if (nx >= 0 && ny >= 0 && nx < input[0].Length && ny < input.Length)
            {
                pos[0] = (nx, ny);
            }
            else
            {
                pos.RemoveAt(0);
                dir.RemoveAt(0);
            }
        }

        return energized.Count;
    }

    private static void PrintGrid(char[][] grid, List<(int x, int y)> beamPos, List<(int x, int y)> beamDir)
    {
        for (int y = 0; y < grid.Length; y++)
        {
            for (int x = 0; x < grid[0].Length; x++)
            {
                int beamIndex = beamPos.IndexOf((x, y));
                if (beamIndex > -1)
                {
                    if (beamDir[beamIndex] == (1, 0)) Console.Write('>');
                    if (beamDir[beamIndex] == (-1, 0)) Console.Write('<');
                    if (beamDir[beamIndex] == (0, 1)) Console.Write('v');
                    if (beamDir[beamIndex] == (0, -1)) Console.Write('^');
                }
                else
                {
                    Console.Write(grid[y][x]);
                }
            }
            Console.WriteLine();
        }
    }
}
