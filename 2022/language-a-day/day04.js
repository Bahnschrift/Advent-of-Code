let fs = require("fs"),
    inp = fs.readFileSync("./2022/inputs/day4.txt", "utf-8").split("\n");

let part1 = 0,
    part2 = 0;

for (const line of inp) {
    if (line === "") continue;

    const matches = line.match(/\d+/g);
    const s1 = parseInt(matches[0]);
    const e1 = parseInt(matches[1]);
    const s2 = parseInt(matches[2]);
    const e2 = parseInt(matches[3]);

    if ((s1 <= s2 && e1 >= e2) || (s2 <= s1 && e2 >= e1)) {
        part1++;
    }

    if ((s1 <= s2 && e1 >= s2) || (s2 <= s1 && e2 >= s1)) {
        part2++;
    }
}

console.log("Part 1:", part1);
console.log("Part 2:", part2);
