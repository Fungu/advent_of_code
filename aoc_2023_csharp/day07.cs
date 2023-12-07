using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day07
{
    static readonly Dictionary<char, int> values = new()
    {
        { 'A', 14 },
        { 'K', 13 },
        { 'Q', 12 },
        { 'J', 11 },
        { 'T', 10 },
        { '9', 9 },
        { '8', 8 },
        { '7', 7 },
        { '6', 6 },
        { '5', 5 },
        { '4', 4 },
        { '3', 3 },
        { '2', 2 }
    };

    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day07.txt");
        var stopwatch = Stopwatch.StartNew();

        List<(char[], int)> parsedInput = [];
        foreach (var line in input)
            parsedInput.Add((line.Split(' ')[0].ToCharArray(), int.Parse(line.Split(' ')[1])));
        
        int part1 = PlayHands(parsedInput, false);
        int part2 = PlayHands(parsedInput, true);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static int PlayHands(List<(char[], int)> input, bool useJokers)
    {
        SortedDictionary<int, int> handScores = [];
        foreach (var line in input)
            handScores.Add(GetHandValue(line.Item1, useJokers), line.Item2);
        int rank = 1;
        int ret = 0;
        foreach (var c in handScores.Keys)
        {
            ret += rank * handScores[c];
            rank++;
        }
        return ret;
    }

    private static int GetHandValue(char[] hand, bool useJokers)
    {
        Dictionary<char, int> occurances = [];
        int score = 0;
        foreach (var c in hand)
        {
            if (!occurances.ContainsKey(c))
                occurances[c] = 0;
            occurances[c]++;
            score *= 17;
            if (!useJokers || c != 'J')
                score += values[c];
        }
        int jokers = 0;
        if (useJokers)
        {
            jokers = occurances.GetValueOrDefault('J');
            occurances['J'] = 0;
        }
        int maxPlusJokers = occurances.Values.Max() + jokers;
        if (maxPlusJokers == 5)
            score += 90000000;
        else if (maxPlusJokers == 4)
            score += 80000000;
        else if (occurances.ContainsValue(3) && occurances.ContainsValue(2))
            score += 70000000;
        else if (jokers == 1 && occurances.Where(a => a.Value == 2).Count() == 2)
            score += 70000000;
        else if (maxPlusJokers == 3)
            score += 60000000;
        else if (occurances.Where(a => a.Value == 2).Count() == 2)
            score += 50000000;
        else if (maxPlusJokers == 2)
            score += 40000000;

        return score;
    }
}
