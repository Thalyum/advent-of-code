use std::{fs, time::Instant};

fn get_input() -> String {
    //     let s = String::from(
    //         "467..114..
    // ...*......
    // ..35..633.
    // ......#...
    // 617*......
    // .....+.58.
    // ..592.....
    // ......755.
    // ...$.*....
    // .664.598..",
    //     );
    let s = fs::read_to_string("input/day3_1").unwrap();

    s
}

fn main() {
    let s = get_input();
    let array: Vec<Vec<_>> = s.lines().map(|l| l.chars().collect()).collect();
    let height = array.len() as i32;
    let width = array[0].len() as i32;
    let now = Instant::now();
    part_one(&array, height, width);
    println!("elapsed: {:?}", now.elapsed());
    let now = Instant::now();
    part_one_2(&array, height, width);
    println!("elapsed: {:?}", now.elapsed());
}

fn part_one_2(array: &Vec<Vec<char>>, height: i32, width: i32) {
    let mut grid = array.clone();
    // detect numbers close to a symbol, and paint them red in a grid
    let mut mul = 0;
    for i in 0..height {
        for j in 0..width {
            // find symbols
            if !grid[i as usize][j as usize].is_numeric() && grid[i as usize][j as usize] != '.' {
                let gear = if grid[i as usize][j as usize] == '*' {
                    true
                } else {
                    false
                };
                let mut gear_count = 0;
                let mut gear_list = [(-1, -1); 2];
                // check in all direction, even diagonally
                for (ni, nj) in [
                    (i - 1, j - 1),
                    (i - 1, j),
                    (i - 1, j + 1),
                    (i, j - 1),
                    (i, j + 1),
                    (i + 1, j - 1),
                    (i + 1, j),
                    (i + 1, j + 1),
                ] {
                    if (0 <= ni) && (ni < height) && (0 <= nj) && (nj < width) {
                        if grid[ni as usize][nj as usize].is_numeric() {
                            if gear {
                                if gear_count < 2 {
                                    let mut next = 1;
                                    while nj - next >= 0
                                        && grid[ni as usize][(nj - next) as usize].is_numeric()
                                    {
                                        grid[ni as usize][(nj - next) as usize] = 'X';
                                        next += 1;
                                    }
                                    let index = (ni, nj - next + 1);
                                    if !gear_list.contains(&index) {
                                        gear_list[gear_count] = index;
                                    }
                                }
                                gear_count += 1;
                            }
                            // paint number red: found digit + rest of the number on the same line
                            grid[ni as usize][nj as usize] = 'X';
                            // paint downstream
                            let mut next = 1;
                            while nj + next < width
                                && grid[ni as usize][(nj + next) as usize].is_numeric()
                            {
                                grid[ni as usize][(nj + next) as usize] = 'X';
                                next += 1;
                            }
                            // paint upstream
                            next = 1;
                            while nj - next >= 0
                                && grid[ni as usize][(nj - next) as usize].is_numeric()
                            {
                                grid[ni as usize][(nj - next) as usize] = 'X';
                                next += 1;
                            }
                        }
                    }
                }
                if gear && gear_count == 2 {
                    let gear1 = array[gear_list[0].0 as usize]
                        .iter()
                        .skip(gear_list[0].1 as usize)
                        .take_while(|s| s.is_numeric())
                        .collect::<String>()
                        .parse::<i32>()
                        .unwrap();
                    let gear2 = array[gear_list[1].0 as usize]
                        .iter()
                        .skip(gear_list[1].1 as usize)
                        .take_while(|s| s.is_numeric())
                        .collect::<String>()
                        .parse::<i32>()
                        .unwrap();
                    mul += gear1 * gear2;
                }
            }
        }
    }
    // walk the grid and keep numbers that has been painted red
    let mut skip = 0;
    let mut sum = 0;
    for i in 0..height {
        for j in 0..width {
            // do not process the same number more than once
            if skip > 0 {
                skip -= 1;
                continue;
            }
            // if not a number, go to next index
            if !array[i as usize][j as usize].is_numeric() {
                continue;
            }
            // extract the whole number from the line (starting at offset)
            let num: Vec<_> = array[i as usize]
                .iter()
                .skip(j as usize)
                .take_while(|c| c.is_numeric())
                .collect();
            let num_len = num.len();
            // check if first digit has been painted 'red'
            if grid[i as usize][j as usize] == 'X' {
                // we got one to keep !
                // parse the number and sum it
                let x = num.into_iter().collect::<String>().parse::<i64>().unwrap();
                sum += x;
            }
            skip = num_len - 1;
        }
    }
    println!("part 1 (v2): {}", sum);
    println!("part 2 (v2): {}", mul);
}

fn part_one(array: &Vec<Vec<char>>, height: i32, width: i32) {
    let mut grid = array.clone();
    // detect numbers close to a symbol, and paint them red in a grid
    for i in 0..height as i32 {
        for j in 0..width as i32 {
            if array[i as usize][j as usize].is_numeric() {
                // check in all direction, even diagonally
                for (ni, nj) in [
                    (i - 1, j - 1),
                    (i - 1, j),
                    (i - 1, j + 1),
                    (i, j - 1),
                    (i, j + 1),
                    (i + 1, j - 1),
                    (i + 1, j),
                    (i + 1, j + 1),
                ] {
                    if (0 <= ni) && (ni < height) && (0 <= nj) && (nj < width) {
                        if !array[ni as usize][nj as usize].is_numeric()
                            && array[ni as usize][nj as usize] != '.'
                        {
                            // paint number red
                            grid[i as usize][j as usize] = 'X';
                            break;
                        }
                    }
                }
            }
        }
    }
    // walk the grid and keep numbers where at least one digit has been painted red
    let mut skip = 0;
    let mut sum = 0;
    for i in 0..height {
        for j in 0..width {
            // do not process the same number more than once
            if skip > 0 {
                skip -= 1;
                continue;
            }
            // extract the whole number from the line (starting at offset)
            let num: Vec<_> = array[i as usize]
                .iter()
                .skip(j as usize)
                .take_while(|c| c.is_numeric())
                .collect();
            let num_len = num.len();
            // if not a number, go to next index
            if num_len == 0 {
                continue;
            }
            // check if any digit has been painted red
            if grid[i as usize]
                .iter()
                .skip(j as usize)
                .take(num_len)
                .any(|&c| c == 'X')
            {
                // we got one to keep !
                // parse the number and sum it
                let x = num.into_iter().collect::<String>().parse::<i64>().unwrap();
                sum += x;
            }
            skip = num_len - 1;
        }
    }
    println!("part 1: {}", sum);
}
