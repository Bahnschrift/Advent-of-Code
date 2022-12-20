open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked

let data =
    (__SOURCE_DIRECTORY__
     |> Directory.GetParent
     |> fun x -> x.FullName, "inputs/day06.txt")
    |> Path.Combine
    |> File.ReadAllText
    |> fun x -> x.Split("\r\n\r\n")

let mutable part1 = 0
let mutable part2 = 0

for group in data do
    let group = group.Split("\r\n")
    let mutable union = Set group.[0]
    let mutable intersection = Set group.[0]

    for person in group.[1..] do
        union <- Set.union union (Set person)
        intersection <- Set.intersect intersection (Set person)

    part1 <- part1 + union.Count
    part2 <- part2 + intersection.Count

printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
