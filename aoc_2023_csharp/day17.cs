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

        int part1 = Search(grid, 0, 3);
        int part2 = Search(grid, 4, 10);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static int Search(int[][] grid, int minSteps, int maxSteps)
    {
        Queue<(int x, int y, int dx, int dy, int steps)> openSet = [];
        Dictionary<(int x, int y, int dx, int dy, int steps), int> closedSet = [];
        openSet.Enqueue((0, 0, 1, 0, 0));
        closedSet.Add((0, 0, 1, 0, 0), 0);
        int ret = int.MaxValue;
        while (openSet.Count > 0)
        {
            (int x, int y, int dx, int dy, int steps) = openSet.Dequeue();
            int heat = closedSet[(x, y, dx, dy, steps)];
            if (x == grid[0].Length - 1 && y == grid.Length - 1 && steps >= minSteps) ret = int.Min(ret, heat);

            List<(int, int, bool)> directions = [];
            if (steps < maxSteps) directions.Add((dx, dy, false));
            if (steps >= minSteps) directions.Add((dy, dx, true));
            if (steps >= minSteps) directions.Add((-dy, -dx, true));
            foreach ((int ndx, int ndy, bool turn) in directions)
            {
                (int nx, int ny) = (x + ndx, y + ndy);
                if (nx >= 0 && ny >= 0 && nx < grid[0].Length && ny < grid.Length)
                {
                    int nsteps = turn ? 1 : steps + 1;
                    int nheat = heat + grid[ny][nx];
                    if (closedSet.TryGetValue((nx, ny, ndx, ndy, nsteps), out int existingHeat))
                    {
                        if (nheat < existingHeat)
                        {
                            if (!openSet.Contains((nx, ny, ndx, ndy, nsteps)))
                                openSet.Enqueue((nx, ny, ndx, ndy, nsteps));
                            closedSet[(nx, ny, ndx, ndy, nsteps)] = nheat;
                        }
                    }
                    else
                    {
                        openSet.Enqueue((nx, ny, ndx, ndy, nsteps));
                        closedSet.Add((nx, ny, ndx, ndy, nsteps), nheat);
                    }
                }
            }
        }
        return ret;
    }
}
