using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day21
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day21.txt");
        var stopwatch = Stopwatch.StartNew();

        int width = input[0].Length;
        int middle = width / 2;
        int maxPos = width - 1;
        
        int part1 = FloodFill(input, middle, middle, 64);

        int totalSteps = 26501365;
        int nrOfTilesRadius = (totalSteps - middle) / width;
        int stepsLeftEdges = width;
        int stepsLeftBig = width + width / 2;
        int stepsLeftSmall = width / 2 - 1;

        bool evenBig = false;
        int n = FloodFill(input, middle, maxPos, stepsLeftEdges, !evenBig);
        int e = FloodFill(input, 0, middle, stepsLeftEdges, !evenBig);
        int s = FloodFill(input, middle, 0, stepsLeftEdges, !evenBig);
        int w = FloodFill(input, maxPos, middle, stepsLeftEdges, !evenBig);
        int cEven = FloodFill(input, middle, middle, 99999, true);
        int cOdd = FloodFill(input, middle, middle, 99999, false);
        int nwBig = FloodFill(input, maxPos, maxPos, stepsLeftBig, evenBig);
        int nwSmall = FloodFill(input, maxPos, maxPos, stepsLeftSmall, !evenBig);
        int neBig = FloodFill(input, 0, maxPos, stepsLeftBig, evenBig);
        int neSmall = FloodFill(input, 0, maxPos, stepsLeftSmall, !evenBig);
        int swBig = FloodFill(input, maxPos, 0, stepsLeftBig, evenBig);
        int swSmall = FloodFill(input, maxPos, 0, stepsLeftSmall, !evenBig);
        int seBig = FloodFill(input, 0, 0, stepsLeftBig, evenBig);
        int seSmall = FloodFill(input, 0, 0, stepsLeftSmall, !evenBig);

        long nrOfEvenCenter = 0;
        long nrOfOddCenter = 0;
        bool c = true;
        for (int i = nrOfTilesRadius - 1; i >= 0; i--)
        {
            if (c)
                nrOfEvenCenter += i;
            else
                nrOfOddCenter += i;
            c = !c;
        }
        nrOfEvenCenter *= 4;
        nrOfOddCenter *= 4;
        nrOfOddCenter += 1;
        long nrOfEdgesBig = nrOfTilesRadius - 1;
        long nrOfEdgesSmall = nrOfTilesRadius;
        long part2 = n + e + s + w + nrOfEvenCenter * cEven + nrOfOddCenter * cOdd + nrOfEdgesBig * (nwBig + neBig + swBig + seBig) + nrOfEdgesSmall * (nwSmall + neSmall + swSmall + seSmall);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    public static int FloodFill(string[] input, int startX, int startY, int maxSteps, bool countCell = true)
    {
        var openSet = new Queue<(int x, int y)>();
        openSet.Enqueue((startX, startY));
        var nextOpenSet = new Queue<(int x, int y)>();
        var closedSet = new Queue<(int x, int y)>();

        int width = input[0].Length;
        int height = input.Length;
        int ret = 0;
        int step = 0;
        (int dx, int dy)[] directions = [(-1, 0), (1, 0), (0, -1), (0, 1)];
        while (true)
        {
            if (openSet.Count == 0)
            {
                if (nextOpenSet.Count == 0)
                {
                    break;
                }
                openSet = nextOpenSet;
                nextOpenSet = new Queue<(int x, int y)>();
                countCell = !countCell;
                step++;
                if (step > maxSteps)
                {
                    break;
                }
            }
            if (countCell)
            {
                ret++;
            }
            (int x, int y) = openSet.Dequeue();
            closedSet.Enqueue((x, y));
            foreach ((int dx, int dy) in directions)
            {
                (int nx, int ny) = (x + dx, y + dy);
                if (nx >= 0 && ny >= 0 && nx < width && ny < height && input[ny][nx] != '#' && !closedSet.Contains((nx, ny)) && !nextOpenSet.Contains((nx, ny)))
                {
                    nextOpenSet.Enqueue((nx, ny));
                }
            }
        }
        return ret;
    }
}
