using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day12
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day12_test.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        List<List<bool[,]>> presents = [];
        List<int> presentSizes = [];
        for (int i = 0; i < lines.Length;)
        {
            if (!lines[i].Contains('x'))
            {
                List<bool[,]> presentNext = [];
                bool[,] present = new bool[3,3];
                int presentSize = 0;
                for (int y = 0; y < 3; y++)
                {
                    for (int x = 0; x < 3; x++)
                    {
                        present[y, x] = lines[i + y + 1][x] == '#';
                        presentSize += lines[i + y + 1][x] == '#' ? 1 : 0;
                    }
                }
                presentSizes.Add(presentSize);
                for (int a = 0; a < 4; a++)
                {
                    presentNext.Add(present);
                    presentNext.Add(FlipH(present));
                    present = RotateCW(present);
                }
                presents.Add(presentNext);
                i += 5;
            }
            else
            {
                string left = lines[i].Split(": ")[0];
                string right = lines[i].Split(": ")[1];
                int width = int.Parse(left.Split("x")[0]);
                int height = int.Parse(left.Split("x")[1]);
                int[] presentsLeft = right.Split(" ").Select(s => int.Parse(s)).ToArray();
                int totalPresentSizes = 0;
                for (int a = 0; a < presentsLeft.Length; a++)
                {
                    totalPresentSizes += presentsLeft[a] * presentSizes[a];
                }
                if ((int)(width / 3) * (int)(height / 3) >= presentsLeft.Sum())
                {
                    // There is enough space to place the presents without any finesse
                    part1++;
                }
                else if (width * height < totalPresentSizes)
                {
                    // There is not enough space regardless of the present configuration
                }
                else
                {
                    // This never happens for my input
                    bool[,] region = new bool[width, height];
                    part1 += TryPlaceEverything(presents, region, presentsLeft) ? 1 : 0;
                }
                i++;
            }
        }

        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: Merry christmas!");
    }

    static bool TryPlaceEverything(List<List<bool[,]>> presents, bool[,] region, int[] presentsLeft)
    {
        List<(int x, int y)> openSpots = [(0, 0)];
        while (openSpots.Count > 0 && presentsLeft.Any(x => x > 0))
        {
            openSpots.Sort((a, b) => (a.x + a.y).CompareTo(b.x + b.y));
            (int x, int y) spot = openSpots[0];
            openSpots.RemoveAt(0);
            bool foundPlacement = false;
            for (int i = 0; i < presents.Count && !foundPlacement; i++)
            {
                if (presentsLeft[i] == 0) continue;
                for (int j = 0; j < presents[i].Count && !foundPlacement; j++)
                {
                    (bool[,] regionNext, bool success) = TryPlace(presents[i][j], region, spot.x, spot.y);
                    if (success)
                    {
                        region = regionNext;
                        presentsLeft[i]--;
                        foundPlacement = true;
                        openSpots.AddRange(GetGaps(presents[i][j], spot.x, spot.y));
                        break;
                    }
                }
            }
            if (!foundPlacement)
            {
                for (int y = 0; y < region.GetLength(0) && !foundPlacement; y++)
                {
                    for (int x = 0; x < region.GetLength(1) && !foundPlacement; x++)
                    {
                        for (int i = 0; i < presents.Count && !foundPlacement; i++)
                        {
                            if (presentsLeft[i] == 0) continue;
                            for (int j = 0; j < presents[i].Count && !foundPlacement; j++)
                            {
                                (bool[,] regionNext, bool success) = TryPlace(presents[i][j], region, spot.x, spot.y);
                                if (success)
                                {
                                    region = regionNext;
                                    presentsLeft[i]--;
                                    foundPlacement = true;
                                    openSpots.AddRange(GetGaps(presents[i][j], spot.x, spot.y));
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }
        return presentsLeft.All(x => x == 0);
    }

    static List<(int x, int y)> GetGaps(bool[,] present, int posX, int posY)
    {
        List<(int x, int y)> ret = [];
        for (int y = 0; y < 3; y++)
        {
            for (int x = 0; x < 3; x++)
            {
                if (!present[y, x])
                {
                    ret.Add((x + posX, y + posY));
                }
            }
        }
        return ret;
    }

    static (bool[,] region, bool success) TryPlace(bool[,] present, bool[,] region, int posX, int posY)
    {
        if (posX > region.GetLength(1) - 3 || posY > region.GetLength(0) - 3) return (region, false);
        bool[,] ret = (bool[,])region.Clone();
        for (int y = 0; y < 3; y++)
        {
            for (int x = 0; x < 3; x++)
            {
                if (present[y, x] && ret[posY + y, posX + x])
                {
                    return (ret, false);
                }
                ret[posY + y, posX + x] = present[y, x];
            }
        }
        return (ret, true);
    }

    static bool[,] RotateCW(bool[,] present)
    {
        return new bool[,]
        {
            {present[0, 2], present[0, 1], present[0, 0]},
            {present[1, 2], present[1, 1], present[1, 0]},
            {present[2, 2], present[2, 1], present[2, 0]}
        };
    }

    static bool[,] FlipH(bool[,] present)
    {
        return new bool[,]
        {
            {present[2, 0], present[1, 0], present[0, 0]},
            {present[2, 1], present[1, 1], present[0, 1]},
            {present[2, 2], present[1, 2], present[0, 2]}
        };
    }


}
