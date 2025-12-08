using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day08
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day08.txt");
        var stopwatch = Stopwatch.StartNew();

        // Parse the junctions
        List<(int, int, int)> junctions = [];
        foreach (string line in lines)
        {
            var parsed = line.Split(",").Select(x => int.Parse(x)).ToArray();
            junctions.Add((parsed[0], parsed[1], parsed[2]));
        }

        // Calculate the distance between each pair of junctions, then sort by distance
        List<(int, int, double)> distances = [];
        for (int i = 0; i < junctions.Count; i++)
        {
            for (int j = i + 1; j < junctions.Count; j++)
            {
                distances.Add((i, j, DistanceSquared(junctions[i], junctions[j])));
            }
        }
        distances.Sort((a, b) => a.Item3.CompareTo(b.Item3));

        // Connect the closest 1000 junctions into circuits
        List<List<int>> circuits = [];
        for (int i = 0; i < junctions.Count; i++)
        {
            circuits.Add([i]);
        }
        for (int i = 0; i < 1000; i++)
        {
            int indexA = FindIndex(circuits, distances[i].Item1);
            int indexB = FindIndex(circuits, distances[i].Item2);
            if (indexA == indexB)
            {
                continue;
            }
            circuits[indexA].AddRange(circuits[indexB]);
            circuits.RemoveAt(indexB);
        }
        circuits.Sort((a, b) => b.Count.CompareTo(a.Count));
        long part1 = circuits[0].Count * circuits[1].Count * circuits[2].Count;

        // Keep connecting into circuits until everything is in one circuit
        long part2 = 0;
        for (int i = 1000; ; i++)
        {
            int indexA = FindIndex(circuits, distances[i].Item1);
            int indexB = FindIndex(circuits, distances[i].Item2);
            if (indexA == indexB)
            {
                continue;
            }
            circuits[indexA].AddRange(circuits[indexB]);
            circuits.RemoveAt(indexB);
            if (circuits.Count == 1)
            {
                part2 = (long)junctions[distances[i].Item1].Item1 * (long)junctions[distances[i].Item2].Item1;
                break;
            }
        }
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static double DistanceSquared((int, int, int) a, (int, int, int) b)
    {
        return Math.Pow(a.Item1 - b.Item1, 2) + Math.Pow(a.Item2 - b.Item2, 2) + Math.Pow(a.Item3 - b.Item3, 2);
    }

    static int FindIndex(List<List<int>> circuits, int a)
    {
        for (int i = 0; i < circuits.Count; i++)
        {
            if (circuits[i].Contains(a))
            {
                return i;
            }
        }
        return -1;
    }
}
