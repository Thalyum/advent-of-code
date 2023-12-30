use std::collections::HashMap;
use std::{fs, time::Instant};

static START: &str = "AAA";
static LOOP_LIMIT: u32 = 10000;

fn get_input() -> String {
    //     String::from(
    //         "LLR

    // AAA = (BBB, BBB)
    // BBB = (AAA, ZZZ)
    // ZZZ = (ZZZ, ZZZ)",
    //     )
    fs::read_to_string("input/day8_1").unwrap()
}

#[derive(Debug)]
struct Paths {
    left: String,
    right: String,
}

fn parse_map_into_graph(map: Vec<&str>) -> (HashMap<String, Paths>, Vec<String>) {
    let mut start = Vec::new();
    let mut nodes: HashMap<String, Paths> = HashMap::new();
    for l in map {
        let (origin, paths) = l.split_once('=').unwrap();
        let origin = origin.trim();
        let (left, right) = paths.split_once(',').unwrap();
        let x: &[_] = &['(', ')', ' '];
        let (left, right) = (
            left.trim_matches(x).to_owned(),
            right.trim_matches(x).to_owned(),
        );
        if &origin[2..] == "A" {
            start.push(String::from(origin));
        }
        nodes.insert(origin.to_owned(), Paths { left, right });
    }
    (nodes, start)
}

fn follow(instructions: &Vec<char>, map: &HashMap<String, Paths>, start: &str) -> usize {
    let mut stop = false;
    let mut next = map.get(start).unwrap();
    let mut walk: Vec<_> = vec![String::from(start)];
    let mut lp = 1;
    loop {
        for i in instructions.iter() {
            // get next node name
            let name = if *i == 'L' { &next.left } else { &next.right };
            // go to next node
            walk.push(String::from(name));
            // prepare next step
            next = map.get(name).unwrap();
            // check if all paths attained a suitable end
            if &walk.last().unwrap()[2..] == "Z" {
                stop = true;
                break;
            }
        }
        // stop loop if end
        // failsafe on loop numbers
        if stop || lp >= LOOP_LIMIT {
            println!("stops after {lp} loops (/{LOOP_LIMIT})");
            break;
        }
        lp += 1;
    }
    // return path length
    walk.len() - 1
}

fn main() {
    let s = get_input();
    let array: Vec<_> = s.lines().collect();
    let now = Instant::now();
    let instruction_list = array[0].chars().collect();
    let (map, start_list) = parse_map_into_graph(array[2..].to_vec());
    println!("elapsed (parsing to graph): {:?}", now.elapsed());
    let now = Instant::now();
    // day1
    let count = follow(&instruction_list, &map, START);
    println!("elapsed (path followed): {:?}", now.elapsed());
    println!("steps: {count}");
}
