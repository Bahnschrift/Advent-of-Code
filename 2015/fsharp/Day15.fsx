open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/15.txt"))
let mutable part1 = 0
let mutable part2 = 0

let mutable ingredientsWithoutCalories = [||]
let mutable calories = [||]
for line in data do
    let line = line.Split()
    let capacity = line.[2].Remove(line.[2].Length - 1) |> int
    let durability = line.[4].Remove(line.[4].Length - 1) |> int
    let flavour = line.[6].Remove(line.[6].Length - 1) |> int
    let texture = line.[8].Remove(line.[8].Length - 1) |> int
    calories <- Array.append calories [|line.[10] |> int|]
    ingredientsWithoutCalories <- Array.append ingredientsWithoutCalories [|[capacity; durability; flavour; texture]|]

let calculate (ingredients: int list[]) (amounts: int[]): int = 
    let mutable total = 1
    for atrIndex in {0 .. ingredients.[0].Length - 1} do
        let mutable atrTotal = 0
        for ingIndex in {0 .. amounts.Length - 1} do
            atrTotal <- atrTotal + amounts.[ingIndex] * ingredients.[ingIndex].[atrIndex]
        total <- if atrTotal > 0 then total * atrTotal else 0
    total

for a in {0 .. 100} do
    for b in {0 .. 100} do
        for c in {0 .. 100} do
            for d in {0 .. 100} do
                let amounts = [|a; b; c; d|]
                if Array.sum amounts = 100 then
                    let total = calculate ingredientsWithoutCalories amounts
                    if total > part1 then
                        part1 <- total
                    let calorySum = 
                        (calories, amounts)
                        ||> Seq.zip
                        |> Seq.sumBy (fun (x, y) -> x * y)
                    if calorySum = 500 && total > part2 then
                        part2 <- total

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds