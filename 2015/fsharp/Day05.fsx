open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/05.txt"))
let mutable part1 = 0
let mutable part2 = 0

for line in data do
    let vowels = "aeiou".ToCharArray()
    let vowelCount = 
        line
        |> Seq.filter (fun x -> Array.contains x vowels)
        |> Seq.length
    let vowelCheck = vowelCount >= 3

    let mutable pairs = []
    let mutable pairCheck = false
    let mutable badCheck = true
    let mutable pairCheck2 = false
    let mutable tripleCheck2 = false
    for x in [0 .. line.Length - 2] do
        let pair = line.[x .. x + 1]
        pairs <- pairs @ [pair]
        if Set pair |> Set.count = 1 then
            pairCheck <- true
        for bad in [|"ab"; "cd"; "pq"; "xy"|] do
            if pair = bad then badCheck <- false
        
        if List.contains pair pairs.[ .. x - 2] then pairCheck2 <- true
        if x <> line.Length - 2 && pair.[0] = line.[x + 2] then tripleCheck2 <- true
    
    if vowelCheck && pairCheck && badCheck then part1 <- part1 + 1    
    if pairCheck2 && tripleCheck2 then part2 <- part2 + 1
       
timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds