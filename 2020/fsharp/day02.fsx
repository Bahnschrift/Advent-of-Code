open System
open System.IO

let count c s = Linq.Enumerable.Count(s, fun c' -> c' = c)

let data =
    (__SOURCE_DIRECTORY__
     |> Directory.GetParent
     |> fun x -> x.FullName, "inputs/day02.txt")
    |> Path.Combine
    |> File.ReadAllLines

let mutable part1 = 0
let mutable part2 = 0

for line in data do
    let parts = line.Split(" ")
    let ends = Array.map int (parts.[0].Split("-"))
    let range = [ends.[0] .. ends.[1]]
    let checkChar = char (parts.[1].[0])
    let checkStr = parts.[2]

    if List.exists((=) (count checkChar checkStr)) range then
        part1 <- part1 + 1
    
    let mutable valid = 0
    for index in ends do
        if checkStr.[index - 1] <> checkChar then
            valid <- valid + 1
    if valid = 1 then part2 <- part2 + 1

printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
