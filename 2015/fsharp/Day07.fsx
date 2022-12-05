open System
open System.IO
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/07.txt"))
let mutable part1 = 0
let mutable part2 = 0

let states = new Dictionary<string, string>()
let solved = new Dictionary<string, int>()  // Dynamic programming cool
for line in data do
    let line = line.Split(" -> ")
    states.Add(line.[1], line.[0])

let rec get value: int = 
    let mutable returnVal = 0
    if solved.ContainsKey value then
        returnVal <- solved.[value]
    else if value |> Seq.forall Char.IsDigit then
        returnVal <- int value
    else
        let expr = states.[value]
        let parts = expr.Split()

        if expr |> Seq.forall Char.IsDigit then
            returnVal <- int expr
        else if parts.Length = 1 then
            returnVal <- get parts.[0]
        else if parts.[0] = "NOT" then
            returnVal <- ~~~(get parts.[1])
        else if parts.[1] = "AND" then
            returnVal <- (get parts.[0]) &&& (get parts.[2])
        else if parts.[1] = "OR" then
            returnVal <- (get parts.[0]) ||| (get parts.[2])
        else if parts.[1] = "LSHIFT" then
            returnVal <- (get parts.[0]) <<< (get parts.[2])
        else if parts.[1] = "RSHIFT" then
            returnVal <- (get parts.[0]) >>> (get parts.[2])

    if not (solved.ContainsKey value) then
        solved.Add(value, returnVal)
    returnVal
part1 <- get "a"

states.["b"] <- part1.ToString()
solved.Clear()
part2 <- get "a"


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds