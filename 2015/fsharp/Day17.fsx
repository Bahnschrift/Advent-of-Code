open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked
module List =  // http://www.fssnip.net/4u/title/Very-Fast-Permutations
    let rec permutations = function
        | []      -> seq [List.empty]
        | x :: xs -> Seq.collect (insertions x) (permutations xs)
    and insertions x = function
        | []              -> [[x]]
        | (y :: ys) as xs -> (x :: xs) :: (List.map (fun x -> y :: x) (insertions x ys))
    let combinations lst =
        let rec comb accLst elemLst =
            match elemLst with
            | h::t ->
                let next = [h]::List.map (fun el -> h::el) accLst @ accLst
                comb next t
            | _ -> accLst
        comb [] lst

let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/17.txt"))
let mutable part1 = 0
let mutable part2 = 0

let containers = 
    data 
    |> Seq.map int 
    |> List.ofSeq
let ways = List.combinations containers

let validWays = ways |> Seq.filter (fun x -> Seq.sum x = 150)

part1 <- validWays |> Seq.length
let smallest = validWays |> Seq.minBy Seq.length |> Seq.length
part2 <- 
    validWays 
    |> Seq.filter (fun x -> Seq.length x = smallest) 
    |> Seq.length

printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds