use std::fs;

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
    print!("part 1: {}", sum);
}
