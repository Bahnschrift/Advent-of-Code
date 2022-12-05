open System
open System.IO
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


module List =  // http://www.fssnip.net/4u/title/Very-Fast-Permutations
    let rec permutations = function
        | []      -> seq [List.empty]
        | x :: xs -> Seq.collect (insertions x) (permutations xs)
    and insertions x = function
        | []             -> [[x]]
        | (y :: ys) as xs -> (x::xs)::(List.map (fun x -> y::x) (insertions x ys))

let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/09.txt"))
let mutable part1 = 0
let mutable part2 = 0

let distances = new Dictionary<Set<string>, int>()
let mutable all = new Set<string>([])
for line in data do
    let line = line.Split " = "
    let places = line.[0].Split " to "
    let distance = int line.[1]
    distances.Add (Set places, distance)
    for place in places do
        all <- all.Add place

let mutable bestPerm = (-1, [""])
let mutable worstPerm = (-1, [""])
let perms = 
    all
    |> Set.toList
    |> List.permutations
for perm in perms do
    let mutable totalDistance = 0
    for x in [0 .. perm.Length - 2] do
        let pair = Set perm.[x .. x + 1]
        totalDistance <- totalDistance + distances.[pair]
    if totalDistance < fst bestPerm || fst bestPerm = -1 then
        bestPerm <- (totalDistance, perm)
    if totalDistance > fst worstPerm || fst worstPerm = -1 then
        worstPerm <- (totalDistance, perm)

part1 <- fst bestPerm
part2 <- fst worstPerm

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds