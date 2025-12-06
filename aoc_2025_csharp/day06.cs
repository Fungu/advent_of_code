using System.Diagnostics;
using System.Text.RegularExpressions;

namespace aoc_2025_csharp;

public static class Day06
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day06.txt");
        var stopwatch = Stopwatch.StartNew();

        long part1 = 0;

        int width = Regex.Split(lines[0].Trim(), @" +").Length;
        long[,] problemNumbers = new long[lines.Length - 1, width];
        for (int y = 0; y < lines.Length - 1; y++)
        {
            string[] s = Regex.Split(lines[y].Trim(), @" +");
            for (int x = 0; x < width; x++)
            {
                problemNumbers[y, x] = long.Parse(s[x]);
            }
        }
        string[] problemOperators = Regex.Split(lines[lines.Length - 1].Trim(), @" +");
        
        for (int x = 0; x < width; x++)
        {
            if (problemOperators[x] == "+")
            {
                long result = 0;
                for (int y = 0; y < lines.Length - 1; y++)
                {
                    result += problemNumbers[y, x];
                }
                part1 += result;
            }
            else
            {
                long result = 1;
                for (int y = 0; y < lines.Length - 1; y++)
                {
                    result *= problemNumbers[y, x];
                }
                part1 += result;
            }
        }

        long part2 = 0;
        char op = ' ';
        List<long> numbers = [];
        for (int x = 0; x < lines[0].Length; x++)
        {
            string column = "";
            for (int y = 0; y < lines.Length - 1; y++)
            {
                column += lines[y][x];
            }
            if (column.Trim().Length == 0)
            {
                if (op == '+')
                {
                    part2 += numbers.Aggregate((a, b) => a + b);
                }
                else
                {
                    part2 += numbers.Aggregate((a, b) => a * b);
                }
                numbers = [];
                op = ' ';
            }
            else
            {
                numbers.Add(long.Parse(column));
                op = op == ' ' ? lines[^1][x] : op;
            }
        }
        if (op == '+')
        {
            part2 += numbers.Aggregate((a, b) => a + b);
        }
        else
        {
            part2 += numbers.Aggregate((a, b) => a * b);
        }
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
