open System
open System.IO
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/10.txt")).TrimEnd()
let mutable part1 = 0
let mutable part2 = 0

let group str =
    if String.length str = 0 then Seq.empty
    else
        seq {
            let mutable last = str.[0]
            let mutable count = 0
            for c in str do
                if last <> c then
                    yield (last, count)
                    last <- c
                    count <- 1
                else
                    count <- count + 1
            yield (last, count)
        }

let lookAndSay str = 
    let sb = Text.StringBuilder()
    group str |> Seq.iter (fun (c, count) -> sb.Append(count).Append(c) |> ignore)
    sb.ToString()

let part1String = seq{1 .. 40} |> Seq.fold (fun i _ -> lookAndSay i) data
part2 <- seq{41 .. 50} |> Seq.fold (fun i _ -> lookAndSay i) part1String |> String.length
part1 <- part1String.Length

timer.Stop()
printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds