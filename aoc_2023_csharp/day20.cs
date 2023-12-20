using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day20
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day20.txt");
        var stopwatch = Stopwatch.StartNew();

        var modules = new Dictionary<string, (char type, string[] destinations)>();
        var flipflopState = new Dictionary<string, bool>();
        var conjunctionState = new Dictionary<string, Dictionary<string, bool>>();
        foreach (var line in input)
        {
            char type = line[0];
            string name = line.Split(" -> ")[0].Substring(1);
            string[] destinations = line.Split(" -> ")[1].Split(", ");
            if (type == 'b')
                name = line.Split(" -> ")[0];
            modules.Add(name, (type, destinations));
            if (type == '%')
                flipflopState.Add(name, false);
        }
        foreach (var name in modules.Keys)
        {
            if (modules[name].type == '&')
            {
                Dictionary<string, bool> inputs = [];
                foreach (var otherName in modules.Keys)
                    if (modules[otherName].destinations.Contains(name))
                        inputs.Add(otherName, false);
                conjunctionState.Add(name, inputs);
            }
        }

        string adjacentConjunction = modules.First(a => a.Value.destinations[0] == "rx").Key;
        List<string> targetConjunctions = modules.Where(a => a.Value.destinations.Contains(adjacentConjunction)).Select(a => a.Key).ToList();
        Dictionary<string, int> loopLengths = [];

        int numberOfLow = 0;
        int numberOfHigh = 0;
        var pulses = new Queue<(string, string, bool)>();
        for (int i = 0; loopLengths.Count != targetConjunctions.Count; i++)
        {
            pulses.Enqueue(("broadcaster", "", false));
            while (pulses.Count > 0)
            {
                (string module, string source, bool high) = pulses.Dequeue();
                if (i < 1000)
                {
                    if (high) numberOfHigh++;
                    else numberOfLow++;
                }

                if (module == "rx")
                {
                    continue;
                }

                // Flip-flop
                if (modules[module].type == '%')
                {
                    // If a flip - flop module receives a high pulse, it is ignored and nothing happens. 
                    if (!high)
                    {
                        // However, if a flip-flop module receives a low pulse, it flips between on and off.
                        // If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse.
                        flipflopState[module] = !flipflopState[module];
                        foreach (var dest in modules[module].destinations)
                        {
                            pulses.Enqueue((dest, module, flipflopState[module]));
                        }
                    }
                }
                // Conjunction
                else if (modules[module].type == '&')
                {
                    // Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules;
                    // they initially default to remembering a low pulse for each input.
                    // When a pulse is received, the conjunction module first updates its memory for that input.
                    conjunctionState[module][source] = high;
                    // Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
                    bool allHigh = conjunctionState[module].Values.All(a => a);
                    foreach (var dest in modules[module].destinations)
                    {
                        pulses.Enqueue((dest, module, !allHigh));
                        if (!allHigh && targetConjunctions.Contains(module) && !loopLengths.ContainsKey(module))
                        {
                            loopLengths[module] = i + 1;
                        }
                    }
                }
                // Broadcaster
                else
                {
                    foreach (var dest in modules[module].destinations)
                    {
                        pulses.Enqueue((dest, module, high));
                    }
                }
            }
        }

        int part1 = numberOfLow * numberOfHigh;
        long part2 = 1;
        foreach (long loopLength in loopLengths.Values)
            part2 = LCM(part2, loopLength);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static long LCM(long a, long b)
    {
        long num1, num2;
        if (a > b)
        {
            num1 = a; num2 = b;
        }
        else
        {
            num1 = b; num2 = a;
        }

        for (int i = 1; i < num2; i++)
        {
            long mult = num1 * i;
            if (mult % num2 == 0)
            {
                return mult;
            }
        }
        return num1 * num2;
    }
}
