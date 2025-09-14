---
title: "Guess"
format: html
---

## Announcements

- Lab Day
    - Mixed use assignment.
    - Practically useful for HW
    - Theoretically useful for Final

## Homework

- "Macros" is ready.
  - Not too hard; just practice with the operators.
- Due Friday, 26 Sept. at 1440 ET.

## Citation

- I learned the term *Hamming distance* from Prof. Josh Laison while discussing a possible research collaboration.

## Today

- [ ] Hamming
- [ ] Hamming weight
- [ ] Hamming distance


# Hamming

## The person

> [Hamming initially wanted to study engineering, but money was scarce during the Great Depression, and the only scholarship offer he received came from the University of Chicago, which had no engineering school. Instead, he became a science student, majoring in mathematics,[5] and received his Bachelor of Science degree in 1937.](https://en.wikipedia.org/wiki/Richard_Hamming)

![](https://i.kym-cdn.com/photos/images/newsfeed/002/519/734/df4)

## Fine print

- It is a virtual certainty that Hamming did not discover the concepts of Hamming weight or Hamming distance, both of which have limited use in historical record before Hamming was alive.
- Typically I avoid using terms where someone is named after someone who did not invent it.
- I don't have alternate name in this case.
    - It can be called "edit distance" but there are other edit distances.
- It must be remarked upon that an abstract mathematical concept was named after a US Ivy Leaguer who worked on the Manhattan Project, and that this naming is highly political.

# Weight

## Definition

> The Hamming weight of a string is the number of symbols that are different from the zero-symbol of the alphabet used.

- This adopts the formal computer science notion of referring to bit strings as:
    - *words* in the 
    - *languages*, which is the set of all possible bitstrings
    - that is composed of the *symbols*, which are the bit values $\{0, 1\}$
- So, Hamming weight of a byte is the number of `1`s in that byte.

## Your task

- Using the bitwise operators, shifts, and addition, write the following functions:
```rs
fn weight_u8(byte:u8) -> u64
fn weight_u64(word:u64) -> u64
fn weight_bytes(bytes:Vec<u8>) -> u64
fn weight_words(words:Vec<u64>) -> u64
```

- You may wish to follow the Rust convention of implementing these in a `src/lib.rs` file.
    - You will need to prefix them as `pub fn` in `src/lib.rs`
    - You will need to prefix them with your package name and `::` in `src/main.rs`
        - I used `hamming::weight_u8`, for example.
- This convention will be required for the homework, but is not required now.

## Template files

- I made a package:
```sh
cargo new 31 --name hamming --vcs none
```
- I wrote a library function:
```{.rs filename="src/lib.rs")
pub fn weight_u8(byte:u8) -> u64 {
    let mut cnt : u64 = 0;
    // This is wrong.
    cnt += 1;
    // That was wrong.
    return cnt;

```
- I wrote some tests:
```{.rs filename="src/main.rs")
fn main() {
    dbg!(hamming::weight_u8(0x33_u8));
}
```
- After fixing my function, I saw the following:
```sh
$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/hamming`
[src/main.rs:2:5] hamming::weight_u8(0x33_u8) = 4
```

# Distance

## Definition

> In information theory, the Hamming distance between two strings or vectors of equal length is the number of positions at which the corresponding symbols are different.

- The Hamming weight is the Hamming distance from the string of all `0` symbols.

## Your task

- Using the bitwise operators, shifts, and addition, write the following functions:
```rs
fn distance_u8(b:u8, c:u8) -> u64
fn distance_u64(w:u64, x:u64) -> u64
fn distance_bytes(bs:Vec<u8>, cs:Vec<u8>) -> u64
fn distance_words(ws:Vec<u64>, xs:Vec<u64>) -> u64
```

- You may change the parameter names if those don't make sense to you.
    - They were procedurally generated.

## Today

- [x] Hamming
- [x] Hamming weight
- [x] Hamming distance

# Challenge Problems

## Strings as bitstrings

- Compute the Hamming distance between the strings `Willamette` and `Xjmmbnfuuf`.
- Successfully pronounce `Xjmmbnfuuf`

## POPCNT

- Read [this paper](https://arxiv.org/pdf/1611.07612)