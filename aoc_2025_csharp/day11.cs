using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day11
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day11.txt");
        var stopwatch = Stopwatch.StartNew();

        Dictionary<string, string[]> devices = [];
        foreach (string line in lines)
        {
            devices.Add(line.Split(": ")[0], line.Split(": ")[1].Split(" "));
        }

        int part1 = CountPaths("you", devices, new Dictionary<string, int>());
        long part2 = CountPaths2("svr", false, false, devices, new Dictionary<(string, bool, bool), long>());
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static int CountPaths(string pos, Dictionary<string, string[]> devices, Dictionary<string, int> dp)
    {
        if (pos == "out")
        {
            return 1;
        }
        if (dp.TryGetValue(pos, out int value))
        {
            return value;
        }

        int paths = 0;
        foreach (string output in devices[pos])
        {
            paths += CountPaths(output, devices, dp);
        }

        dp.Add(pos, paths);
        return paths;
    }

    static long CountPaths2(string pos, bool visitedDac, bool visitedFft, Dictionary<string, string[]> devices, Dictionary<(string, bool, bool), long> dp)
    {
        if (pos == "dac") visitedDac = true;
        if (pos == "fft") visitedFft = true;
        if (pos == "out") return visitedDac && visitedFft ? 1 : 0;

        if (dp.TryGetValue((pos, visitedDac, visitedFft), out long value))
        {
            return value;
        }
        
        long paths = 0;
        foreach (string output in devices[pos])
        {
            paths += CountPaths2(output, visitedDac, visitedFft, devices, dp);
        }

        dp.Add((pos, visitedDac, visitedFft), paths);
        return paths;
    }

}
