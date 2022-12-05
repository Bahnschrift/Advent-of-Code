open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/06.txt"))
let mutable part1 = 0
let mutable part2 = 0

let mutable grid1 = [| for _ in 1 .. 1000 * 1000 -> false|]
let mutable grid2 = [| for _ in 1 .. 1000 * 1000 -> 0|]

let print thing = 
    printfn "%A" thing

for line in data do
    let mutable (starts, ends) = (0, 0)
    let line = line.Split()
    let mutable instruction = ""
    if line.[0] = "toggle" then
        starts <- 1
        ends <- 3
        instruction <- "toggle"
    else
        starts <- 2
        ends <- 4
        instruction <- line.[1]
    let startPos = line.[starts].Split(",") |> Array.map int
    let sx = startPos.[0]
    let sy = startPos.[1]
    let endPos = line.[ends].Split(",") |> Array.map int
    let ex = endPos.[0]
    let ey = endPos.[1]


    for x in [sx .. ex] do
        for y in [sy .. ey] do
            if instruction = "toggle" then
                grid1.[x * 1000 + y] <- not grid1.[x * 1000 + y]
                grid2.[x * 1000 + y] <- grid2.[x * 1000 + y] + 2
            elif instruction = "on" then
                grid1.[x * 1000 + y] <- true
                grid2.[x * 1000 + y] <- grid2.[x * 1000 + y] + 1
            elif instruction = "off" then
                grid1.[x * 1000 + y] <- false
                if grid2.[x * 1000 + y] > 0 then grid2.[x * 1000 + y] <- grid2.[x * 1000 + y] - 1

part1 <- Seq.filter id grid1 |> Seq.length
part2 <- Seq.sum grid2

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds