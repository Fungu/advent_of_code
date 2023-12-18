using System.Diagnostics;
using System.Globalization;

namespace aoc_2023_csharp;

public static class Day18
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day18.txt");
        var stopwatch = Stopwatch.StartNew();

        List<(long x, long y)> vertices = [];
        long x = 0;
        long y = 0;
        long totalSteps = 0;
        foreach (string line in input)
        {
            string dir = line.Split(" ")[0];
            int steps = int.Parse(line.Split(" ")[1]);
            totalSteps += steps;
            if (dir == "R") x += steps;
            if (dir == "D") y += steps;
            if (dir == "L") x -= steps;
            if (dir == "U") y -= steps;
            vertices.Add((x, y));
        }
        totalSteps /= 2;
        long part1 = ShoelaceArea(vertices) + totalSteps + 1;

        vertices = [];
        x = 0;
        y = 0;
        totalSteps = 0;
        foreach (string line in input)
        {
            char dir = line.Split(" ")[2][7];
            long steps = long.Parse(line.Split(" ")[2].Substring(2, 5), NumberStyles.HexNumber);
            totalSteps += steps;
            if (dir == '0') x += steps;
            if (dir == '1') y += steps;
            if (dir == '2') x -= steps;
            if (dir == '3') y -= steps;
            vertices.Add((x, y));
        }
        totalSteps /= 2;
        long part2 = ShoelaceArea(vertices) + totalSteps + 1;

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static long ShoelaceArea(List<(long x, long y)> vertices)
    {
        long area = 0;
        for (int i = 0; i < vertices.Count - 1; i++)
        {
            area += vertices[i].x * vertices[i + 1].y;
            area -= vertices[i].y * vertices[i + 1].x;
        }
        area += vertices[^1].x * vertices[0].y;
        area -= vertices[^1].y * vertices[0].x;
        area = Math.Abs(area);
        area /= 2;
        return area;
    }
}
