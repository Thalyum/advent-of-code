use std::cmp;
use std::fs;

fn get_input() -> String {
    // let s = String::from(
    //     "1abc2
    // pqr3stu8vwx
    // a1b2c3d4e5f
    // treb7uchet",
    // );
    // let s = fs::read_to_string("input/day1_1").unwrap();
    //     let s = String::from(
    //         "two1nine
    // eightwothree
    // abcone2threexyz
    // xtwone3four
    // 4nineeightseven2
    // zoneight234
    // 7pqrstsixteen",
    //     );
    let s = fs::read_to_string("input/day1_2").unwrap();

    s
}

fn number_from_slice(s: &str) -> Option<i32> {
    match s {
        _ if s.starts_with("one") => Some(1),
        _ if s.starts_with("two") => Some(2),
        _ if s.starts_with("three") => Some(3),
        _ if s.starts_with("four") => Some(4),
        _ if s.starts_with("five") => Some(5),
        _ if s.starts_with("six") => Some(6),
        _ if s.starts_with("seven") => Some(7),
        _ if s.starts_with("eight") => Some(8),
        _ if s.starts_with("nine") => Some(9),
        _ if s.starts_with("1") => Some(1),
        _ if s.starts_with("2") => Some(2),
        _ if s.starts_with("3") => Some(3),
        _ if s.starts_with("4") => Some(4),
        _ if s.starts_with("5") => Some(5),
        _ if s.starts_with("6") => Some(6),
        _ if s.starts_with("7") => Some(7),
        _ if s.starts_with("8") => Some(8),
        _ if s.starts_with("9") => Some(9),
        _ => None,
    }
}

fn number_form_line(s: &str) -> i32 {
    // part 1
    // let a = s.chars().find(|c| c.is_numeric()).unwrap();
    // let b = s.chars().rev().find(|c| c.is_numeric()).unwrap();
    // let number = a.to_string() + &b.to_string();
    // number.parse::<i32>().unwrap()

    // part 2
    let length = s.len();
    let mut a = -1;
    for i in 0..length {
        let max = cmp::min(length, i + 5);
        let subs = &s[i..max];
        if let Some(x) = number_from_slice(subs) {
            a = x;
            break;
        }
    }
    // dbg!(&a);
    let mut b = -1;
    for i in 0..length {
        let r = length - i - 1;
        let max = cmp::min(length, r + 5);
        let subs = &s[r..max];
        if let Some(x) = number_from_slice(subs) {
            b = x;
            break;
        }
    }
    // dbg!(&b);
    a * 10 + b
}

fn main() {
    let s = get_input();
    let o: i32 = s.lines().map(|s| number_form_line(s)).sum();
    println!("{}", o);
}
