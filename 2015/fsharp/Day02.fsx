open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/02.txt"))
let mutable part1 = 0
let mutable part2 = 0

for line in data do
    let mutable line = line.Split("x") |> Array.map int
    let w = line.[0]
    let h = line.[1]
    let l = line.[2]
    line <- Array.append line.[0 .. Array.IndexOf (line, Array.max line) - 1] line.[Array.IndexOf (line, Array.max line) + 1 .. ]
    let sides = [l * w; w * h; h * l]
    part1 <- part1 + 2 * List.sum sides + List.min sides
    
    part2 <- part2 + 2 * Array.sum line + w * h * l


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds