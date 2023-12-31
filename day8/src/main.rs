use std::{cell::RefCell, fs, rc::Rc, time::Instant};

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
struct Graph {
    nodes: Vec<Node>,
}

impl Graph {
    fn new() -> Self {
        Graph { nodes: vec![] }
    }

    fn update(&self, start: &str, left: &str, right: &str) {
        // get start node
        let node = self.get_node(start).unwrap();
        // update left path
        let left = self.get_node(left).unwrap();
        node.update_left(left);
        // update right path
        let right = self.get_node(right).unwrap();
        node.update_right(right);
    }

    fn add(&mut self, name: &str) {
        if let Some(_) = self.get_node(name) {
            panic!("Trying to add node that already exists");
        };

        let node = Node::new(name.to_string());
        self.nodes.push(node);
    }

    fn contains(&self, name: &str) -> bool {
        self.nodes.iter().any(|n| n.0.borrow().name == name)
    }

    fn get_node(&self, name: &str) -> Option<&Node> {
        self.nodes.iter().find(|n| n.0.borrow().name == name)
    }

    fn print_nodes(&self) {
        self.nodes
            .iter()
            .for_each(|n| println!("{}", n.0.borrow().name))
    }

    fn follow(&self, instructions: &Vec<char>, start: &str) -> usize {
        let mut stop = false;
        let mut next = self.get_node(start).unwrap().0.clone();
        let mut walk: Vec<_> = vec![String::from(start)];
        let mut lp = 1;
        loop {
            for i in instructions.iter() {
                // found path end
                if &next.borrow().name[2..] == "Z" {
                    stop = true;
                    break;
                }
                // get next node name
                next = if *i == 'L' {
                    next.borrow().links[0].clone()
                } else {
                    next.borrow().links[1].clone()
                };
                // go to next node
                walk.push(String::from(next.borrow().name.clone()));
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
}

/* https://ricardomartins.cc/2016/06/08/interior-mutability */
type NodeRef = Rc<RefCell<_Node>>;

#[derive(Debug)]
struct _Node {
    name: String,
    links: Vec<NodeRef>,
}

#[derive(Debug)]
struct Node(NodeRef);

impl Node {
    fn new(name: String) -> Self {
        let node = _Node {
            name,
            links: Vec::with_capacity(2),
        };
        Node(Rc::new(RefCell::new(node)))
    }

    fn update_left(&self, left: &Self) {
        assert_eq!(self.0.borrow().links.len(), 0);
        (self.0.borrow_mut()).links.push(left.0.clone());
    }

    fn update_right(&self, right: &Self) {
        assert_eq!(self.0.borrow().links.len(), 1);
        (self.0.borrow_mut()).links.push(right.0.clone());
    }
}

struct Parsed(String, String, String);

fn parse_input(map: Vec<&str>) -> Vec<Parsed> {
    let mut node_list = Vec::new();
    for l in map {
        let (origin, paths) = l.split_once('=').unwrap();
        let (left, right) = paths.split_once(',').unwrap();
        let trim_pattern: &[_] = &['(', ')', ' '];
        let origin = origin.trim_matches(trim_pattern).to_owned();
        let left = left.trim_matches(trim_pattern).to_owned();
        let right = right.trim_matches(trim_pattern).to_owned();

        node_list.push(Parsed(origin, left, right));
    }
    node_list
}

fn get_starts(nodes: &Vec<Parsed>) -> Vec<String> {
    nodes
        .iter()
        .filter(|p| &p.0[2..] == "A")
        .map(|p| p.0.clone())
        .collect()
}

fn main() {
    let s = get_input();
    let array: Vec<_> = s.lines().collect();
    let g_now = Instant::now();
    let instructions = array[0].chars().collect();
    let parsed = parse_input(array[2..].to_vec());
    // get all starting points
    let start_list = get_starts(&parsed);
    // create all graph nodes
    let mut graph = Graph::new();
    for p in parsed.iter() {
        graph.add(&p.0);
    }
    // update all links
    for p in parsed.iter() {
        graph.update(&p.0, &p.1, &p.2);
    }
    // day1
    let now = Instant::now();
    let count = graph.follow(&instructions, START);
    println!("elapsed (path followed): {:?}", now.elapsed());
    println!("(day 1) steps: {count}");
    // day 2
    for start in start_list {
        println!("===\nFollowing path from {start}");
        let now = Instant::now();
        let count = graph.follow(&instructions, start.as_str());
        println!("elapsed (path followed): {:?}", now.elapsed());
        println!("steps: {count}");
    }
    println!("\nelapsed (end): {:?}", g_now.elapsed());
}
