module List = 
    let product (lst: seq<'a>) (repeat: int): list<list<'a>> = 
        let pools = List.replicate repeat lst
        let mutable result = [[]]
        for pool in pools do
            result <- [for x in result do for y in pool do x @ [y]]
        result

    let permutations (lst: seq<'a>) (r: int) = 
        let pool = Array.ofSeq lst
        let n = Seq.length lst
        let mutable result = []
        for indices in (product {0 .. n - 1} r) do
            if Set indices |> Seq.length = r then
                result <- result @ [[for x in indices do pool.[x]]]
        result

    let combinationss (lst: seq<'a>) (r: int) = 
        let pool = Array.ofSeq lst
        let n = Seq.length lst
        let mutable result = []
        for indices in (permutations {0 .. n - 1} r) do
            if List.sort indices = indices then
                result <- result @ [[for x in indices do pool.[x]]]
        result

    let combinations (lst: seq<'a>) (r: int) = 
        let pool = List.ofSeq lst
        let n = pool.Length
        let indices = [|0 .. r - 1|]
        let mutable cont = true
        let mutable result = [[for x in indices do pool.[x]]]
        while cont do
            let mutable last = 0
            cont <- false
            for i in {r - 1 .. -1 .. 0} do
                if not cont then
                    last <- i
                if indices.[i] <> i + n - r then
                    cont <- true
            if cont then
                indices.[last] <- indices.[last] + 1
                for j in {last + 1 .. r - 1} do
                    indices.[j] <- indices.[j - 1] + 1
                result <- result @ [[for x in indices do pool.[x]]]
        result
        
    let crombinations lst =
        let rec comb accLst elemLst =
            match elemLst with
            | h::t ->
                let next = [h]::List.map (fun el -> h::el) accLst @ accLst
                comb next t
            | _ -> accLst
        comb [] lst

let l = [1 .. 20]
let timer = System.Diagnostics.Stopwatch.StartNew()
let startTime = timer.Elapsed.TotalSeconds
printfn "%A" (List.combinations l 16 |> List.length)
printfn "%A" (timer.Elapsed.TotalSeconds - startTime)
// printfn "%A" (List.product l 2)
// printfn "%A" (List.permutations l 2)
// printfn "%A" (List.combinationss l 3)
// printfn "%A" (List.combinations l 3)