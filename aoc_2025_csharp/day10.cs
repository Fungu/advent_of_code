using System.Diagnostics;
using System.Security.Cryptography.X509Certificates;

namespace aoc_2025_csharp;

public static class Day10
{
    public static void Solve() 
    {
        string[] lines = File.ReadAllLines("C:/Dropbox/advent_of_code/2025/day10.txt");
        var stopwatch = Stopwatch.StartNew();

        int part1 = 0;
        long part2 = 0;
        foreach (string line in lines)
        {
            string[] tempSplit = line.Split("] ");
            bool[] indicatorLightDiagram  = tempSplit[0][1..].ToCharArray().Select(c => c == '#').ToArray();
            tempSplit = tempSplit[1].Split(" {");
            List<int[]> buttons = tempSplit[0].Split(" ").Select(s => s[1..(s.Length - 1)].Split(",").Select(t => int.Parse(t)).ToArray()).ToList();
            double[] joltageRequirements = tempSplit[1][..(tempSplit[1].Length - 1)].Split(",").Select(t => double.Parse(t)).ToArray();

            buttons.Sort((a, b) => a.Length.CompareTo(b.Length));
            double[,] equations = new double[joltageRequirements.Length, buttons.Count];
            for (int i = 0; i < buttons.Count; i++)
            {
                for (int j = 0; j < buttons[i].Length; j++)
                {
                    equations[buttons[i][j], i] = 1;
                }
            }
            var result = GaussianElimination(equations, joltageRequirements);
            part2 += result;
        }
        
        
        stopwatch.Stop();
        Console.WriteLine($"Execution time: {stopwatch.ElapsedMilliseconds} ms");
        Console.WriteLine($"Part 1: {part1}");
        Console.WriteLine($"Part 2: {part2}");
    }

    static int GaussianElimination(double[,] equations, double[] right)
    {
        List<int> freeVariables = [];
        for (int i = 0; i < Math.Min(equations.GetLength(0), equations.GetLength(1)); i++)
        {
            if (equations[i, i] == 0)
            {
                int swapIndex = FindNonZeroRow(equations, i);
                if (swapIndex != -1)
                {
                    SwapRows(equations, right, i, swapIndex);
                }
                else
                {
                    swapIndex = FindNonZeroColumn(equations, i);
                    if (swapIndex != -1)
                    {
                        SwapColumns(equations, i, swapIndex);
                    }
                    else
                    {
                        freeVariables.Add(i);
                        continue;
                    }
                }
            }
            double ii = equations[i, i];
            right[i] /= ii;
            for (int j = 0; j < equations.GetLength(1); j++)
            {
                equations[i, j] /= ii;
            }
            for (int j = i + 1; j < equations.GetLength(0); j++)
            {
                double ji = equations[j, i];
                for (int k = i; k < equations.GetLength(1); k++)
                {
                    equations[j, k] -= equations[i, k] * ji;
                }
                right[j] -= right[i] * ji;
            }
        }
        for (int i = Math.Min(equations.GetLength(0), equations.GetLength(1)) - 1; i >= 0; i--)
        {
            for (int j = i - 1; j >= 0; j--)
            {
                double ji = equations[j, i];
                for (int k = i; k < equations.GetLength(1); k++)
                {
                    equations[j, k] -= equations[i, k] * ji;
                }
                right[j] -= right[i] * ji;
            }
        }
        for (int i = equations.GetLength(0); i < equations.GetLength(1); i++)
        {
            freeVariables.Add(i);
        }
        List<int> freeVariableValues = new(freeVariables.Count);
        for (int i = 0; i < freeVariables.Count; i++)
        {
            freeVariableValues.Add(0);
        }
        var ret = FreeVariableValueSearch(equations, right, freeVariables) ?? -1;
        return ret;
    }

    static int FindNonZeroRow(double[,] equations, int index)
    {
        for (int i = index + 1; i < equations.GetLength(0); i++)
        {
            if (equations[i, index] != 0)
            {
                return i;
            }
        }
        return -1;
    }

    static int FindNonZeroColumn(double[,] equations, int index)
    {
        for (int i = index + 1; i < equations.GetLength(1); i++)
        {
            if (equations[index, i] != 0)
            {
                return i;
            }
        }
        return -1;
    }

    static void SwapRows(double[,] equations, double[] right, int indexA, int indexB)
    {
        for (int i = 0; i < equations.GetLength(1); i++)
        {
            (equations[indexB, i], equations[indexA, i]) = (equations[indexA, i], equations[indexB, i]);
        }
        (right[indexB], right[indexA]) = (right[indexA], right[indexB]);
    }

    static void SwapColumns(double[,] equations, int indexA, int indexB)
    {
        for (int i = 0; i < equations.GetLength(0); i++)
        {
            (equations[i, indexB], equations[i, indexA]) = (equations[i, indexA], equations[i, indexB]);
        }
    }

    static bool IsAllIntegers(double[,] equations, double[] right, int scale, int row)
    {
        for (int i = 0; i < equations.GetLength(1); i++)
        {
            if (!IsInteger(equations[row, i] * scale))
            {
                return false;
            }
        }
        return IsInteger(right[row] * scale);
    }

    static void ScaleEquation(double[,] equations, double[] right, int scale, int row)
    {
        for (int i = 0; i < equations.GetLength(1); i++)
        {
            equations[row, i] = Math.Round(equations[row, i] * scale);
        }
        right[row] = Math.Round(right[row]* scale);
    }

    static int? FreeVariableValueSearch(double[,] equations, double[] right, List<int> freeVariables)
    {
        int[] distribution = new int[freeVariables.Count];
        int? lowestCountFound = GetTotal(equations, right, freeVariables, distribution);
        int max = (int)right.Max();
        while (true)
        {
            int? newTotal = GetTotal(equations, right, freeVariables, distribution);
            if (lowestCountFound is null || newTotal < lowestCountFound)
            {
                lowestCountFound = newTotal;
            }
            bool distributionDone = IncreaseDistribution(distribution, max);
            if (distributionDone) 
            {
                return lowestCountFound;
            }
        }
    }

    static bool IncreaseDistribution(int[] distribution, int max)
    {
        if (distribution.Length == 0)
        {
            return true;
        }
        distribution[0]++;
        for (int i = 0; ; i++)
        {
            if (distribution[i] > max)
            {
                distribution[i] = 0;
                if (i + 1 < distribution.Length)
                {
                    distribution[i + 1]++;
                }
                else
                {
                    return true;
                }
            }
            else
            {
                return false;
            }
        }
    }

    static int? GetTotal(double[,] equations, double[] right, List<int> freeVariables, int[] freeVariableValues)
    {
        int rightSum = 0;
        for (int i = 0; i < equations.GetLength(0); i++)
        {
            double freeVariableResult = 0;
            for (int a = 0; a < freeVariables.Count; a++)
            {
                freeVariableResult += equations[i, freeVariables[a]] * freeVariableValues[a];
            }
            double rightAfterFree = right[i] - freeVariableResult;
            if (rightAfterFree < -0.0000001 || !IsInteger(rightAfterFree)) 
                return null;
            rightSum += (int)Math.Round(rightAfterFree);
        }
        return rightSum + freeVariableValues.Sum();
    }

    static bool IsInteger(double a)
    {
        double diff = Math.Abs(Math.Truncate(a) - a);
        return (diff < 0.0000001) || (diff > 0.9999999);
    }



}
