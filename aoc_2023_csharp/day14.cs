using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day14
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day14.txt");
        var stopwatch = Stopwatch.StartNew();

        char[][] grid = new char[input.Length][];
        for (int i = 0; i < input.Length; i++)
            grid[i] = input[i].ToCharArray();

        Dictionary<string, int> gridToCycleHistory = [];
        Dictionary<int, string> cycleToGridHistory = [];
        int cycle = 0;
        AddToHistory(gridToCycleHistory, cycleToGridHistory, cycle++, GetGridKey(grid));

        Tilt(grid, (0, -1));
        long part1 = GetLoad(grid);
        Tilt(grid, (-1, 0));
        Tilt(grid, (0, 1));
        Tilt(grid, (1, 0));
        AddToHistory(gridToCycleHistory, cycleToGridHistory, cycle++, GetGridKey(grid));
        
        int longEnough = 1000000000;
        while (true)
        {
            Tilt(grid, (0, -1));
            Tilt(grid, (-1, 0));
            Tilt(grid, (0, 1));
            Tilt(grid, (1, 0));
            string key = GetGridKey(grid);
            if (gridToCycleHistory.TryGetValue(key, out int loopStart))
            {
                int loopLength = cycle - loopStart;
                int remainder = (longEnough - loopStart) % loopLength;
                
                string[] rows = cycleToGridHistory[loopStart + remainder].Split(",");
                for (int y = 0; y < rows.Length; y++)
                    grid[y] = rows[y].ToCharArray();
                break;
            }
            AddToHistory(gridToCycleHistory, cycleToGridHistory, cycle++, GetGridKey(grid));
        }
        long part2 = GetLoad(grid);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static void Tilt(char[][] grid, (int x, int y) direction)
    {
        bool everythingSettled = false;
        while (!everythingSettled)
        {
            everythingSettled = true;
            for (int y = 0; y < grid.Length; y++)
            {
                for (int x = 0; x < grid[y].Length; x++)
                {
                    (int nx, int ny) = (x + direction.x, y + direction.y);
                    if (IsValidPos(nx, ny, grid[y].Length, grid.Length) && grid[y][x] == 'O' && grid[ny][nx] == '.')
                    {
                        grid[y][x] = '.';
                        while (IsValidPos(nx, ny, grid[y].Length, grid.Length) && grid[ny][nx] == '.')
                            (nx, ny) = (nx + direction.x, ny + direction.y);
                        (nx, ny) = (nx - direction.x, ny - direction.y);
                        grid[ny][nx] = 'O';
                        everythingSettled = false;
                    }
                }
            }
        }
    }

    private static int GetLoad(char[][] grid)
    {
        int load = 0;
        for (int y = 0; y < grid.Length; y++)
            for (int x = 0; x < grid[y].Length; x++)
                if (grid[y][x] == 'O')
                    load += grid.Length - y;
        return load;
    }

    private static void AddToHistory(Dictionary<string, int> gridToCycleHistory, Dictionary<int, string> cycleToGridHistory, int cycle, string key)
    {
        cycleToGridHistory.Add(cycle, key);
        gridToCycleHistory.Add(key, cycle);
    }

    private static string GetGridKey(char[][] grid)
    {
        return string.Join(",", grid.Select(a => string.Join("", a)));
    }

    private static bool IsValidPos(int x, int y, int gridWidth, int gridHeight)
    {
        return x >= 0 && y >= 0 && x < gridWidth && y < gridHeight;
    }
}
