using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day02
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day02.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        int part2 = 0;
        var limits = new Dictionary<string, int>
        {
            { "red", 12 },
            { "green", 13 },
            { "blue", 14 }
        };
        foreach (string line in input)
        {
            var minCubes = new Dictionary<string, int>
            {
                { "red", 0 },
                { "green", 0 },
                { "blue", 0 }
            };
            bool withinLimits = true;
            int id = int.Parse(line.Split(": ")[0].Split(" ")[1]);
            string games = line.Split(": ")[1];
            foreach (string set in games.Split("; "))
            {
                foreach (string cube in set.Split(", "))
                {
                    int number = int.Parse(cube.Split(" ")[0]);
                    string color = cube.Split(" ")[1];
                    if (number > limits[color])
                        withinLimits = false;
                    minCubes[color] = Math.Max(minCubes[color], number);
                }
            }
            if (withinLimits)
                part1 += id;
            part2 += minCubes["red"] * minCubes["green"] * minCubes["blue"];
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
