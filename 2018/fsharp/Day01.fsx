#load "Utils.fsx"
open Utils
open System
open System.IO
open System.Text.RegularExpressions
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines "../inputs/01.txt"
        |> Array.map int
let mutable part1 = 0
let mutable part2 = 0

let mutable visited = new Set<int>([])
let mutable vall = 0
part1 <- Array.sum data

while (part2 = 0) do
    for ins in data do
        &vall += ins
        if (part2 = 0 && Set.contains vall visited) then
            part2 <- vall
        visited <- visited.Add(vall)


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds