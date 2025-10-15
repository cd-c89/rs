---
title: "Numbers"
---

# Announcements

- **Welcome** to Systems in Rust
- **Action Items**:
  - Midterms verbal update.
  - Next assignment goes out Friday, start whenever.
  - This lecture supports that homework.


## Today

- Finite sets, rings
- Arbitrary/high precision integers
- Arithmetic operations
- Function types
  
# Finite sets, rings
  
## Apocryphal Quote

- I cannot find it, but I believe a philosopher one jested:

> I am a weapons-grade finitist. I don't believe in numbers larger than two.

- Arrays of such numbers are sufficient for computation of arbitrary precision.
- We can not capture the infinite, but we may model it.
  
## What are integers?

- Denote integers as the mathematical symbol $\mathbb{Z}$
  - Something to do with the German/Deutsch
- Not particular useful in cryptography, actually
  - We tend to want the naturals, denoted $\mathbb{N}$
  - Counting numbers, $0$ and up.

## In Python

- We can write them in Python with `itertools`

```{.python filename="fields.py"}
from itertools import count
N = count()
make_z = lambda n : n // 2 if n % 2 else -n // 2
Z = (make_z(n) for n in count(1))
# We can see elements of these infinite collections with
[next(N) for _ in range(5)], [next(Z) for _ in range(5)]
```

- What do you see?
```python
([0, 1, 2, 3, 4], [0, -1, 1, -2, 2])
```

## Aside

- It is moderately controversial to assert:
$$
0 \in \mathbb{N}
$$
  - Enderton, Herbert B. (1977). Elements of set theory. New York: Academic Press. p. 66. ISBN 0122384407.
- Fortunately this is a CS class.
```python
assert(0 in count())
```

## $\mathbb{N}$ is akin to `u`$n$

- The natural numbers $\mathbb{N}$ probably look a lot like the unsigned integers.
- There's only one real problem.
  - Get it, $\mathbb{R}$EAL problem.  
- We don't have the unsigned integers in Rust.
  - We don't have them in Python either, but for a different reason.

## The Problem

- Python has been lying to us for years that its set of integers has no upper bound.
  - We say $\nexists n : n \notin$ `count()`
  - Let's just try a reasonably sized number, say googolplex $= 10^{10^{100}}$

## Test with `-c`

- We use the `-c` flag to Python to run a script directly at command line.
```python
python3 -c "print('hello world')"
```
- Perform multi-line calculuations using `;`
  - Oh - like Rust. 🤔

```python
python3 -c "from itertools import count; print(0 in count())"
```

## Time it

```sh
$ time python3 -c "from itertools import count; print(0 in count())"
True

real    0m0.013s
user    0m0.014s
sys     0m0.000s
```

- We could argue it takes .013 seconds to check
- Or .013 seconds to find itertools on a SDD

## Bigger Numbers

- Check e.g. 1000
```sh
$ time python3 -c "from itertools import count; print(1000 in count())"
True

real    0m0.012s
user    0m0.012s
sys     0m0.000s
```

- Trivial.

## Test it

- Try a few powers yourself. What do you find?

```email
time python3 -c "from itertools import count; n=1; print(10**n in count())"
```

##

::::{.columns}

:::{.column width="%50"}

|10^$n$|`real`|
|-|-|
|1|00.012|
|2|00.012|
|3|00.012|
|4|00.013|
|5|00.013|
|6|00.027|
|7|00.164|
|8|01.498|
|9|16.810|

:::


:::{.column width="%50"}

- Expect:
$$
t(10^{10}) \in [140,170]
$$
- Expect for $n \gt 9$
$$
t(10^n) \in [14,17] \times 10^{n-9}
$$
- Expect $10^{10^{100}}$ in
  - $10^{10^{91}}$ seconds
  - 316 novemvigintilion years

:::

::::

## Rust

