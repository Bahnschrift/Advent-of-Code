open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/11.txt")).TrimEnd()
let mutable part1 = ""
let mutable part2 = ""

let increment (str: string) = 
    let mutable str = str.ToCharArray() |> Array.map int
    let mutable cont = true
    let mutable pos = str.Length - 1
    while cont do
        str.[pos] <- str.[pos] + 1
        if str.[pos] > int 'z' then
            str.[pos] <- int 'a'
            pos <- pos - 1
            if pos = -1 then  // This should never happen
                str <- Array.append [|int 'a'|] str
                cont <- false
        else
            cont <- false
    String.Concat(Array.map char str)

let mutable cont = true
let mutable pass = data
while cont do
    pass <- increment pass
    let mutable straightCheck = false
    let mutable badCharsCheck = not <| pass.Contains('i') || pass.Contains('o') || pass.Contains('l')
    let mutable overlapCheck = false
    for x in seq{0 .. pass.Length - 3} do
        if not straightCheck then
            if int pass.[x + 2] - int pass.[x + 1] = 1 && int pass.[x + 1] - int pass.[x] = 1 then
                straightCheck <- true

    let pairs = 
        pass
        |> Seq.pairwise
        |> Seq.filter (fun (a, b) -> a = b)
        |> set
    if Seq.length pairs > 1 then
        overlapCheck <- true

    if straightCheck && badCharsCheck && overlapCheck then
        if part1 = "" then
            part1 <- pass
        else
            part2 <- pass
            cont <- false

timer.Stop()
printfn "Part 1: %s" part1
printfn "Part 2: %s" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds