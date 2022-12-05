open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/14.txt"))
let mutable part1 = 0
let mutable part2 = 0

type Reindeer(name, moveSpeed, moveTime, restTime) =  // Probably should've just used a dictionary...
    let mutable tick = 0
    let mutable distance = 0
    let mutable state = "Resting"
    let mutable points = 0
    member this.Name: string = name
    member this.MoveSpeed: int = moveSpeed
    member this.MoveTime: int = moveTime
    member this.RestTime: int = restTime
    
    member this.GetTick = tick
    member this.SetTick x = tick <- x
    member this.GetDistance = distance
    member this.SetDistance x = distance <- x
    member this.GetState = state
    member this.GetPoints = points
    member this.SetPoints x = points <- points + x
    member this.GivePoint = points <- points + 1
    member this.DoTick = 
        this.SetTick (tick + 1)
        if tick > this.MoveTime + this.RestTime then
            this.SetTick 1
        if tick <= moveTime then
            state <- "Moving"
            this.SetDistance (distance + moveSpeed)
        else
            state <- "Resting"    
    member this.GetInfo = 
        sprintf "Name: %s; Distance: %i; Points: %i; Tick: %i; State: %s" this.Name distance points tick state
    
    static member SGetTick (reindeer: Reindeer) = reindeer.GetTick
    static member SGetDistance (reindeer: Reindeer) = reindeer.GetDistance
    static member SGetState (reindeer: Reindeer) = reindeer.GetState
    static member SGetPoints (reindeer: Reindeer) = reindeer.GetPoints
    static member SGivePoint (reindeer: Reindeer) = reindeer.GivePoint
    static member SDoTick (reindeer: Reindeer) = reindeer.DoTick
    static member SGetInfo (reindeer: Reindeer) = reindeer.GetInfo

let mutable reindeer: Reindeer list = []
for line in data do
    let line = line.Split()
    let name = line.[0]
    let moveSpeed = int line.[3]
    let moveTime = int line.[6]
    let restTime = int line.[13]
    reindeer <- List.append reindeer [Reindeer(name, moveSpeed, moveTime, restTime)]

let doFullTick (reindeerList: Reindeer list) = 
    reindeerList |> Seq.iter Reindeer.SDoTick    
    reindeer
    |> Seq.maxBy (fun x -> x.GetDistance)
    |> Reindeer.SGivePoint

for _ in {1 .. 2503} do
    doFullTick reindeer

part1 <- 
    reindeer
    |> Seq.maxBy (fun x -> x.GetDistance)
    |> Reindeer.SGetDistance

part2 <- 
    reindeer
    |> Seq.maxBy (fun x -> x.GetPoints)
    |> Reindeer.SGetPoints

timer.Stop()
printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds