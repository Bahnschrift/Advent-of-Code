from os import chdir, path
from shutil import copy
from sys import argv

day = int(argv[1])
if len(argv) > 2:
    year = int(argv[2])
else:
    year = 2022

chdir(path.dirname(__file__))

with open("template.ipynb", "r") as src:
    with open(f"{year}/python/day{day:02d}.ipynb", "w+") as dst:
        for line in src:
            dst.write(line.replace(" 1", f" {day}").replace("/1", f"/{day}").replace("2022", f"{year}"))
