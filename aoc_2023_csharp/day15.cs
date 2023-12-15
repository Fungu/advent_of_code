using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day15
{
    public static void Solve() 
    {
        string input = File.ReadAllText("input/day15.txt");
        var stopwatch = Stopwatch.StartNew();

        var boxes = new List<(string label, int focal)>[256];
        for (int i = 0; i < 256; i++)
            boxes[i] = [];

        long part1 = 0;
        foreach (var step in input.Split(','))
        {
            part1 += HashAlgorithm(step);

            char operation = step.Contains('=') ? '=' : '-';
            string label = step.Split(operation)[0];
            var box = boxes[HashAlgorithm(label)];
            int slot = box.FindIndex(s => s.label == label);

            if (operation == '=')
            {
                int focalLength = int.Parse(step.Split(operation)[1]);
                if (slot >= 0)
                    box[slot] = (label, focalLength);
                else
                    box.Add((label, focalLength));
            }
            else if (slot >= 0)
            {
                box.RemoveAt(slot);
            }
        }

        long part2 = 0;
        for (int i = 0; i < 256; i++)
        {
            for (int j = 0; j < boxes[i].Count; j++)
            {
                int focusingPower = 1 + i;
                focusingPower *= (1 + j);
                focusingPower *= boxes[i][j].focal;
                part2 += focusingPower;
            }
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static int HashAlgorithm(string input)
    {
        int currentValue = 0;
        foreach (char c in input)
        {
            currentValue += c;
            currentValue *= 17;
            currentValue %= 256;
        }
        return currentValue;
    }
}
