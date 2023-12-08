using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day08
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day08.txt");
        var stopwatch = Stopwatch.StartNew();

        char[] sequence = input[0].ToCharArray();
        Dictionary<string, (string, string)> nodes = [];
        List<string> startGhost = [];
        for (int i = 2; i < input.Length; i++)
        {
            string[] a = input[i].Split(" = ");
            string[] b = a[1].Split(", ");
            nodes.Add(a[0], (b[0].Replace("(", ""), b[1].Replace(")", "")));
            if (a[0].EndsWith('A'))
                startGhost.Add(a[0]);
        }

        int part1 = 0;
        string current = "AAA";
        for (int i = 0; current != "ZZZ"; i++)
        {
            if (i >= sequence.Length) i = 0;
            part1++;
            if (sequence[i] == 'L')
                current = nodes[current].Item1;
            else
                current = nodes[current].Item2;
        }

        List<long> loopStart = [];
        List<long> loopLength = [];
        List<long> targetPos = [];
        for (int a = 0; a < startGhost.Count; a++)
        {
            List<string> seen = [];
            string ghost = startGhost[a];
            int counter = 0;
            for (int i = 0; ; i++)
            {
                if (i >= sequence.Length) i = 0;
                if (ghost.EndsWith('Z'))
                {
                    targetPos.Add(counter);
                }
                if (seen.Contains(ghost + i))
                {
                    loopStart.Add(seen.IndexOf(ghost + i));
                    loopLength.Add(counter - seen.IndexOf(ghost + i));
                    break;
                }
                seen.Add(ghost + i);

                counter++;
                if (sequence[i] == 'L')
                    ghost = nodes[ghost].Item1;
                else
                    ghost = nodes[ghost].Item2;
            }
        }

        long gcd = loopLength[0];
        for (int i = 1; i < loopLength.Count; i++)
        {
            gcd = GCD(gcd, loopLength[i]);
            if (loopLength[i] != targetPos[i])
                throw new Exception("I assume that the target is at the end of the loops.");
        }

        long part2 = 1;
        for (int i = 0; i < loopLength.Count; i++)
            part2 *= loopLength[i] / gcd;
        part2 *= gcd;

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static long GCD(long a, long b)
    {
        while (a != 0 && b != 0)
        {
            if (a > b)
                a %= b;
            else
                b %= a;
        }

        return a | b;
    }
}
