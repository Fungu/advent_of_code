using System.Diagnostics;

namespace aoc_2023_csharp;

public static class Day23
{
    private readonly static Dictionary<char, (int dx, int dy)> SLOPES = new Dictionary<char, (int dx, int dy)>() {
        { '>', (1, 0) },
        { 'v', (0, 1) },
        { '<', (-1, 0) },
        { '^', (0, -1) },
        { '#', (0, 0) }
    };
    private readonly static (int ndx, int ndy)[] directions = [(-1, 0), (1, 0), (0, -1), (0, 1)];

    public static void Solve() 
    {
        string[] input = File.ReadAllLines("input/day23.txt");
        var stopwatch = Stopwatch.StartNew();

        Dictionary<(int x, int y), List<(int x, int y, int length)>> nodes = [];
        nodes.Add((1, 0), []);
        FindConnection(input, nodes, 1, 0, 0, 1);

        long part1 = FindLongestRoute(nodes, (1, 0), [], false);
        long part2 = FindLongestRoute(nodes, (1, 0), [], true);

        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    private static void FindConnection(string[] input, Dictionary<(int x, int y), List<(int x, int y, int length)>> nodes, int startX, int startY, int dx, int dy)
    {
        int x = startX + dx;
        int y = startY + dy;
        int length = 1;
        while (true)
        {
            length++;
            foreach ((int ndx, int ndy) in directions)
            {
                if (ndx == -dx && ndy == -dy) continue;
                int nx = x + ndx;
                int ny = y + ndy;
                if (ny == input.Length - 1)
                {
                    nodes[(startX, startY)].Add((0, 0, length));
                    nodes[(0, 0)] = [];
                    return;
                }
                char c = input[ny][nx];
                if (c == '#' || (c != '.' && SLOPES[c].dx == -dx && SLOPES[c].dy == -dy))
                    continue;
                if (c != '.')
                {
                    // Found the next node
                    nx += ndx;
                    ny += ndy;
                    nodes[(startX, startY)].Add((nx, ny, length + 1));
                    if (!nodes.ContainsKey((nx, ny)))
                    {
                        nodes.Add((nx, ny), []);
                    }
                    else
                    {
                        return;
                    }

                    foreach ((int nndx, int nndy) in directions)
                    {
                        if (nndx == -ndx && nndy == -ndy) continue;
                        int nnx = nx + nndx;
                        int nny = ny + nndy;
                        char nc = input[nny][nnx];
                        if (SLOPES[nc].dx == nndx && SLOPES[nc].dy == nndy)
                        {
                            FindConnection(input, nodes, nx, ny, nndx, nndy);
                        }
                    }
                    return;
                }
                dx = ndx;
                dy = ndy;
                x = nx;
                y = ny;
                break;
            }
        }
    }

    private static int FindLongestRoute(Dictionary<(int x, int y), List<(int x, int y, int length)>> nodes, (int x, int y) node, List<(int x, int y)> visited, bool allowUphill)
    {
        if (node == (0, 0)) return 0;
        var vistedNext = new List<(int x, int y)>(visited);
        vistedNext.Add(node);
        Dictionary<(int x, int y), int> neighbors = [];
        foreach (var n in nodes[node])
        {
            var neighbor = (n.x, n.y);
            if (!visited.Contains(neighbor))
                neighbors.Add(neighbor, n.length);
        }
        if (allowUphill)
        {
            foreach (var neighbor in nodes.Keys)
            {
                if (visited.Contains(neighbor))
                    continue;
                foreach (var connection in nodes[neighbor])
                    if (connection.x == node.x && connection.y == node.y)
                        neighbors.Add(neighbor, connection.length);
            }
        }
        int longest = -999999;
        foreach (var neighbor in neighbors)
        {
            var length = neighbor.Value;
            longest = Math.Max(longest, length + FindLongestRoute(nodes, neighbor.Key, vistedNext, allowUphill));
        }
        return longest;
    }
}
