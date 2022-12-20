open System
open System.IO

let data =
    (__SOURCE_DIRECTORY__
     |> Directory.GetParent
     |> fun x -> x.FullName, "inputs/day05.txt")
    |> Path.Combine
    |> File.ReadAllLines

let mutable part1 = 0
let mutable part2 = 0
let mutable passes = Set.empty

for pass in data do
    let pass =
        Convert.ToInt32(
            pass
                .Replace("F", "0")
                .Replace("B", "1")
                .Replace("L", "0")
                .Replace("R", "1"),
            2
        )

    passes <- passes.Add pass

part1 <- passes.MaximumElement

for x in [ passes.MinimumElement .. passes.MaximumElement ] do
    if not (passes.Contains x) then
        part2 <- x

printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
