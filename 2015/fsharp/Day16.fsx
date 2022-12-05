open System
open System.IO
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/16.txt"))
let mutable part1 = 0
let mutable part2 = 0

let mutable sues: Dictionary<string, int> list = []  // Index + 1 = Sue number
let categories = [|"children"; "cats"; "samoyeds"; "pomeranians"; "akitas"; "vizslas"; "goldfish"; "trees"; "cars"; "perfumes"|]
let normalCategories = [|"children"; "samoyeds"; "akitas"; "vizslas"; "cars"; "perfumes"|]
let largerCategories = [|"cats"; "trees"|]
let smallerCategories = [|"goldfish"; "pomeranians"|]
let correctSue = new Dictionary<string, int>()

for (k, v) in (Array.zip categories [|3; 7; 2; 3; 0; 0; 5; 3; 2; 1|]) do
   correctSue.Add(k, v)

for line in data do
    let line = 
        line.Split().[2 .. ] 
        |> String.concat ""
        |> fun x -> x.Split ","
    let sue = new Dictionary<string, int>()
    for category in line do
        let category = category.Split ":"
        sue.Add(category.[0], int category.[1])
    sues <- sues @ [sue]

for sueIndex in {0 .. 499} do
    let sue = sues.[sueIndex]
    if (
        categories
        |> Seq.forall (fun x -> not(sue.ContainsKey x) || sue.[x] = correctSue.[x])
    ) then
        part1 <- sueIndex + 1
        if (
            largerCategories
            |> Seq.forall (fun x -> not(sue.ContainsKey x) || sue.[x] > correctSue.[x])
        ) 
        && 
        (
            smallerCategories
            |> Seq.forall (fun x -> not(sue.ContainsKey x) || sue.[x] < correctSue.[x])
        ) then
            part2 <- sueIndex + 1

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds