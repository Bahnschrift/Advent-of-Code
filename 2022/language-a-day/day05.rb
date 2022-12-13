inpFile = File.open("./2022/inputs/day5.txt")
inp = inpFile.read.split("\n\n").map{|g| g.split("\n")}
inpFile.close

crates, instructions = inp
num_crates = crates[0].length / 4 + 1
contents_1 = Array.new(num_crates) { Array.new() }

crates.length.times do |i|
    crates[i].length.times do |j|
        c = crates[i][j]
        if c =~ /[A-Z]/
            index = j / 4
            contents_1[index].unshift c
        end
    end
end

contents_2 = Marshal.load(Marshal.dump(contents_1))

instructions.each do |ins|
    move, from, to = ins.scan(/\d+/).map(&:to_i)
    from -= 1
    to -= 1

    contents_1[to].push(*contents_1[from][-move..].reverse)
    contents_1[from] = contents_1[from][..-move - 1]

    contents_2[to].push(*contents_2[from][-move..])
    contents_2[from] = contents_2[from][..-move - 1]
end

part_1 = contents_1.map{|c| c[-1]}.join("")
part_2 = contents_2.map{|c| c[-1]}.join("")
puts "Part 1: #{part_1}"
puts "Part 2: #{part_2}"
