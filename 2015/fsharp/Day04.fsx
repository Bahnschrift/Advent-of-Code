open System
open System.IO
open System.Security.Cryptography
open Microsoft.FSharp.Core.Operators.Checked


let hash (md5: Security.Cryptography.MD5, str: string): string =
    str
    |> System.Text.Encoding.ASCII.GetBytes
    |> md5.ComputeHash
    |> Seq.map (fun x -> x.ToString("X2"))
    |> Seq.reduce ( + )

let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/04.txt")).TrimEnd()
let mutable part1 = 0
let mutable part2 = 0
let md5 = MD5.Create()

let mutable x = 0
while hash(md5, data + (string x)).[ .. 4] <> "00000" do x <- x + 1
part1 <- x

x <- x * 2
while hash(md5, data + (string x)).[ .. 5] <> "000000" do x <- x + 1
part2 <- x


timer.Stop()
printfn "Part 1: %A" part1
printfn "Part 2: %A" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds