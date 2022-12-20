let ( |/ ) (x) (y) = float x / float y 
let ( /| ) (x) (y) = int x / int y 

let ( += ) (x: byref<_>) (y: _) = x <- x + y 
let ( -= ) (x: byref<_>) (y: _) = x <- x + y 
let ( *= ) (x: byref<_>) (y: _) = x <- x * y 
let ( /= ) (x: byref<_>) (y: _) = x <- x / y 
let ( |/= ) (x: byref<_>) (y: _) = x <- x |/ y 
let ( /|= ) (x: byref<_>) (y: _) = x <- x /| y 
let ( **= ) (x: byref<_>) (y: _) = x <- pown x y 
let ( %= ) (x: byref<_>) (y: _) = x <- x % y 
let ( +== ) (x: byref<int>, y: byref<int>) (dx: int, dy: int) = x <- x + dx; y <- y + dy 

module List = 
    let combinations lst =
        let rec comb accLst elemLst =
            match elemLst with
            | h::t ->
                let next = [h]::List.map (fun el -> h::el) accLst @ accLst
                comb next t
            | _ -> accLst
        comb [] lst