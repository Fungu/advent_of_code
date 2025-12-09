using System.Diagnostics;

namespace aoc_2025_csharp;

public static class Day09
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day09.txt");
        var stopwatch = Stopwatch.StartNew();

        List<(long x, long y)> tiles = [];
        foreach (var line in lines)
        {
            tiles.Add((long.Parse(line.Split(',')[0]), long.Parse(line.Split(',')[1])));
        }

        long part1 = 0;
        for (int i = 0; i < tiles.Count; i++)
        {
            for (int j = i + 1; j < tiles.Count; j++)
            {
                var w = Math.Abs(tiles[i].x - tiles[j].x) + 1;
                var h = Math.Abs(tiles[i].y - tiles[j].y) + 1;
                part1 = Math.Max(part1, w * h);
            }
        }
        
        int turns = 0;
        for (int i = 0; i < tiles.Count; i++)
        {
            turns += IsRightTurn(tiles, i) ? 1 : -1;
        }
        bool IsRightSideInside = turns == 4;

        long part2 = 0;
        for (int i = 0; i < tiles.Count; i++)
        {
            for (int j = i + 1; j < tiles.Count; j++)
            {
                // Check if any red tiles are inside the rectangle
                bool foundTileInside = tiles.Any(t => IsTileInside(tiles[i], tiles[j], t));
                if (foundTileInside) continue;

                // Check if any lines intersects with the rectangle
                bool foundLineInside = false;
                long middleX = (tiles[i].x + tiles[j].x) / 2;
                long middleY = (tiles[i].y + tiles[j].y) / 2;
                for (int ii = 0; ii < tiles.Count; ii++)
                {
                    int jj = ii == tiles.Count - 1 ? 0 : ii + 1;
                    if (CheckIntersects(((tiles[ii].x, tiles[ii].y), (tiles[jj].x, tiles[jj].y)), ((middleX, tiles[i].y), (middleX, tiles[j].y))) || 
                        CheckIntersects(((tiles[ii].x, tiles[ii].y), (tiles[jj].x, tiles[jj].y)), ((tiles[i].x, middleY), (tiles[j].x, middleY))))
                    {
                        foundLineInside = true;
                        break;
                    }
                }
                if (foundLineInside) continue;

                // Check if the rectangle is inside the loop. (This check was not needed for my input)
                (long, long) tileTowardsJ = (
                    tiles[i].x + Math.Clamp(tiles[j].x - tiles[i].x, -1, 1),
                    tiles[i].y + Math.Clamp(tiles[j].y - tiles[i].y, -1, 1)
                );
                int a = i == 0 ? tiles.Count - 1 : i - 1;
                int b = i == tiles.Count - 1 ? 0 : i + 1;
                (long, long) tileInsideCorner = (
                    tiles[i].x + Math.Clamp(tiles[a].x - tiles[i].x, -1, 1) + Math.Clamp(tiles[b].x - tiles[i].x, -1, 1),
                    tiles[i].y + Math.Clamp(tiles[a].y - tiles[i].y, -1, 1) + Math.Clamp(tiles[b].y - tiles[i].y, -1, 1)
                );
                bool isRight = IsRightTurn(tiles, i);
                bool isRectangleInside = tileTowardsJ == tileInsideCorner == IsRightSideInside == isRight;

                if (!foundTileInside && !foundLineInside && isRectangleInside)
                {
                    var w = Math.Abs(tiles[i].x - tiles[j].x) + 1;
                    var h = Math.Abs(tiles[i].y - tiles[j].y) + 1;
                    part2 = Math.Max(part2, w * h);
                }
            }
        }
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static bool CheckIntersects(((long x, long y) p1, (long x, long y) p2) line1, ((long x, long y) p1, (long x, long y) p2) line2)
    {
        if ((line1.p1.x == line1.p2.x && line2.p1.x == line2.p2.x) || (line1.p1.y == line1.p2.y && line2.p1.y == line2.p2.y))
        {
            return false;
        }
        if (line1.p1.y == line1.p2.y)
        {
            return line2.p1.x > Math.Min(line1.p1.x, line1.p2.x) && line2.p1.x < Math.Max(line1.p1.x, line1.p2.x) && 
                Math.Min(line2.p1.y, line2.p2.y) < line1.p1.y && Math.Max(line2.p1.y, line2.p2.y) > line1.p1.y;
        }
        else
        {
            return line2.p1.y > Math.Min(line1.p1.y, line1.p2.y) && line2.p1.y < Math.Max(line1.p1.y, line1.p2.y) && 
                Math.Min(line2.p1.x, line2.p2.x) < line1.p1.x && Math.Max(line2.p1.x, line2.p2.x) > line1.p1.x;
        }
    }

    static bool IsRightTurn(List<(long x, long y)> tiles, int i)
    {
        int a = i == 0 ? tiles.Count - 1 : i - 1;
        int b = i == tiles.Count - 1 ? 0 : i + 1;
        long dxa = Math.Clamp(tiles[i].x - tiles[a].x, -1, 1);
        long dya = Math.Clamp(tiles[i].y - tiles[a].y, -1, 1);
        long dxb = Math.Clamp(tiles[b].x - tiles[i].x, -1, 1);
        long dyb = Math.Clamp(tiles[b].y - tiles[i].y, -1, 1);
        return dxa == dyb && dya == -dxb;
    }

    static bool IsTileInside((long x, long y) p1, (long x, long y) p2, (long x, long y) tile)
    {
        return tile.x > Math.Min(p1.x, p2.x) && 
                tile.x < Math.Max(p1.x, p2.x) &&
                tile.y > Math.Min(p1.y, p2.y) && 
                tile.y < Math.Max(p1.y, p2.y);
    }

    static long GetDir(long a, long b)
    {
        if (a == b) return 0;
        long d = b - a;
        return d / Math.Abs(d);
    }
}
