#load "Utils.fsx"
open Utils
open System
open System.IO
open System.Text.RegularExpressions
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines "../inputs/02.txt"
let mutable part1 = 0
let mutable part2 = ""

let mutable passed2 = 0
let mutable passed3 = 0
for word in data do
    let mutable pass2 = false
    let mutable pass3 = false
    for c in word do
        if (word
            |> String.filter (fun x -> x = c)
            |> String.length = 2) then pass2 <- true
        elif (word
            |> String.filter (fun x -> x = c)
            |> String.length = 3) then pass3 <- true
    
        // printfn "%A" pass2
    if pass2 then &passed2 += 1
    if pass3 then &passed3 += 1
part1 <- passed2 * passed3

for a in {0 .. data.Length - 2} do
    for b in {a + 1 .. data.Length - 1} do
        let x = data.[a]
        let y = data.[b]
        for c in {0 .. x.Length - 1} do
            if (x.[ .. c - 1] + x.[c + 1 .. ] = y.[ .. c - 1] + y.[c + 1 .. ]) then
                part2 <- x.[ .. c - 1] + x.[c + 1 .. ]


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %s" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds