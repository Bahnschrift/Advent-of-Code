open System
open System.IO
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


module List =  // http://www.fssnip.net/4u/title/Very-Fast-Permutations
    let rec permutations = function
        | []      -> seq [List.empty]
        | x :: xs -> Seq.collect (insertions x) (permutations xs)
    and insertions x = function
        | []              -> [[x]]
        | (y :: ys) as xs -> (x :: xs) :: (List.map (fun x -> y :: x) (insertions x ys))

let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/13.txt"))
let mutable part1 = 0
let mutable part2 = 0

let happinessGuide = new Dictionary<string, Dictionary<string, int>>()
for line in data do
    let line = line.Split()
    let p1 = line.[0]
    let p2 = line.[10] |> fun x -> x.Remove(x.Length - 1)
    let plusOrMinus = if line.[2] = "gain" then 1 else -1
    let change = int line.[3] * plusOrMinus
    if happinessGuide.ContainsKey p1 then
        happinessGuide.[p1].Add(p2, change)
    else
        happinessGuide.Add(p1, new Dictionary<string, int>())
        happinessGuide.[p1].Add(p2, change)

let calculateHappiness (arrangement: string list) =
    let mutable happiness = 0
    let first = arrangement.[0]
    let last = arrangement.[arrangement.Length - 1]
    for x in seq{0 .. arrangement.Length - 1} do
        let p1 = if x = 0 then last else arrangement.[x - 1]
        let p2 = arrangement.[x]
        let p3 = if x = arrangement.Length - 1 then first else arrangement.[x + 1]  // Such that p2 is seated between p1 and p3
        happiness <- happiness + happinessGuide.[p2].[p1]
        happiness <- happiness + happinessGuide.[p2].[p3]
    happiness

let people1 = happinessGuide.Keys |> List.ofSeq
let arrangements1 = List.permutations people1
part1 <- 
    arrangements1 
    |> Seq.maxBy calculateHappiness 
    |> calculateHappiness

happinessGuide.Add("me", new Dictionary<string, int>())
for person in people1 do
    happinessGuide.["me"].Add(person, 0)
    happinessGuide.[person].Add("me", 0)

let people2 = happinessGuide.Keys |> List.ofSeq
let arrangements2 = List.permutations people2
part2 <- 
    arrangements2
    |> Seq.maxBy calculateHappiness 
    |> calculateHappiness

timer.Stop()
printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds