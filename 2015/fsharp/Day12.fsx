open System
open System.IO
open System.Text.RegularExpressions
#r "nuget: FSharp.Data"
open FSharp.Data
open Microsoft.FSharp.Core.Operators.Checked


let timer = Diagnostics.Stopwatch.StartNew()
let data = File.ReadAllText(Path.Combine(Directory.GetParent(__SOURCE_DIRECTORY__).FullName, "inputs/12.txt")).TrimEnd()
let mutable part1 = 0
let mutable part2 = 0

let json = JsonValue.Parse data

let rec parse filter (value: JsonValue) =
    match value with
    | JsonValue.Number n -> int n
    | JsonValue.Record r when not (filter r) -> r |> Array.sumBy (fun (x, y) -> parse filter y)
    | JsonValue.Array a -> a |> Array.sumBy (fun x -> parse filter x)
    | _ -> 0

let hasRedProperty (record: (string * JsonValue)[]) = 
    Array.exists (fun (x, y) ->
        match y with
        | JsonValue.String s when s = "red" -> true
        | _ -> false
    ) record

part1 <- parse (fun _ -> false) json
part2 <- parse hasRedProperty json

timer.Stop()
printfn "Part 1: %i" part1
printfn "Part 2: %i" part2
printfn "Time: %fs" timer.Elapsed.TotalSeconds