- Rust is a little more forthright about how big its numbers get.
```{.rs}
pub const MAX: i32 = i32::MAX; // 2_147_483_647i32
```
- [Read more, or don't. I'm a hyperlink; not an imperative.](https://doc.rust-lang.org/std/i32/constant.MAX.html)

## Quoth Rust Book

> Let’s say you have a variable of type u8 that can hold values between 0 and 255. If you try to change the variable to a value outside that range, such as 256, integer overflow will occur, which can result in one of two behaviors. When you’re compiling in debug mode, Rust includes checks for integer overflow that cause your program to panic at runtime if this behavior occurs. Rust uses the term panicking when a program exits with an error...

## Quoth Rust Book

> When you’re compiling in release mode with the --release flag, Rust does not include checks for integer overflow that cause panics. Instead, if overflow occurs, Rust performs two’s complement wrapping. In short, values greater than the maximum value the type can hold “wrap around” to the minimum of the values the type can hold. In the case of a u8, the value 256 becomes 0, the value 257 becomes 1, and so on. The program won’t panic, but the variable will have a value that probably isn’t what you were expecting it to have. Relying on integer overflow’s wrapping behavior is considered an error.

## Quoth Rust Book

> The program won’t panic, but the variable will have a value that probably isn’t what you were expecting it to have. Relying on integer overflow’s wrapping behavior is considered an error.

> To explicitly handle the possibility of overflow, you can use these families of methods provided by the standard library for primitive numeric types:

## Methods in Rust

- Wrap in all modes with the `wrapping_*` methods, such as `wrapping_add`.
- Return the None value if there is overflow with the `checked_*` methods.
- Return the value and a Boolean indicating whether there was overflow with the `overflowing_*` methods.
- Saturate at the value’s minimum or maximum values with the `saturating_*` methods.

## Editorializing

- I find having different numerical behavior in debug and release versions *extremely* questionable.
- I was willing to bite my tongue but in fact:
    - This is impacts SHA-2, upcoming ECDSA, `f16` and `ix`
    - Using stable numerical behavior facilitated debatably easier implementations in C last term.
    
## Demo in Rust

- We don't have to just trust in the given `i32` upper bound, we can test it.
- Well, kinda...
```{.rs filename="src/main.rs"}
fn main() {
    let mut n: i32 = 0;
    while (n + 1) > n {
        n += 1;
    }
    dbg!(n);
    dbg!(i32::MAX);
}
```

## Testing...

- Let's time how long this takes!
    - We timed Python.
- Go ahead and `time cargo run`
```sh
   Compiling num v0.1.0 (/home/user/tmp/num)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.25s
     Running `target/debug/num`

thread 'main' panicked at src/main.rs:3:11:
attempt to add with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

real    0m4.943s
user    0m4.914s
sys     0m0.079s
```

## Discuss

- For me, this took 4.66s on `i32`
  - Same value in Python was 1m9.32s
    - This is about half the speed I got with C.
- How long for  `u64`?
  - In Python?
- How would speed up the code?
  - What assumptions did you make?
- How many base 10 digits does the largest number we can store in 32 bytes have?

## Testing...

- Rust behaves differently with the `--release` flag.
    - Just me: I hate this!
- `time cargo run --release`
```sh
   Compiling num v0.1.0 (/home/user/tmp/num)
    Finished `release` profile [optimized] target(s) in 0.54s
     Running `target/release/num`
[src/main.rs:6:5] n = 2147483647
[src/main.rs:7:5] i32::MAX = 2147483647

real    0m0.578s
user    0m0.086s
sys     0m0.116s
```


## Rings

- As far as I know (not a mathematician) the `u`$n$s and `i`$n$'s in Rust are *rings*
  - They have addition and multiplication
- They aren't fields - zero is divisible
  - Spoiler alert, but $2^{\frac{n}{2}} \times 2^{\frac{n}{2}} \equiv 0 \pmod{2^n}$

## Rings vs Integers

- Rings have some "goofy" features
  - $a, b \in$ `u`$n$ $\nRightarrow a + b > a$
  - Same with multiplication.
- Let's look at an example.

## Checkers

```{.rs filename="src/main.rs"}
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let a:u8 = args[1].parse().unwrap();
    let b:u8 = args[2].parse().unwrap();
    dbg!(a + b);
}
```

## Do some additions

```sh
$ cargo run -- 10 20
   Compiling num v0.1.0 (/home/user/tmp/num)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/num 10 20`
[src/main.rs:5:5] a + b = 30
```
- `30` - that makes sense!


## Do some additions

```sh
$ cargo run -- 100 200
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/num 100 200`

thread 'main' panicked at src/main.rs:5:10:
attempt to add with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```
- Overflow - sure, $100 + 200 = 300 > 2^8 = 256$

## Do some additions

```sh
$ cargo run --release -- 100 200
   Compiling num v0.1.0 (/home/user/tmp/num)
    Finished `release` profile [optimized] target(s) in 0.25s
     Running `target/release/num 100 200`
[src/main.rs:5:5] a + b = 44
```
- `44`? From Whence?

$$
100 + 200 \equiv 44 \pmod{2^8}
$$
- Or perhaps
```sh
python3 -c "print((100 + 200) % (2 ** 8) == 44)"
```

## Rust integers are *finite*

```email
>>> 200 + 100
300
>>> 2 ** 8
256
>>> 300 - 256
44
>>> 300 % 256
44
```

- Equivalent to operations on the naturals modulo $2^8$
- Usually denoted as:
$$
\mathbb{Z}/2^8\mathbb{Z}
$$
- We say $\mathbb{Z}$ not $\mathbb{N}$ as $-1 \in \mathbb{Z}/n\mathbb{Z}$

## In practice

- $\exists$ `i32::MAX`, `u64::MAX`, etc.
- Sums and products less than these values are unaffected.
- Sums and products greater than these values are unstable.
- Use methods or compile for release.

## Problem Statement

- Quoth GitHub

> [`ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

- Wait a minute. 
- What does that 4096 stand for?
  - For what does that 4096 stand?

## $n > 128$ bits

- Modern security recommendations are for 4096 bit cryptographic keys.
  - 2048 is generally considered "okay" or "acceptable"

```email
NAME
     ssh-keygen — OpenSSH authentication key utility

SYNOPSIS
     ssh-keygen [-q] [-a rounds] [-b bits] 
```

# Today

- &check; Finite sets, rings
- Arbitrary/high precision integers
- Arithmetic operations
- Function types

## Big Values

- Soon, we will implement key generation.
  - We'll talk about what it is then.
- First, we need a way to deal with integers that big.
- We will use *modular arithmetic*.
  - Finite `u64` models infinite $\mathbb{Z}$

## Simple Example

- Yoink a data science example.
- We had a data set for which we determined a mean height in inches.
- We converted it to inches and feet.
```python
>>> 69.3 // 12, 69.3 % 12
(5.0, 9.299999999999997)
```
- Floats: they're bad.

## Addition is easy

- WNBA MVP and Olympic Gold Medalist A'ja Wilson is [6 ft 4 in](https://en.wikipedia.org/wiki/A%27ja_Wilson)
- How much taller is that than 5 ft 9.3 in
  - Can convert to non-integer inches, but...
  - We already had the .299... problem

## Difference

- We perform "long subtraction"
- It's fun!

| |ft|in.|.in|
|-|--|---|---|
|A'ja|6|4|0|
|Mean|5|9|3|

## Difference

- $0 - 3 \equiv 7 \pmod{10}$
- Tenths of inches

| |ft|in.|.in|
|-|--|---|---|
|A'ja|6|4|0|
|Mean|5|9|3|
|Diff| | |7|

## Difference

- But wait - `3` is more than `0`
- Track via a "carry"

| |ft|in.|.in|
|-|--|---|---|
|A'ja|6|4|0|
|Mean|5|9|3|
|Carry|0|1|0|
|Diff| | |7|

## Difference

- $4 - 9 - 1 \equiv 6 \pmod{12}$
- 12 in = 1 ft

| |ft|in.|.in|
|-|--|---|---|
|A'ja|6|4|0|
|Mean|5|9|3|
|Carry|0|1|0|
|Diff| |6|7|


## Difference

- Another carry.
- 12 in = 1 ft

| |ft|in.|.in|
|-|--|---|---|
|A'ja|6|4|0|
|Mean|5|9|3|
|Carry|1|0|0|
|Diff| |6|7|


## Difference

- $6 - 5 - 1 = 0$
- Nonmodular - feet has no max.

| |ft|in.|.in|
|-|--|---|---|
|A'ja|6|4|0|
|Mean|5|9|3|
|Carry|1|0|0|
|Diff|0|6|7|

## Conclusion

- Iconic living legend A'ja Wilson is tall af.
- We can do addition and substraction on larger values than `u64::MAX` by:
  - Breaking numbers in smaller ranges
    - A tenths digit
    - A ones digit
    - A twelves digit

## Usefulness

- We can now do arithmetic correctly
  - @Python
- What else can we do?
  - Arbitrary (not infinite) precision.

## FAQ

- Can we use this to add numbers bigger than $2^n$ using adds over at most $n$ bits at a time?
  - Sure! Change the modulos and you're set.
    - Get it? Because the numbers form a set?
- Can we do this for more than 3 units?
  - Sure! Just put the middle (both consumes and produces a carry bit) in a loop!

# Today

- &check; Finite sets, rings
- &check; Arbitrary/high precision integers
- Arithmetic operations
- Function types

## Easy Mode

- Addition and subtraction are easy.
- For some value of easy.
  - Cut a too-big number into chunks.
  - Add or subtract within chunks of the same index/offset/significance.
  - Only wrinkle is a carry bit.
- Identical to digit-based addition.
  - `u8`s as digits in base 256 arithmetic

## Hard Mode

- Some cryptographical algorithms, however, use two extremely advanced arithmetic operations:
  - Multiplication, and
  - Division, and
  - Modulo
- Fortunately this only two operations (need a combined `divmod`)

## Example

- Last term I taught:
  - 14 MS-level Computer Scientists
    - 9-12 hrs/wk
    - 14 week contract
  - 34 BS-level Computer Scientists
    - 6-9 hrs/wk
    - 15.5 week contract
- How many person hours is this?

## Napkin Math

- I'd say
  - $14 \times 12 \times 14$
  - $34 \times 9 \times 15.5$
- I... can't quite do that in one fell swoop.
  - $14 \times 12$ is trivially $12^2 + 24 = 168$
  - $9 \times 15.5$ is trivially $155 - 15.5 = 139.5$

## $34 \times 139.5$

- That just isn't easy 
 - (140 * 34 isn't bad, but we need a motivating example). 
- Express *digit-wise*:

| |1|3|9|5|
|-|-|-|-|-|
|3|-|-|-|-|
|4|-|-|-|-|

## $34 \times 139.5$

- Compute all products over single-digit factors

| |1|3|9|5|
|-|-|-|-|-|
|3|3|9|27|15|
|4|4|12|36|20|

- These:
  - Aren't single digit
  - Aren't of the same signficance

## $34 \times 139.5$

- Include sigificance

| |100|30|9|.5|
|-|-|-|-|-|
|30|3000|900|270|15|
|4|400|120|36|2|

## Dear Watson


::::{.columns}

:::{.column width="%50"}


| |100|30|9|.5|
|-|-|-|-|-|
|30|3000|900|270|15|
|4|400|120|36|2|


:::


:::{.column width="%50"}

$$
\begin{align*}
5& \times 4  \times 10^{-1}  &= 2&\\
+5& \times 3  \times 10^{0}  &= 15&\\
+9& \times 4  \times 10^{0}  &= 36&\\
+9& \times 3  \times 10^{1}  &= 270&\\
+3& \times 4  \times 10^{1}  &= 120&\\
+3& \times 3  \times 10^{2}  &= 900&\\
+1& \times 4  \times 10^{2}  &= 400&\\
+1& \times 3  \times 10^{3}  &= 3000&\\
\end{align*}
$$

:::

::::

## Express as

$$
\begin{align*}
139.5& = &1 * 10^2 + &3 * 10^1 + &9 * 10^0& + 5 * 10^{-1}\\
34& = &&3 * 10^1 + &4 * 10^0&\\
\end{align*}
$$

- Take $x = 10$
$$
\begin{align*}
139.5& = &1 * x^2 + &3 * x + &9& + 5 * x^{-1}\\
34& = &&3 * x + &4&\\
\end{align*}
$$

- That is polynomial; can work with those.

## Polynomial

$$
(x^2 + 3x + 9 + 5x^{-1})(3x + 4)
$$

$$
(x^2 + 3x + 9 + 5x^{-1})(3x) + (x^2 + 3x + 9 + 5x^{-1})(4)
$$


$$
(3x^3 + 9x^2 + 27x + 15) + (4x^2 + 12x + 36 + 20x^{-1})
$$

$$
3x^3 + 13x^2 + 39x + 51 + 20x^{-1}
$$

## Aside

- I think this is covered around ~8th grade
- I don't want to assume the integrity to US public school system
  - Or anything school system
  - Shout out school
- The point of this class isn't middle/high school math
  - That's the point of life itself /s

## Considerations

- It is natural to express multiplication of e.g. 4096 bit integers as a polynomial over, say, 64 bit integers.
- One teeny problem:
  - Overflow.

## Overflow

- The point of calculating this was to get things down to single digit:

$$
3x^3 + 13x^2 + 39x + 51x^0 + 20x^{-1}
$$

- 13, 39, 51, and 20 are all not compliant (debatably 20 is okay)
- Essentially, 1-digit multiply may produce a 2-digit product.


## Size of ints

- Say we have two integers of 8 bits of precision.
- We multiple them together.
- What is the largest number we can get, and
- How many bits does it require?
```{.email}
python3 -c "x = 2 ** 8 - 1 ; x = x * x ; print(x.bit_length())"
```
- 16

# Carrys for mults

- When we are doing big multiplications:
  - We must multiply chunks of at most half the size of our biggest integer.
  - We must keep track of significance - their position in an imagined larger integer
  - We must perform adds over these terms, using big addition

## Division

- Remember long division?
  - Align the highest digits (I took the log base 2)
  - Divide.
  - Keep track of significance (Difference between logs)
  - Calculate remainder.
  - Loop.
- The final remainder is the mod.

## Today

- &check; Finite sets, rings
- &check; Arbitrary/high precision integers
- &check; Arithmetic operations
- Function types

## An arbitrary precision type.

- Just as with `f16`, we can create something to hold numbers.
  - I used a boolean for signs and a vector for digits.
- Here's an example function declaration:
```{.rs filename="src/lib.rs"}
// At the top
#![allow(non_camel_case_types)]
pub struct ix {

// Latter
pub fn add_ix(a: &ix, b: &ix) -> ix {
```

## Borrowing

- Why borrow?
    - These are *data structures*, not numerical literals.
- Much closer to vectorized operations than to integer addition.
```py
>>> import numpy as np
>>> hours = np.array([100, 30, 9, .5])
>>> hours * 34
array([3400., 1020.,  306.,   17.])
>>> >>> np.sum(hours * 34)
np.float64(4743.0)
```

## FAQ

- Isn't there a way to use just `+` and `-`.
  - Yes.
  - I didn't find it interesting, you are welcome to do so.
  - Provide wrappers of the needed type (`(&ix, &ix) -> ix`) to use the autotester.

# Today

  - &check; Finite sets, rings
  - &check; Arbitrary/high precision integers
  - &check; Arithmetic operations
  - &check; Function types
