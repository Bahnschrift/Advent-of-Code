open System
open System.IO
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/03.txt"))
let mutable part1 = 0
let mutable part2 = 0

let deliveries = new Dictionary<int * int, int>()
let rdeliveries = new Dictionary<int * int, int>()
let directions = dict['^', (0, 1); 'v', (0, -1); '>', (1, 0); '<', (-1, 0)]
let mutable x = 0
let mutable y = 0
let mutable rsx = 0
let mutable rsy = 0
let mutable rrx = 0
let mutable rry = 0
deliveries.Add((x, y), 1)
rdeliveries.Add((x, y), 1)

for i in [0 .. data.Length - 1] do
    let c = data.[i]
    let dir = directions.Item(c)
    let (dx, dy) = dir

    x <- x + dx
    y <- y + dy

    if deliveries.ContainsKey (x, y) then
        deliveries.[(x, y)] <- deliveries.[(x, y)] + 1
    else 
        deliveries.Add((x, y), 1)
    
    if i % 2 = 0 then
        rrx <- rrx + dx
        rry <- rry + dy
        if rdeliveries.ContainsKey (rrx, rry) then
            rdeliveries.[(rrx, rry)] <- rdeliveries.[(rrx, rry)] + 1
        else 
            rdeliveries.Add((rrx, rry), 1)
    else
        rsx <- rsx + dx
        rsy <- rsy + dy
        if rdeliveries.ContainsKey (rsx, rsy) then
            rdeliveries.[(rsx, rsy)] <- rdeliveries.[(rsx, rsy)] + 1
        else 
            rdeliveries.Add((rsx, rsy), 1)

part1 <- deliveries.Count
part2 <- rdeliveries.Count


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds