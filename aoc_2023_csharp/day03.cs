using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day03
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day03.txt");
        var stopwatch = Stopwatch.StartNew();

        string[][] grid = new string[input.Length][];
        for (int i = 0; i < input.Length; i++)
            grid[i] = input[i].ToCharArray().Select(c => c.ToString()).ToArray();

        int part1 = 0;
        int part2 = 0;
        var gears = new Dictionary<(int, int), List<int>>();
        for (int y = 0; y < grid.Length; y++)
        {
            for (int x = 0; x < grid[y].Length; x++)
            {
                int startX = x;
                int number = 0;
                while (x < grid[y].Length && int.TryParse(grid[y][x], out int i))
                {
                    number *= 10;
                    number += i;
                    x++;
                }
                if (number > 0)
                {
                    var neighbors = new List<(int, int)>
                    {
                        (startX - 1, y),
                        (x, y)
                    };
                    for (int xx = startX - 1; xx <= x; xx++)
                    {
                        neighbors.Add((xx, y - 1));
                        neighbors.Add((xx, y + 1));
                    }
                    bool isPart = false;
                    foreach (var neighbor in neighbors)
                    {
                        string s = GetSymbol(grid, neighbor.Item1, neighbor.Item2);
                        if (s == "*")
                        {
                            if (!gears.ContainsKey(neighbor))
                                gears.Add(neighbor, []);
                            gears[neighbor].Add(number);
                        }
                        isPart |= s != "";
                    }

                    if (isPart)
                        part1 += number;
                }
            }
        }
        foreach (List<int> gear in gears.Values)
            if (gear.Count == 2)
                part2 += gear[0] * gear[1];

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static string GetSymbol(string[][] grid, int x, int y)
    {
        if (x < 0 || x >= grid[0].Length || y < 0 || y >= grid.Length) 
            return "";
        string s = grid[y][x];
        if (s != "." && !int.TryParse(s, out int _))
            return s;
        else
            return "";
    }
}
