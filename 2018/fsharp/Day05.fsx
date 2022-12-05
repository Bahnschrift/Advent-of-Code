#load "Utils.fsx"
open Utils
open System
open System.IO
open System.Text.RegularExpressions
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText "../inputs/05.txt"
let mutable part1 = 0
let mutable part2 = -1

let polymerLength (inp: String): int = 
    let mutable str = inp.ToCharArray()
    let mutable cont = true
    while cont do
        cont <- false
        let ind = (str |> Seq.pairwise |> Seq.tryFindIndex (fun x -> (fst x |> Char.ToLower) = (snd x |> Char.ToLower) && fst x <> snd x))
        if ind.IsSome then
            cont <- true
            str <- Array.append str.[ .. ind.Value - 1] str.[ind.Value + 2 .. ]
    str.Length

part1 <- polymerLength data

for c in "abcdefghijklmnopqrstuvwxyz" do
    let withoutC = data |> String.filter (fun x -> x <> c && x <> (c |> Char.ToUpper))
    let cLength = polymerLength withoutC
    if part2 = -1 || cLength < part2 then
        part2 <- cLength

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds