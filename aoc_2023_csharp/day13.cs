using System.Diagnostics;
using System.IO;

namespace aoc_2023_csharp;

public static class Day13
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day13.txt");
        var stopwatch = Stopwatch.StartNew();

        long part1 = 0;
        long part2 = 0;

        List<string> pattern = [];
        for (int i = 0; i < input.Length + 1; i++)
        {
            if (i == input.Length || input[i].Length == 0)
            {
                var columns = GetColumns(pattern);

                if (GetCenter(pattern, false, out int row))
                    part1 += 100 * (row + 1);
                else if (GetCenter(columns, false, out int column))
                    part1 += column + 1;

                if (GetCenter(pattern, true, out int row2))
                    part2 += 100 * (row2 + 1);
                else if (GetCenter(columns, true, out int column))
                    part2 += column + 1;
                
                pattern.Clear();
            }
            else
            {
                pattern.Add(input[i]);
            }
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static bool GetCenter(List<string> pattern, bool fixSmudge, out int center)
    {
        for (int x = 0; x < pattern.Count - 1; x++)
        {
            bool isValidCenter = true;
            bool needToFixSmudge = fixSmudge;
            for (int a = 0; x - a >= 0 && 1 + x + a < pattern.Count; a++)
            {
                int differences = CountDifferences(pattern[x - a], pattern[1 + x + a]);
                if (differences == 1 && needToFixSmudge)
                {
                    needToFixSmudge = false;
                }
                else if (differences > 0)
                {
                    isValidCenter = false;
                    break;
                }
            }
            if (isValidCenter && !needToFixSmudge)
            {
                center = x;
                return true;
            }
        }
        center = -1;
        return false;
    }

    private static List<string> GetColumns(List<string> pattern)
    {
        List<string> ret = [];
        for (int i = 0; i < pattern[0].Length; i++)
        {
            string column = "";
            for (int a = 0; a < pattern.Count; a++)
            {
                column += pattern[a][i];
            }
            ret.Add(column);
        }
        return ret;
    }

    private static int CountDifferences(string a, string b)
    {
        int differences = 0;
        for (int i = 0; i < a.Length; i++)
            if (a[i] != b[i])
                differences++;
        return differences;
    }
}
