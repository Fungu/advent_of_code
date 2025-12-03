using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day03
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day03.txt");
        var stopwatch = Stopwatch.StartNew();

        long part1 = 0;
        long part2 = 0;
        
        foreach (string line in input)
        {
            part1 += GetVoltage(line, 2);
            part2 += GetVoltage(line, 12);
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static long GetVoltage(string line, int numberOfBatteries)
    {
        int[] batteries = new int[numberOfBatteries];
        for (int i = 0; i < batteries.Length; i++)
        {
            batteries[i] = (int)line[line.Length + i - batteries.Length] - 48;
        }
        for (int i = line.Length - 1 - batteries.Length; i >= 0; i--)
        {
            int nextBattery = (int)line[i] - 48;
            for (int j = 0; j < batteries.Length; j++)
            {
                if (nextBattery >= batteries[j])
                {
                    // Use tuple to swap values (IDE0180)
                    (nextBattery, batteries[j]) = (batteries[j], nextBattery);
                }
                else
                {
                    break;
                }
            }
        }
        long temp = 0;
        for (int i = 0; i < batteries.Length; i++)
        {
            temp *= 10;
            temp += batteries[i];
        }
        return temp;
    }
}
