#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define LINE_LENGTH 3

char beats(char move) {
    if (move == 'A') {
        return 'C';
    } else if (move == 'B') {
        return 'A';
    } else if (move == 'C') {
        return 'B';
    } else {
        return ' ';
    }
}

char inverseBeats(char move) {
    if (move == 'A') {
        return 'B';
    } else if (move == 'B') {
        return 'C';
    } else if (move == 'C') {
        return 'A';
    } else {
        return ' ';
    }
}

int score1(char mine, char theirs) {
    int score = mine == theirs ? 3 : (beats(mine) == theirs ? 6 : 0);
    score += mine == 'A' ? 1 : (mine == 'B' ? 2 : 3);
    return score;
}

int score2(char mine, char theirs) {
    if (mine == 'A') {
        mine = beats(theirs);
    } else if (mine == 'B') {
        mine = theirs;
    } else if (mine == 'C') {
        mine = inverseBeats(theirs);
    }

    int score = mine == theirs ? 3 : (beats(mine) == theirs ? 6 : 0);
    score += mine == 'A' ? 1 : (mine == 'B' ? 2 : 3);
    return score;
}

int main(void) {
    FILE *fp;
    int bufferLength = LINE_LENGTH + 2;
    char buffer[bufferLength];
    fopen_s(&fp, "./2022/inputs/day2.txt", "r");

    int part_1 = 0;
    int part_2 = 0;
    while (fgets(buffer, bufferLength, fp) != NULL) {
        char theirs = buffer[0];
        char mine = buffer[2];
        mine = mine - 'X' + 'A';

        part_1 += score1(mine, theirs);
        part_2 += score2(mine, theirs);
    }

    printf("Part 1: %d\n", part_1);
    printf("Part 2: %d\n", part_2);
}
