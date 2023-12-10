using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day10
{
    static readonly Dictionary<char, (int x, int y)[]> pipes = new ()
    {
        { '|', [(0, -1), (0, 1)] },
        { '-', [(-1, 0), (1, 0)] },
        { 'L', [(0, -1), (1, 0)] },
        { 'J', [(0, -1), (-1, 0)] },
        { '7', [(0, 1), (-1, 0)] },
        { 'F', [(0, 1), (1, 0)] },
        { '.', [] }
    };
    static readonly (int x, int y)[] directions = [(-1, 0), (1, 0), (0, -1), (0, 1)];
    static readonly (int x, int y)[] cornerDirections = [(-1, -1), (0, -1), (0, 0), (-1, 0)];

    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day10.txt");
        var stopwatch = Stopwatch.StartNew();

        char[][] grid = new char[input.Length][];
        int[][] loopCounter = new int[input.Length][];
        bool[][] outside = new bool[input.Length][];

        for (int i = 0; i < input.Length; i++)
        {
            grid[i] = input[i].ToCharArray();
            loopCounter[i] = Enumerable.Repeat(0, input[i].Length).ToArray();
            outside[i] = Enumerable.Repeat(false, input[i].Length).ToArray();
        }
        int gridWidth = grid[0].Length;
        int gridHeight = grid.Length;
        int startX = 0;
        int startY = 0;
        for (int y = 0; y < grid.Length; y++)
            for (int x = 0; x < grid[y].Length; x++)
                if (grid[y][x] == 'S')
                {
                    startX = x;
                    startY = y;
                }

        (int x, int y) position = (0, 0);
        (int x, int y) prevPosition = (startX, startY);
        foreach ((int dx, int dy) in directions)
        {
            int nx = startX + dx; 
            int ny = startY + dy;
            if (IsValidPos(nx, ny, gridWidth, gridHeight) && pipes[grid[ny][nx]].Any(dir => dir.x == -dx && dir.y == -dy))
            {
                position = (nx, ny);
                loopCounter[ny][nx] = 1;
                break;
            }
        }

        int part1 = 1;
        while (position != (startX, startY))
        {
            part1++;
            (int x, int y) = position;
            (int prevX, int prevY) = prevPosition;
            foreach ((int dx, int dy) in pipes[grid[y][x]])
            {
                if (x + dx != prevX || y + dy != prevY)
                {
                    prevPosition = position;
                    position = (x + dx, y + dy);
                    loopCounter[y + dy][x + dx] = part1;
                    break;
                }
            }
        }

        Queue<(int, int)> openSet = new();
        for (int x = 0; x <= loopCounter[0].Length; x++)
        {
            openSet.Enqueue((x, 0));
            openSet.Enqueue((x, loopCounter.Length));
        }
        for (int y = 0; y <= loopCounter.Length; y++)
        {
            openSet.Enqueue((0, y));
            openSet.Enqueue((loopCounter[0].Length, y));
        }
        HashSet<(int, int)> closedSet = [];
        while (openSet.Count > 0)
        {
            (int x, int y) = openSet.Dequeue();
            closedSet.Add((x, y));
            foreach ((int dx, int dy) in cornerDirections)
            {
                (int nx, int ny) = (x + dx, y + dy);
                if (IsValidPos(nx, ny, gridWidth, gridHeight) && loopCounter[ny][nx] == 0)
                    outside[ny][nx] = true;
            }
            List<int> adjacentStart = GetAdjacentFromCorner(x, y, loopCounter);
            foreach ((int dx, int dy) in directions)
            {
                (int nx, int ny) = (x + dx, y + dy);
                if (!IsValidCorner(nx, ny, gridWidth, gridHeight)) 
                    continue;
                if (closedSet.Contains((nx, ny)) || openSet.Contains((nx, ny)))
                    continue;
                List<int> intersection = adjacentStart.Intersect(GetAdjacentFromCorner(nx, ny, loopCounter)).ToList();
                if (intersection.Count != 2 || (Math.Abs(intersection[0] - intersection[1]) != part1 - 1 && Math.Abs(intersection[0] - intersection[1]) != 1))
                    openSet.Enqueue((nx, ny));
            }
        }
        int part2 = grid.Length * grid[0].Length - outside.Sum(a => a.Count(b => b)) - part1;
        part1 /= 2;

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static bool IsValidPos(int x, int y, int gridWidth, int gridHeight)
    {
        return x >= 0 && y >= 0 && x < gridWidth && y < gridHeight;
    }

    private static bool IsValidCorner(int x, int y, int gridWidth, int gridHeight)
    {
        return x >= 0 && y >= 0 && x <= gridWidth && y <= gridHeight;
    }

    private static List<int> GetAdjacentFromCorner(int x, int y, int[][] loopCounter)
    {
        List<int> result = [];
        foreach ((int dx, int dy) in cornerDirections)
        {
            (int nx, int ny) = (x + dx, y + dy);
            if (IsValidPos(nx, ny, loopCounter[0].Length, loopCounter.Length) && loopCounter[ny][nx] > 0)
            {
                result.Add(loopCounter[ny][nx]);
            }
        }
        return result;
    }
}
