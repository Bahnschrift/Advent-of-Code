open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/01.txt"))
let mutable part1 = 0
let mutable part2 = -1

for x in [1 .. data.Length] do
    let c = data.[x - 1]
    if c = '(' then
        part1 <- part1 + 1
    else if c = ')' then
        part1 <- part1 - 1
        
    if part2 = -1 && part1 < 0 then
        part2 <- x


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds