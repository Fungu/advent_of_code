using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day02
{
    public static void Solve() 
    {
        string input = File.ReadAllText("C:/Dropbox/advent_of_code/2025/day02.txt");
        var stopwatch = Stopwatch.StartNew();

        long part1 = 0;
        long part2 = 0;
        
        string[] ranges = input.Split(',');
        foreach (string range in ranges)
        {
            string[] ids = range.Split('-');
            long firstId = long.Parse(ids[0]);
            long lastId = long.Parse(ids[1]);
            for (long id = firstId; id <= lastId; id++)
            {
                string idString = "" + id;
                int middle = idString.Length / 2;
                if (idString.Length % 2 == 0 && idString[0..middle] == idString[middle..]) 
                    part1 += id;
                
                for (int chunkSize = 1; chunkSize <= middle; chunkSize++)
                {
                    if (idString.Length % chunkSize != 0) 
                        continue;
                    bool foundNonRepeating = false;
                    for (int i = 1; i < idString.Length / chunkSize; i++)
                    {
                        if (idString[(i * chunkSize)..((i + 1) * chunkSize)] != idString[..chunkSize])
                        {
                            foundNonRepeating = true;
                            break;
                        }
                    }
                    if (!foundNonRepeating)
                    {
                        part2 += id;
                        break;
                    }
                }
            }
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }
}
