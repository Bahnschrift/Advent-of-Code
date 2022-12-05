open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllLines(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/08.txt"))
let mutable part1 = 0
let mutable part2 = 0

for line in data do
    let fullLength = line.Length
    let mutable escapedLength = 0
    let mutable rescapedLength = fullLength + 2
    let mutable x = 1
    while x < fullLength - 1 do
        if line.[x] = '\\' then
            if line.[x + 1] = '\\' && x <> fullLength - 1 then
                escapedLength <- escapedLength + 1
                x <- x + 2
            else if line.[x + 1] = '"' && x <> fullLength - 1 then
                escapedLength <- escapedLength + 1
                x <- x + 2
            else if line.[x + 1] = 'x' && x <> fullLength - 3 then
                if line.[x + 2 .. x + 3] |> Seq.forall(fun x -> Seq.contains x "1234567890abcdef") then
                    escapedLength <- escapedLength + 1
                    x <- x + 4
                else
                    escapedLength <- escapedLength + 1
                    x <- x + 1
            else
                escapedLength <- escapedLength + 1
                x <- x + 1
        else
            escapedLength <- escapedLength + 1
            x <- x + 1
    
    for c in line do
        if Seq.contains c [|'\\'; '"'|] then
            rescapedLength <- rescapedLength + 1
    
    part1 <- part1 + fullLength - escapedLength
    part2 <- part2 - fullLength + rescapedLength

timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds