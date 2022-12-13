let inpFname = "./2022/inputs/day3.txt"

let lines fname = System.IO.File.ReadAllLines fname

let priority c =
    [ 'a' .. 'z' ] @ [ 'A' .. 'Z' ]
    |> List.findIndex (fun x -> x = c)
    |> (+) 1

let part1 (inp: string []) =
    inp
    |> Seq.map (fun line ->
        [line[0 .. line.Length / 2 - 1]; line[line.Length / 2 .. line.Length - 1]]
        |> Seq.map Set
        |> Seq.reduce Set.intersect
        |> Seq.map priority
        |> Seq.sum)
    |> Seq.sum

let part2 (inp: string []) =
    inp
    |> Seq.chunkBySize 3
    |> Seq.map (fun group ->
        group
        |> Seq.map Set
        |> Seq.reduce Set.intersect
        |> Seq.map priority
        |> Seq.sum)
    |> Seq.sum

printfn "Part 1: %d" (inpFname |> lines |> part1)
printfn "Part 2: %d" (inpFname |> lines |> part2)
