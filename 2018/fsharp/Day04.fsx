#load "Utils.fsx"
open Utils
open System
open System.IO
open System.Text.RegularExpressions
open System.Collections.Generic
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines "../inputs/04.txt" |> Array.sort
let mutable part1 = 0
let mutable part2 = 0

let mutable sleepTimes = new Dictionary<int, int * Dictionary<int, int>>()

let mutable guard = 0
let mutable time = 0
let mutable timeSlept = 0
for line in data do
    let minute = line.[15 .. 16] |> int
    if line.[19 .. 23] = "Guard" then
        guard <- line.Split().[3].[1 .. ] |> int
        if not (sleepTimes.ContainsKey guard) then
            sleepTimes.Add(guard, (0, new Dictionary<int, int>()))
        time <- -minute
        timeSlept <- 0
    else
        if line.Split().[2] = "wakes" then
            while time < minute - 1 do
                &time += 1
                sleepTimes.[guard] <- (fst sleepTimes.[guard] + 1, snd sleepTimes.[guard])
                if (snd sleepTimes.[guard]).ContainsKey time then
                    (snd sleepTimes.[guard]).[time] <- (snd sleepTimes.[guard]).[time] + 1
                else
                    (snd sleepTimes.[guard]).Add (time, 1)
        else
            time <- minute - 1
    

let mostSleep = (sleepTimes |> Seq.maxBy (fun x -> fst x.Value)).Key
part1 <- mostSleep * (snd sleepTimes.[mostSleep] |> Seq.maxBy (fun x -> x.Value) |> fun x -> x.Key)

let mutable bestMins = new Dictionary<int, int * int>()
for guard in sleepTimes.Keys do
    if fst sleepTimes.[guard] > 0 then
        let bestMin = snd sleepTimes.[guard] |> Seq.maxBy (fun x -> x.Value)
        bestMins.Add (guard, (bestMin.Key, bestMin.Value))

let bestGuard = (bestMins |> Seq.maxBy (fun x -> snd x.Value)).Key
part2 <- bestGuard * fst bestMins.[bestGuard]

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds