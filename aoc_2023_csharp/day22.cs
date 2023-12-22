using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day22
{
    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day22.txt");
        var stopwatch = Stopwatch.StartNew();

        var bricks = new List<int[][]>();
        // [[x1, y1, z1], [x2, y2, z2]]
        foreach (var line in input)
        {
            var p1 = line.Split('~')[0].Split(',').Select(int.Parse).ToArray();
            var p2 = line.Split('~')[1].Split(',').Select(int.Parse).ToArray();
            var brickLength = Math.Abs(p1[0] - p2[0]) + Math.Abs(p1[1] - p2[1]) + Math.Abs(p1[2] - p2[2]) + 1;
            var delta = new int[3];
            for (int i = 0; i < 3; i++)
                delta[i] = -(p1[i] - p2[i]) / (p1[i] == p2[i] ? 1 : Math.Abs(p1[i] - p2[i]));
            int[][] points = new int[brickLength][];
            for (int i = 0; i < brickLength; i++)
                points[i] = [p1[0] + i * delta[0], p1[1] + i * delta[1], p1[2] + i * delta[2]];
            bricks.Add(points);
        }

        List<int>[] restsOn = new List<int>[bricks.Count];
        for (int i = 0; i < bricks.Count; i++)
            restsOn[i] = [];
        bool[] settled = Enumerable.Repeat(false, bricks.Count).ToArray();
        while (settled.Any(a => !a))
        {
            for (int i = 0; i < bricks.Count; i++)
            {
                if (settled[i]) continue;
                for (int j = 0; j < bricks[i].Length; j++)
                    if (bricks[i][j][2] == 1)
                    {
                        settled[i] = true;
                        break;
                    }
                if (settled[i]) continue;
                MoveBrick(bricks[i], -1);
                bool collided = false;
                for (int j = 0; j < bricks.Count; j++)
                {
                    if (i == j) continue;
                    if (CheckCollision(bricks[i], bricks[j]))
                    {
                        collided = true;
                        if (settled[j])
                        {
                            settled[i] = true;
                            restsOn[i].Add(j);
                        }
                    }
                }
                if (collided) MoveBrick(bricks[i], 1);
            }
        }
        
        long part1 = 0;
        long part2 = 0;
        for (int i = 0; i < bricks.Count; i++)
        {
            if (!restsOn.Any(a => a.Count == 1 && a[0] == i))
            {
                part1++;
            }
            for (int j = 0; j < bricks.Count; j++)
            {
                if (i == j) continue;
                Queue<int> targets = new();
                targets.Enqueue(j);
                bool foundOtherBase = false;
                bool foundTarget = false;
                while (targets.Count > 0)
                {
                    int current = targets.Dequeue();
                    if (current == i)
                    {
                        foundTarget = true;
                        continue;
                    }
                    if (restsOn[current].Count == 0)
                    {
                        foundOtherBase = true;
                        break;
                    }
                    foreach (int a in restsOn[current])
                        targets.Enqueue(a);
                }
                if (foundTarget && !foundOtherBase)
                {
                    part2++;
                }
            }
        }

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static bool CheckCollision(int[][] brick1, int[][] brick2)
    {
        for (int i = 0; i < brick1.Length; i++)
            for (int j = 0; j < brick2.Length; j++)
                if (CheckPointCollision(brick1[i], brick2[j]))
                    return true;
        return false;
    }

    private static bool CheckPointCollision(int[] p1, int[] p2)
    {
        for (int a = 0; a < 3; a++)
            if (p1[a] != p2[a])
                return false;
        return true;
    }

    private static void MoveBrick(int[][] brick, int dz)
    {
        for (int i = 0; i < brick.Length; i++)
            brick[i][2] += dz;
    }

    private static void PrintBrick(int[][] brick)
    {
        for (int j = 0; j < brick.Length; j++)
        {
            Console.WriteLine(string.Join(", ", brick[j]));
        }
    }
}
