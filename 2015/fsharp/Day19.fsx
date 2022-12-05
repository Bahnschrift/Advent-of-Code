open System
open System.IO
#load "Utils.fsx"
open Utils
open System.Collections.Generic
open System.Text.RegularExpressions
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/19.txt")).Split("\r\n\r\n")
let mutable part1 = 0
let mutable part2 = 0

let getElements str = 
    Regex.Matches(str, "[A-Z][a-z]?") |> List.ofSeq |> List.map string

let replacements = new Dictionary<string, string list list>()
for line in data.[0].Split("\r\n") do
    let line = line.Split(" => ")
    let inp = line.[0]
    let out = getElements line.[1]
    if replacements.ContainsKey inp then
        replacements.[inp] <- replacements.[inp] @ [out]
    else
        replacements.Add(inp, [out])

let elements = getElements data.[1]
let mutable seen = new Set<string list>([])

for elementInd in {0 .. elements.Length - 1} do
    let element = elements.[elementInd]
    if replacements.ContainsKey(element) then
        for replacement in replacements.[element] do
            seen <- seen |> Set.add (elements.[ .. elementInd - 1] @ replacement @ elements.[elementInd + 1 .. ])
part1 <- Seq.length seen

let countRnAr = elements |> List.countBy (fun x -> x = "Rn" || x = "Ar") |> List.last |> snd
let countY = elements |> List.countBy (fun x -> x = "Y") |> List.last |> snd
part2 <- elements.Length - countRnAr - 2 * countY - 1

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds