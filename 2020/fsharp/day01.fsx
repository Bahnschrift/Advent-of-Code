open System
open System.IO

let data =
    (__SOURCE_DIRECTORY__
     |> Directory.GetParent
     |> fun x -> x.FullName, "inputs/day01.txt")
    |> Path.Combine
    |> File.ReadAllLines
    |> Seq.map int

let mutable part1 = 0
let mutable part2 = 0

for x in data do
    for y in data do
        if x + y = 2020 then part1 <- x * y

        for z in data do
            if x + y + z = 2020 then
                part2 <- x * y * z


printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
