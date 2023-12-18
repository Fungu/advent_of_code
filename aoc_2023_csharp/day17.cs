using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day17
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day17.txt");
        var stopwatch = Stopwatch.StartNew();

        int[][] grid = new int[input.Length][];
        for (int i = 0; i < input.Length; i++)
            grid[i] = input[i].Select(a => int.Parse(a.ToString())).ToArray();

        int part1 = Search(grid, 1, 3);
        int part2 = Search(grid, 4, 10);
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static int Search(int[][] grid, int minSteps, int maxSteps)
    {
        int width = grid[0].Length;
        int height = grid.Length;
        Queue<(int x, int y, bool vertical)> openSet = [];
        Dictionary<(int x, int y, bool vertical), int> closedSet = [];
        openSet.Enqueue((0, 0, true));
        openSet.Enqueue((0, 0, false));
        closedSet.Add((0, 0, true), 0);
        closedSet.Add((0, 0, false), 0);
        while (openSet.Count > 0)
        {
            (int x, int y, bool vertical) = openSet.Dequeue();
            int heat = closedSet[(x, y, vertical)];
            (int x, int y)[] directions;
            if (vertical)
                directions = [(1, 0), (-1, 0)];
            else
                directions = [(0, 1), (0, -1)];
            foreach ((int dx, int dy) in directions)
            {
                int subHeat = 0;
                (int nx, int ny) = (x, y);
                for (int step = 1; step <= maxSteps; step++)
                {
                    nx += dx;
                    ny += dy;
                    if (nx < 0 || ny < 0 || nx >= width || ny >= height) break;
                    subHeat += grid[ny][nx];
                    if (step >= minSteps)
                    {
                        if (closedSet.TryGetValue((nx, ny, !vertical), out int existingHeat))
                        {
                            if (heat + subHeat < existingHeat)
                            {
                                if (!openSet.Contains((nx, ny, !vertical)))
                                    openSet.Enqueue((nx, ny, !vertical));
                                closedSet[(nx, ny, !vertical)] = heat + subHeat;
                            }
                        }
                        else
                        {
                            openSet.Enqueue((nx, ny, !vertical));
                            closedSet.Add((nx, ny, !vertical), heat + subHeat);
                        }
                    }
                }
            }
        }
        return int.Min(
            closedSet[(width - 1, height - 1, true)], 
            closedSet[(width - 1, height - 1, false)]);
    }
}
