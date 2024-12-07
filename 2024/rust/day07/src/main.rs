fn main() {
    let input = include_str!("../../../inputs/day07.txt").trim();

    let mut ans = 0;

    for line in input.lines() {
        let (astr, bsstr) = line.split_once(": ").unwrap();
        let a = astr.parse::<u64>().unwrap();
        let bs: Vec<_> = bsstr
            .split_terminator(" ")
            .map(|b| b.parse::<u64>().unwrap())
            .collect();

        let mut stack = Vec::new();
        stack.push((a, (bs.len() - 1) as i32));

        while !stack.is_empty() {
            let (b, i) = stack.pop().unwrap();

            if i == -1 || b == 0 {
                if i == -1 && b == 0 {
                    ans += a;
                    break;
                }

                continue;
            }

            let next = bs[i as usize];
            if next <= b {
                stack.push((b - next, i - 1));

                let next_len = next.checked_ilog10().unwrap() + 1;
                let b_rem = b - next;
                if b_rem % 10u64.pow(next_len) == 0 {
                    stack.push((b_rem / 10u64.pow(next_len), i - 1));
                }
            }

            if b % next == 0 {
                stack.push((b / next, i - 1));
            }
        }
    }

    println!("{}", ans);
}
