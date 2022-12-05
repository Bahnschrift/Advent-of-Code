open System
open System.IO
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked
#load "Utils.fsx"
open Utils


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/20.txt")).TrimEnd()
let mutable part1 = 0
let mutable part2 = 0


let N = int data
let houses = new Dictionary<int, int>()
for i in {1 .. N / 10} do
    for j in {i .. i .. N / 10} do
        if houses.ContainsKey(j) then
            houses.[j] <- houses.[j] + i * 10
        else
            houses.Add(j, i * 10)
for h in houses do
    if part1 = 0 then
        let n, v = h.Deconstruct()
        if v >= N then
            part1 <- n

houses.Clear()
for i in {1 .. N / 10} do
    let mutable c = 0
    for j in {i .. i .. N / 10} do
        if c < 50 then
            &c += 1
            if houses.ContainsKey(j) then
                houses.[j] <- houses.[j] + i * 11
            else
                houses.Add(j, i * 11)
for h in houses do
    if part2 = 0 then
        let n, v = h.Deconstruct()
        if v >= N then
            part2 <- n

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds