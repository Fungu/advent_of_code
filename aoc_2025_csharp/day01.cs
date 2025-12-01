using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day01
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day01.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        int part2 = 0;
        int dial = 50;
        foreach (string line in input)
        {
            int steps = int.Parse(line[1..]);
            
            if (dial == 0 && line[0] == 'L')
                part2--;
            
            if (line[0] == 'R')
                dial += steps;
            else
                dial -= steps;
            
            while (dial < 0) 
            {
                dial += 100;
                part2++;
            }
            while (dial > 99)
            {
                dial -= 100;
                part2++;
            }
            
            if (dial == 0 && line[0] == 'R')
                part2--;
            
            if (dial == 0)
            {
                part1++;
                part2++;
            }
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
