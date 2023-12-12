using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day12
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day12.txt");
        var stopwatch = Stopwatch.StartNew();

        long part1 = 0;
        long part2 = 0;
        foreach (var line in input)
        {
            var a = line.Split(' ');
            string map = a[0];
            string groups = a[1];

            var groupArray = groups.Split(',').Select(int.Parse).ToArray();
            part1 += CountValid([], map, groupArray, 0, 0);

            string repeatedMap = string.Join('?', Enumerable.Repeat(map, 5));
            string repeatedGroups = string.Join(',', Enumerable.Repeat(groups, 5));
            var repeatedGroupArray = repeatedGroups.Split(',').Select(int.Parse).ToArray();
            part2 += CountValid([], repeatedMap, repeatedGroupArray, 0, 0);
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static long CountValid(Dictionary<object, long> dp, string map, int[] groupSizes, int mapIndex, int groupIndex)
    {
        bool groupsDone = groupIndex == groupSizes.Length;
        bool mapDone = mapIndex == map.Length || map.LastIndexOf('#') < mapIndex;
        if (groupsDone)
        {
            if (mapDone) return 1;
            else return 0;
        }
        object key = (mapIndex, groupIndex);
        if (dp.TryGetValue(key, out long value)) return value;

        long ret = 0;
        for (int i = mapIndex; i + groupSizes[groupIndex] <= map.Length; i++)
        {
            if (map[i] == '#' || map[i] == '?')
            {
                bool groupFits = true;
                for (int j = 0; j < groupSizes[groupIndex]; j++)
                    if (map[i + j] != '#' && map[i + j] != '?')
                    {
                        groupFits = false;
                        break;
                    }
                int groupEndIndex = i + groupSizes[groupIndex];
                if (groupEndIndex != map.Length && map[groupEndIndex] != '.' && map[groupEndIndex] != '?')
                    groupFits = false;
                if (groupFits)
                    ret += CountValid(dp, map, groupSizes, groupEndIndex + 1, groupIndex + 1);
                if (map[i] == '#')
                    break;
            }
        }
        dp.Add(key, ret);
        return ret;
    }
}
