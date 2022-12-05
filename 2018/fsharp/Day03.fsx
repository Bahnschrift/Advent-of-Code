#load "Utils.fsx"
open Utils
open System
open System.IO
open System.Text.RegularExpressions
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data: string[] = File.ReadAllLines "../inputs/03.txt"
let mutable part1 = 0
let mutable part2 = 0

let mutable grid: array<array<array<int>>> = [|for y in {1 .. 1000} do [|for x in {1 .. 1000} do [||]|]|]
let mutable counts = new Dictionary<int, (int * int)>()

for line in data do
    let line = line.Split(' ')
    let id = int line.[0].[1 .. ]
    let coords = line.[2].Split(',')
    let x = int coords.[0]
    let y = int coords.[1].[ .. String.length coords.[1] - 2]
    let dims = line.[3].Split('x')
    let w = int dims.[0]
    let h = int dims.[1]
    counts.Add (id, (w * h, 0))

    for a in {y .. y + h - 1} do
        for b in {x .. x + w - 1} do
            grid.[a].[b] <- Array.append grid.[a].[b] [|id|]

            if grid.[a].[b].Length = 1 then
                counts.[id] <- (fst counts.[id], snd counts.[id] + 1)
            elif grid.[a].[b].Length = 2 then
                counts.[grid.[a].[b].[0]] <- (fst counts.[grid.[a].[b].[0]], snd counts.[grid.[a].[b].[0]] - 1)

for x in grid do
    for y in x do
        if y.Length > 1 then
            &part1 += 1
        
for id in counts.Keys do
    if fst counts.[id] = snd counts.[id] then
        part2 <- id

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds