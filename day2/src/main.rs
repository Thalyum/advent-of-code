use pest::Parser;
use pest_derive::Parser;
use std::{collections::HashMap, fs};

#[derive(Parser)]
#[grammar_inline = r#"
WHITESPACE = _{ " " }

count = @{ ASCII_DIGIT+ }
color = @{ ASCII_ALPHA+ }

data = { count ~ color }
turn = { data ~ ("," ~ data)* }
id = { "Game" ~ count }
game = { id ~ ":" ~ turn ~ (";" ~ turn)* }

file = { SOI ~ ((game)? ~ NEWLINE)* ~ EOI }
"#]

pub struct GameParser;

const GREEN_LIMIT: i32 = 13;
const RED_LIMIT: i32 = 12;
const BLUE_LIMIT: i32 = 14;

fn get_input() -> String {
    // let s = String::from(
    //     "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    // Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    // Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    // Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    // Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    // ",
    // );
    let s = fs::read_to_string("input/day2_1").unwrap();

    s
}

#[derive(PartialEq, Eq, Hash, Debug)]
enum Colors {
    Blue,
    Red,
    Green,
    None,
}

fn main() {
    let s = get_input();
    let parse = GameParser::parse(Rule::file, &s)
        .expect("unsuccessful parse")
        .next()
        .unwrap();

    let mut parsed: HashMap<i32, Vec<Vec<(Colors, i32)>>> = HashMap::new();

    for line in parse.into_inner() {
        match line.as_rule() {
            Rule::game => {
                let mut inner_rules = line.into_inner(); // { id ~ ":" ~ turn+ }
                let id = inner_rules.next().unwrap(); // { id }

                // get the game number into the { id }
                let game_id = id
                    .into_inner()
                    .next()
                    .unwrap()
                    .as_str()
                    .parse::<i32>()
                    .unwrap(); // { count }

                // collect all { turn }
                let game_turns: Vec<Vec<(Colors, i32)>> = inner_rules
                    // collect all { data }
                    .map(|turn| {
                        turn.into_inner()
                            // collect all { color + count } of the turn
                            .map(|turn_singleton| process_turn_singleton(turn_singleton))
                            .collect()
                    })
                    .collect();

                parsed.insert(game_id, game_turns);
            }
            Rule::EOI => (),
            _ => unreachable!(),
        }
    }

    // part 1
    let invalid = sum_invalid_games(&parsed);
    // sum of valid games = sum of number of games - sum of invalid games
    let o: i32 = parsed.iter().map(|(id, _)| id).sum::<i32>() - invalid;
    println!("part 1: {}", o);
    // part 2
    let power = game_power(&parsed);
    println!("part 2: {}", power);
}

fn process_turn_singleton(s: pest::iterators::Pair<'_, Rule>) -> (Colors, i32) {
    let mut color: Colors = Colors::None;
    let mut count = "";
    for t in s.into_inner() {
        match t.as_rule() {
            Rule::color if t.as_str() == "green" => color = Colors::Green,
            Rule::color if t.as_str() == "blue" => color = Colors::Blue,
            Rule::color if t.as_str() == "red" => color = Colors::Red,
            Rule::count => count = t.as_str(),
            _ => unreachable!(),
        }
    }
    (color, count.parse::<i32>().unwrap())
}

fn sum_invalid_games(games_data: &HashMap<i32, Vec<Vec<(Colors, i32)>>>) -> i32 {
    games_data
        .iter()
        .map(|(&game_id, game_data)| {
            if game_data.iter().any(|turn_data| {
                turn_data.iter().any(|(color, count)| match color {
                    Colors::Blue => count > &BLUE_LIMIT,
                    Colors::Green => count > &GREEN_LIMIT,
                    Colors::Red => count > &RED_LIMIT,
                    _ => unreachable!(),
                })
            }) {
                game_id
            } else {
                0
            }
        })
        .sum()
}

fn game_power(games_data: &HashMap<i32, Vec<Vec<(Colors, i32)>>>) -> i32 {
    games_data
        .iter()
        .map(|(_, game_data)| {
            let f: Vec<&(Colors, i32)> = game_data.into_iter().flatten().collect();
            let mut blue_max = 0;
            let mut green_max = 0;
            let mut red_max = 0;
            f.iter().for_each(|(color, count)| match color {
                Colors::Blue => {
                    if count > &blue_max {
                        blue_max = *count;
                    }
                }
                Colors::Red => {
                    if count > &red_max {
                        red_max = *count;
                    }
                }
                Colors::Green => {
                    if count > &green_max {
                        green_max = *count;
                    }
                }
                _ => unreachable!(),
            });
            blue_max * green_max * red_max
        })
        .sum()
}
