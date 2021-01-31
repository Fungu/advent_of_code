#include <iostream>
#include <fstream>
#include <algorithm>

int main()
{
    std::ifstream ifs("input/day01.txt");
    std::string content((std::istreambuf_iterator<char>(ifs)),
                        (std::istreambuf_iterator<char>()));

    int part2 = -1;
    int floor = 0;
    for (size_t i=0; i<content.length(); i++) {
        if (content.at(i) == '(') {
            floor++;
        } else if (content.at(i) == ')') {
            floor--;
        }
        if (floor == -1 && part2 == -1) {
            part2 = i + 1;
        }
    }

    printf("Part 1: %d\n", floor);
    printf("Part 2: %d", part2);
}