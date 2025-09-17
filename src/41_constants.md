---
title: "Constants"
format: html
---

## Announcements

- Enrichment assignment
    - Use case/limitation of IEEE 754 floating point values
    - Use case of binary search
    - Use case of pre-compute.

## Homework

- SHA beckons
- Due Friday, 10 Oct. at 1440 ET.
    - Expect it to take you both weeks.
    - Do not work on this instead of that, after lab section today, until you are done with that.

## Citation

- I checked my work vs. this implementation, in C++, of which I have not verified complete correctness.
- [RadeelAhmad](https://github.com/RadeelAhmad/SHA-512/blob/main/code.cpp)

## Today

- [ ] Floating point
- [ ] Binary search
- [ ] Pre-compute

# Background

## The Constants

> [first <s>32</s>64 bits of the fractional parts of the square roots of the first 8 primes 2..19](https://en.wikipedia.org/wiki/SHA-2)

- Wait how do we calculate that?

### Floats and Square Roots

- There is square root in Rust... kinda.
- [f64::sqrt](https://doc.rust-lang.org/std/primitive.f64.html#method.sqrt)
- We recall the rules on floating point:

> [Kernel code is normally prohibited from using floating-point (FP) registers or instructions, including the C float and double data types.](https://docs.kernel.org/core-api/floating-point.html)

### The Values

$$
\begin{align*}
\begin{split}
   H_0^{(0)} = \texttt{0x6a09e667f3bcc908}, \quad H_1^{(0)} = \texttt{0xbb67ae8584caa73b},\\
   H_2^{(0)} = \texttt{0x3c6ef372fe94f82}, \quad H_3^{(0)} = \texttt{0xa54ff53a5f1d36f1},\\
   H_4^{(0)} = \texttt{0xa54ff53a5f1d36f1}, \quad H_5^{(0)} = \texttt{0x9b05688c2b3e6c1f},\\
   H_6^{(0)} = \texttt{0x1f83d9abfb41bd6b}, \quad H_7^{(0)} = \texttt{0x5be0cd19137e2179}.
\end{split}
\end{align*}
$$

- Perhaps this works?

### First $n$ primes

- Primes are annoying, mostly because 2 exists.
- I did the following:
```rs
fn main() {
    for i in [2,3,5,7,11] {
        println!("{i}");
    }
    let mut cnt = 5;
    let mut val = 13;
    while cnt < 8 {
        if is_prime(val) {
            println!("{val}");
            cnt += 1;
        }
        val += 2;
    }
}
```

# Exercise 0

- Write `is_prime`
- The above `main` should produce the following:
```email
2
3
5
7
11
13
17
19
```

## Square roots

- We can naively attempt to calculate round constants with `f64::sqrt`
```rs
dbg!(f64::sqrt(x as f64));
```
- You'd see something like the following:
```email
sqrt(2.0) = 1.4142135623730951
sqrt(3.0) = 1.7320508075688772
sqrt(5.0) = 2.23606797749979
sqrt(7.0) = 2.6457513110645907
sqrt(11.0) = 3.3166247903554
sqrt(13.0) = 3.605551275463989
sqrt(17.0) = 4.123105625617661
sqrt(19.0) = 4.358898943540674
```
- We should note that is pretty far from the constants!

### Fractional components

- Compute only the fractional components of the roots:
    - The square root of $2$ is approximately $1.414...$
    - The fractional component is $.414...$
    - To express this value in 64 bits, I can multiple by $2 ^ 64$
    - To view it as represented in the constants, I can represent the value in hexadecimal.
    
# Exercise 1

- Approximate the fractional components using `f64::sqrt`
```email
sqrt(02) = 1.41421356 -> 6a09e667f3bcd000
sqrt(03) = 1.73205081 -> bb67ae8584caa000
sqrt(05) = 2.23606798 -> 3c6ef372fe950000
sqrt(07) = 2.64575131 -> a54ff53a5f1d4000
sqrt(11) = 3.31662479 -> 510e527fade68000
sqrt(13) = 3.60555128 -> 9b05688c2b3e6000
sqrt(17) = 4.12310563 -> 1f83d9abfb41c000
sqrt(19) = 4.35889894 -> 5be0cd19137e4000
```
- We should note that these are quite wrong.

## Floating points

- Basically, a `f64` can only store 64 bits of information.
- This means it cannot store 64 bits worth of fractional information and also a whole number, as it must be able to do.
- This leads to a loss of precision well before calculating 64 bits worth of precision.
- In practice, they are implemented something like [this](https://en.wikipedia.org/wiki/Floating-point_arithmetic):
<center>
<br>
<img style="filter:invert(1)" src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Float_example.svg/590px-Float_example.svg.png">
</center>
- This is obviously terrible 

## Today

- [x] Floating point
- [ ] Binary search
- [ ] Pre-compute

## A Plan

- That said, we can...
    - Find the `f64` approximation of the root.
    - Convert back to an integer type[^1]
    - Compute the square.
- Let's see what this may looks like.
```email
sqrt(02) = 1.41421356 -> 16a09e666 ^ 2 = 01fffffffa7a8770a4
sqrt(03) = 1.73205081 -> 1bb67ae83 ^ 2 = 02fffffff746605709
sqrt(05) = 2.23606798 -> 23c6ef370 ^ 2 = 04fffffff29bbdd100
sqrt(07) = 2.64575131 -> 2a54ff537 ^ 2 = 06ffffffee28d451d1
sqrt(11) = 3.31662479 -> 3510e527c ^ 2 = 0affffffe79823ac10
sqrt(13) = 3.60555128 -> 39b056888 ^ 2 = 0cffffffe1effec840
sqrt(17) = 4.12310563 -> 41f83d9a7 ^ 2 = 10ffffffd6ebf68af1
sqrt(19) = 4.35889894 -> 45be0cd14 ^ 2 = 12ffffffd3bf490990
```
- An astute student will notice the following:
    - I am printing precisely 18 hex digits for the square.
    - The lower 64 digits are very close to the maximal value.
    - The upper 2 digits are the hexadecimal representation of the prime, less one.
- So we have slightly underestimated, at least in this case.
    - I will note I can converting back to integers with 32 bits of precision then squaring with 128 bits of precision.
    - The 32 bits clip values to ensure an undercount.
    - The 128 bits ensure we do not overflow when squaring the 32 bit value.
- From there, we can conduct a binary search.
    - Find the highest non-one value in the candidate square root.
    - Set it to one.
    - Check for overflow:
        - If so, revert to zero.
        - If not, leave as one.
    - Loop.

# Exercise 3

- Compute the 64 bit contants using binary search.

## Today

- [x] Floating point
- [x] Binary search
- [ ] Pre-compute

## Precompute

- I hope it suffices to say, there is no obvious reason any application *using* these values need compute them.
- This is the usefulness of precomputing constant values - or, perhaps, of numerical computing.

## Today

- [x] Floating point
- [x] Binary search
- [x] Pre-compute

# Challenge Problems

- SHA-512 also uses *round contants*

> first <s>32</s>64 bits of the fractional parts of the cube roots of the first <s>64</s>80 primes

- Compute the SHA-512 round constants.
