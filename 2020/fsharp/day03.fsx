open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked

let data =
    (__SOURCE_DIRECTORY__
     |> Directory.GetParent
     |> fun x -> x.FullName, "inputs/day03.txt")
    |> Path.Combine
    |> File.ReadAllLines

let mutable part1 = int64 0
let mutable part2 = int64 0

let toboggan right down =
    let mutable c = 0
    let mutable x = 0
    let mutable y = 0

    while y < data.Length do
        if data.[y].[x] = '#' then c <- c + 1
        x <- (x + right) % String.length data.[0]
        y <- y + down

    int64 c

part1 <- toboggan 3 1

part2 <-
    toboggan 1 1
    * part1
    * toboggan 5 1
    * toboggan 7 1
    * toboggan 1 2

printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
