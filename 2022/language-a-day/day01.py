with open("./2022/inputs/day1.txt", "r") as f:
    inp = [list(map(int, g.splitlines())) for g in f.read().split("\n\n")]

part_1 = max(sum(g) for g in inp)
part_2 = sum(sorted(sum(g) for g in inp)[-3:])

print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
