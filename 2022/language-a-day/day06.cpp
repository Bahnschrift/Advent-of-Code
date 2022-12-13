#include <fstream>
#include <string>
#include <iostream>
#include <set>

int firstIndex(std::string inp, int n) {
    for (int i = n; i < inp.length(); i++) {
        std::string substr = inp.substr(i - n, n);
        if (std::set<char>(substr.begin(), substr.end()).size() == n) {
            return i;
        }
    }

    return -1;
}

int main(void) {
    std::ifstream inpStream("./2022/inputs/day6.txt");
    std::string inp;
    std::getline(inpStream, inp);
    inpStream.close();

    std::cout << "Part 1: " << firstIndex(inp, 4) << std::endl;
    std::cout << "Part 2: " << firstIndex(inp, 14) << std::endl;

    return 0;
}
