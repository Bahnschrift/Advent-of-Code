open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked
#load "Utils.fsx"
open Utils


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/18.txt"))
let mutable part1 = 0
let mutable part2 = 0

let buildGrid (data: string[]): bool[] list = 
    let mutable grid: bool[] list = []
    for row in data do
        let boolRow = 
            row.ToCharArray()
            |> Array.map (fun x -> x = '#') 
        grid <- grid @ [boolRow]
    grid

let mutable grid = buildGrid data

let neighbourPositions = [(1, 0); (-1, 0); (0, 1); (0, -1); (1, 1); (1, -1); (-1, -1); (-1, 1)]
let doMove (grid: bool[] list): bool[] list = 
    let newGrid = [for line in grid do [|for cell in line do cell|]]
    for y in {0 .. grid.Length - 1} do
        for x in {0 .. grid.[y].Length - 1} do
            let mutable neighbourCount = 0
            for neighbourPos in neighbourPositions do
                let (nx, ny) = (x + (fst neighbourPos), y + (snd neighbourPos))
                if 0 <= ny && ny < grid.Length && 0 <= nx && nx < grid.[x].Length then
                    if grid.[ny].[nx] then
                        &neighbourCount += 1
            if grid.[y].[x] && not(neighbourCount = 2 || neighbourCount = 3) then
                newGrid.[y].[x] <- false
            elif not grid.[y].[x] && neighbourCount = 3 then
                newGrid.[y].[x] <- true
    newGrid

let printGrid grid = 
    for line in grid do
        let l = 
            line
            |> Array.map (fun x -> if x then "#" else ".")
            |> String.concat ""
        printfn "%s" l

for _ in {1 .. 100} do
    grid <- doMove grid
part1 <- List.sum [for row in grid do List.sum [for cell in row do if cell then 1 else 0]]

grid <- buildGrid data
let setCorners (state: bool) (grid: bool[] list): bool[] list = 
    grid.[0].[0] <- state
    grid.[grid.Length - 1].[0] <- state
    grid.[grid.Length - 1].[grid.[0].Length - 1] <- state
    grid.[0].[grid.[0].Length - 1] <- state
    grid

setCorners true grid
for _ in {1 .. 100} do
    grid <- grid |> doMove |> setCorners true
part2 <- List.sum [for row in grid do List.sum [for cell in row do if cell then 1 else 0]]

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds