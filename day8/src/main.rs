use std::{fs, time::Instant};

fn get_input() -> String {
    let s = String::from(
        "LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)",
    );
    // let s = fs::read_to_string("input/day8_1").unwrap();

    s
}

fn parse_map_into_graph(array: Vec<&str>) {
    let map = &array[2..];
    for l in map {
        dbg!(&l);
    }
}

fn main() {
    let s = get_input();
    let array: Vec<_> = s.lines().collect();
    let now = Instant::now();
    let _instruction_list = array[0].chars();
    parse_map_into_graph(array);
    println!("elapsed: {:?}", now.elapsed());
}
