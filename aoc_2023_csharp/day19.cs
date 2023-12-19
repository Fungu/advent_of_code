using System.Diagnostics;
using System.Text.RegularExpressions;

namespace aoc_2023_csharp;

public static class Day19
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day19.txt");
        var stopwatch = Stopwatch.StartNew();

        Regex workflowRegex = new(@"(?<name>.+){(?<rules>.+)}");
        Regex partRegex = new(@"{x=(?<x>[0-9]+),m=(?<m>[0-9]+),a=(?<a>[0-9]+),s=(?<s>[0-9]+)}");
        Dictionary<string, string[]> workflows = [];
        List<Dictionary<string, int>> parts = [];
        bool workflowsDone = false;
        foreach (string line in input)
        {
            if (line.Length == 0)
            {
                workflowsDone = true;
            }
            else if (!workflowsDone)
            {
                Match match = workflowRegex.Match(line);
                workflows.Add(match.Groups["name"].Value, match.Groups["rules"].Value.Split(','));
            }
            else
            {
                Match match = partRegex.Match(line);
                parts.Add(new Dictionary<string, int>(){
                    { "x", int.Parse(match.Groups["x"].Value) },
                    { "m", int.Parse(match.Groups["m"].Value) },
                    { "a", int.Parse(match.Groups["a"].Value) },
                    { "s", int.Parse(match.Groups["s"].Value) }});
            }
        }

        var validRanges = Search(workflows, new Dictionary<string, (int min, int max)> {
            { "x", (1, 4000) },
            { "m", (1, 4000) },
            { "a", (1, 4000) },
            { "s", (1, 4000) }}, "in");

        int part1 = 0;
        foreach (var part in parts)
        {
            foreach (var range in validRanges)
            {
                bool isValid = true;
                foreach (string category in part.Keys)
                {
                    if (part[category] < range[category].min || part[category] > range[category].max)
                    {
                        isValid = false;
                    }
                }
                if (isValid)
                {
                    part1 += part.Values.Sum();
                }
            }
        }

        long part2 = 0;
        foreach (var range in validRanges)
        {
            long area = 1;
            foreach ((int min, int max) in range.Values)
            {
                area *= (1 + max - min);
            }
            part2 += area;
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static List<Dictionary<string, (int min, int max)>> Search(Dictionary<string, string[]> workflows, Dictionary<string, (int min, int max)> ranges, string workflowName)
    {
        List<Dictionary<string, (int min, int max)>> ret = [];
        var miss = new Dictionary<string, (int min, int max)>(ranges);
        foreach (var unparsedStep in workflows[workflowName])
        {
            var match = new Dictionary<string, (int min, int max)>(miss);
            string destination;
            if (unparsedStep.Contains(':'))
            {
                string left = unparsedStep.Split(':')[0];
                string op = left.Contains('<') ? "<" : ">";
                string category = left.Split(op)[0];
                int value = int.Parse(left.Split(op)[1]);
                destination = unparsedStep.Split(':')[1];
                if (op == "<")
                {
                    match[category] = (miss[category].min, int.Min(miss[category].max, value - 1));
                    miss[category] = (int.Max(miss[category].min, value), miss[category].max);
                }
                else if (op == ">")
                {
                    match[category] = (int.Max(miss[category].min, value + 1), miss[category].max);
                    miss[category] = (miss[category].min, int.Min(miss[category].max, value));
                }
            }
            else
            {
                destination = unparsedStep;
                miss["x"] = (-1, 1);
            }

            if (IsValidRange(match))
            {
                if (destination == "A")
                {
                    ret.Add(match);
                }
                else if (destination != "R")
                {
                    ret.AddRange(Search(workflows, match, destination));
                }
            }
            if (!IsValidRange(miss))
            {
                break;
            }
        }
        return ret;
    }

    private static bool IsValidRange(Dictionary<string, (int min, int max)> ranges)
    {
        foreach ((int min, int max) in ranges.Values)
            if (min > max)
                return false;
        return true;
    }
}
