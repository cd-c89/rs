---
title: "Guess"
format: html
---

## Announcements

- Lab Day
    - Prepare for Wordle

## Homework

- Wordle is ready after this class.
  - It is exactly hard enough to use all programming basics.
  - Windows development is no longer supported.
- Due Friday, 19 Sept. at 1440 ET.

## Citation

- The idea to do Wordle as the first Rust assignment was inspired by the Chapter 2 of the Rust Book, [Guessing Game](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html)
- The idea to do Wordle as a programming assignment is inspired by the Nifty Assignment of the [same name](http://nifty.stanford.edu/2022/eroberts-spelling-bee-wordle/).

## Today

- [ ] `const`
- [ ] Character iteration
- [ ] `/dev/urandom`
- [ ] `stdin()`
- [ ] "Fixes"


# consts

## Compile time

- In Wordle, you'll likely have two kinds of values that won't change.
    - The "ANSI Escape Codes" which allow you to print to the terminal in color, which are set when you install your operating system.
        - For these we may use a Rust `const`
    - The "answer" which will be set as soon as the program begins running, and never be altered thereafter.
        - For these, we use a `let`.
- I refer to the first as "compile time constants" and declare them outside of any function.

```{.rs filename="src/main.rs"}
const RED : &str = "\u{001b}[31m";
const WHT : &str = "\u{001b}[0m";

fn main() {
    println!("White text. {RED}Red text. {WHT}White text.");
}
```

*This section transparently added in response to a question in class. I do not use `const` in my own code rather than `let`, though perhaps I should.*

## Create constants

- Create your own constants for yellow and green.
    - You may want to write a loop to try different colors, or consult documentation.
- For Wordle, I used a function with the following type, which you may wish to take as inspiration, to print a single character in a given color.
```{.rs}
fn letter(a:char, c:i32)
```

# Character iteration

## Strings lack indices

- In Python, we have some packing and unpacking to do to edit strings by character index.
```{.py}
>>> s = list("hello, world")
>>> s[10] = 'd'
>>> s[11] = 'l'
>>> "".join(s)
'hello, wordl'
```

## Rust uses `.chars()`

- In the case of Wordle, all solutions are formulated as 5 characters, so we can assume the underlying character-ness of strings.
    - This is not permitted *generally* in Rust, but in our case we may.
- To unpack Rust strings into characters, you may use `.chars()`

```{.rs filename="src/main.rs"}
fn main() {
    let s = "Hello, world";
    println!("{:?}", s.chars());
}
```

- What do you see?
    - Can you access the `i`th element?
    - Can you loop over object?
    
## Iterators

- What `.chars()` returns is called an iterator, it is much like a Python generator.
```{.py}
>>> gen = (i ** i for i in range(100))
>>> next(gen)
1
>>> next(gen)
1
>>> next(gen)
4
>>> next(gen)
27
>>> next(gen)
256
```
- Basically, it is a collection type of unknown size where next elements may be queried.

## Rust uses `.nth()`

- You can see the `n`th element of an iterator with `.nth()`, more or less:

```{.rs filename="src/main.rs"}
fn main() {
    let s = "Hello, world";
    println!("{:?}", s.chars().nth(10));
}
```
- What do you see?
    - What happens if you ask for the 256th letter?
    
## Options

- Rust library functions almost always return an `Option`
    - This is just good practice, it beats returning e.g. Python `None` sometimes, or crashing.
- An option is simple:
```rs
pub enum Option<T> {
    None,
    Some(T),
}
```

## Options for options

- [ ] Pattern match
- [ ] Expect
- [ ] Unwrap

## Pattern match

- The language designers intend options to be handled as follows:

```{.rs filename="src/main.rs"}
fn main() {
    let s = "Hello, world";
    match s.chars().nth(11) {
        Some(c) => println!("The 11th character is {:?}", c),
        None => println!("String `s` is fewer than 11 characters in length"),
    }
}
```

- I very rarely see code that looks like this, including in official Rust documentation.
- For example, the Polars documentation does not manage `Option` return types this way.
- This is, however, the only way to ensure code does not crash on e.g. arbitrary length input.

## Expect

- The incrementally less heavyweight option is with `.expect()`, a method of options that either:
    - Sucessful unpacks the option into a usable type, or
    - Causes a "panic" - a comparatively graceful program crash.
        - This panic prints the message you furnished to expect.
        
```{.rs filename="src/main.rs"}
fn main() {
    let s = "Hello, world";
    println!("{:?}", s.chars().nth(13).expect("The string literal is known to be of length 11"));
}
```

- Try checking for existing and non-existant characters. What do you find?

## Rust uses `.unwrap()`

- The incrementally less heavyweight option is with `.unwrap()`.
- Unwrap does not require a message but is otherwise just like `.expect()`
- Unwrap is used by e.g. the Polars documentation.

```{.rs filename="src/main.rs"}
fn main() {
    let s = "Hello, world";
    println!("{:?}", s.chars().nth(13).unwrap());
}
```

- Try `.unwrap()` on both successful and failed `.nth()` calls.

## Unwrap vs. Expect

- I have never voluntarily used `.expect()` instead of `.unwrap()`, but...

::: {.callout-note appearance="simple"}

## Help Yourself


If your code uses `.unwrap()` instead of `.expect()` you should carefully consider converting any `.unwrap()`s to `.expect()`s before asking someone else, who is less familiar with the assumptions you made when writing your code, for help.

This applies to colleagues, QUAD TAs, and potential to the course instructor depending on how busy things are.

:::

# /dev/random

## Randomization

- There are always many ways to generated results that are vaguely random.
- As a security researcher, I am required to instruct you about `/dev/random` rather than use the Rust Book recommendations.
- Separately we:
    - Learn to read from a file.
    - Get to think about how random different things really are.

## Quoth Wikipedia

> [In Unix-like operating systems, /dev/random and /dev/urandom are special files that provide random numbers from a cryptographically secure pseudorandom number generator (CSPRNG). The CSPRNG is seeded with entropy (a value that provides randomness) from environmental noise, collected from device drivers and other sources. Users can obtain random numbers from the CSPRNG simply by reading the file.](https://en.wikipedia.org/wiki//dev/random)

## Peep it

- Verify you are on a system implementing `/dev/random` with the following, at command line:
```{.bash}
head -1 /dev/random
```
- For me, I see:
```{.sh}
$ head -1 /dev/random
6��c�W�Y|S�t��|��=���U�>�$��8�����E���*�&;�F�§�6␦8�{X�~�1U�J␦�Y���Eyg��Z��{ ��^"/%!7���vv@�w{p��q�y"� AD�/Ahb��fb��Ed�
                                                                                                                      ­�k�:���F�>����09h��Ʊl#�>�J����:J����5|I�E���04�������NH��-�X����l�,k�<�������=.4^qav�}Y��
        ��(�)1���B���c)�&*�#r��"H�(�:�e���֩A
$
```
- You can test what `head` does on a file with which you are familiar, or consult `man head`

# File I/O

## `open`

- A la Python, Rust utilizes `open` to read files.
- Unlike Python, Rust has a great love for gobs of a text and `Option`s.
- The following opens `/dev/random` to be read.
    - Think about why we need to `.unwrap()` when opening a file.
    - What is the Python equivalent?
```rs
std::fs::File::open("/dev/random").unwrap();
```
- We require mutability to be able to read successive bits from the file, as our location in the file is tracked within the Rust `File` object.

> An object providing access to an open file on the filesystem.

## `use`

- A lot of people who aren't me prefer to use `use` to have shorter names.
- I don't personally understand this, but I do use `from pgl import *` in Python.
- Here's an example from [Rust documentation](https://doc.rust-lang.org/std/fs/struct.File.html) of a `use`:
```{.rs filename="src/main.rs"}
use std::fs::File;

fn main() {
    let mut devrnd = File::open("/dev/random").unwrap();
}
```

- [The Used - The Bird And The Worm (Video)](https://www.youtube.com/watch?v=12dBCgAo-RA)

## `read`

- True to form, `read` has a variety of complexities introduced by:
    - Not assuming anything about the Rust `File` object
    - Not assuming anything about how to read or save data.
    - Not assuming anything about the underlying file within the computer's file system.
- I use it as follows:
```rs
std::io::Read::read_exact(&mut devrnd, &mut buffer).unwrap();
```
- An astute reader will notice a few idiosyncracies.

## `&mut`

- When we:
    - Have a variable in Rust
    - For which the ownership model applies, such as a file of arbitrary size
    - For which mutability is necessary, such as a `File` object from which `n` bytes have been read.
- We can use this variable:
    - Within some other function, while
    - Retaining the ability to use it again in some future function.
- We do so by passing a "mutable reference", generated by prefixing the variable name with `&mut` and a space.

## Buffers

- It is common in lower level languages to read from a file into a "buffer", a temporary storage space within the executing program.
- These are commonly implemented as multiple of bytes of some fixed size in that language's array type.
- These bits are commonly initialized to zero.
- I am aware of no graceful way to do this in Rust, so I'll tell you what I'm doing now and why.

## Arrays

- Arrays in Rust are fixed size and typed, not unlike NumPy array.
- They see little use versus the more common vector type, but I preferred arrays for Wordle.
    - And in fact expect to prefer arrays this term.

## Quoth the [Docs](https://doc.rust-lang.org/std/primitive.array.html)

- A fixed-size array, denoted `[T; N]`, for the element type, `T`, and the non-negative compile-time constant size, `N`.
- There are two syntactic forms for creating an array:

    - A list with each element, i.e., `[x, y, z]`.

    - A repeat expression `[expr; N]` where `N` is how many times to repeat expr in the array. expr must either be:
        - A value of a type implementing the Copy trait
        - A const value
- I never read this, I found [this page](https://blog.orhun.dev/zero-deps-random-in-rust/) through a search engine and ripped it.
    - Search for `dev/urandom` on that page.
    
## Create an array

- The following is a mutable - so we can read file data *into* it - array of 8 bytes.
```rs
let mut buffer = [0u8; 8];
```
- Breakdown.
    - The `0` in `0u8` is the initialization value.
    - The `u8` is the type, unsigned 8 bit value.
    - The post comma `8` is the number of 8 bit values to store.
- There's only one problem here.
    - That second `8` is a magic number, which to me represents poor style.
        - Believe me, I wanted to just type 8, but we shouldn't.
        
## On Magic Numbers

- To select a random word, eventually you will probably have:
    - An array of 5 letter words.
    - That array will have some length.
    - That length will be whatever Rust uses to store the size of memory objects.
    - Different computers have different ways of address memory...
    - So we cannot make assumptions about the size of values which themselves store the size of memory.
        - I wish I was kidding! I'm not!

## 32 vs 64 bit

- For example, how many memory locations can be addressed by a 32 bit system?
- How many on a 64 bit system?
- Does your device potentially use 48 bit addresses?
- How could you tell?
- What if you run code on a 16 bit microcontroller?
- Enter `usize`
    - The unsigned value that is the right size to store a size.
    
## `usize`

- We will use `usize` by name twice:
    - We need to read a random usize.
- We can determine how many `u8`s are required to make up a `usize` by checking how many bits are in a `usize`. and dividing by 8.
```rs
usize::BITS / 8
```
- Only one problem - for some reason `usize` stores *its* size as a `u32`.
- So to get enough bits to fill I `usize`, I ended up doing... this?
```rs
let mut buffer = [0u8; (usize::BITS / 8) as usize];
```

![](https://c.tenor.com/Xi9e2RhtY7kAAAAC/tenor.gif)

*Presumably I'm doing this wrong.*

## Check in

- I have this so far:

```rs
let mut devrnd = std::fs::File::open("/dev/urandom").unwrap();
let mut buffer = [0u8; (usize::BITS / 8) as usize];
std::io::Read::read_exact(&mut devrnd, &mut buffer).unwrap();
```

## Candidate Answers

- You can imagine testing with a smaller word list, like the words of the [Sator Square](https://en.wikipedia.org/wiki/Sator_Square)

```rs
const WORDS : [&str; 5] = ["rotas", "opera", "tenet", "arepo", "sator"];
```

- Here `&str` is used to refer to string literals, that is, *not* the `String` quasi-data structure of arbitrary size.
    - This was the type that e.g. `"hello world"` had the whole time under the hood.

```{.rs filename="src/main.rs"}
const WORDS : [&str; 5] = ["rotas", "opera", "tenet", "arepo", "sator"];

fn main() {
    let i : u8 = 2;
    println!("{:?}", WORDS[i]);
}
```
- This doesn't work.

## Indices

- An array can be as large as memory.
- So it's index can be as large as memory.
- The thing as large memory is `usize`.
```bash
error[E0277]: the type `[&'static str]` cannot be indexed by `u8`
 --> src/main.rs:5:28
  |
5 |     println!("{:?}", WORDS[i]);
  |                            ^ slice indices are of type `usize` or ranges of `usize`
```

## Byte array to `usize`

- Usize helpfully has "from bytes" methods.
    - There are 3 such methods for different *endianness*es, a future topic.
- I use little endianness because it doesn't matter - `le`
```rs
let secret = usize::from_le_bytes(buffer);
```
- This can be used as an index, but it's probably too large.

## `.len()`

- Rust furnishes the `.len()` method of arrays to detect their type.
```rs
WORDS[secret % WORDS.len()]
```

## Altogether

- We use `String::from()` to get a `String` from a `&str`, as the array contains fixed length strings and I use the `String` type for consistency with lecture recommendations.

```rs
let mut devrnd = std::fs::File::open("/dev/urandom").unwrap();
let mut buffer = [0u8; (usize::BITS / 8) as usize];
std::io::Read::read_exact(&mut devrnd, &mut buffer).unwrap();
let mut secret = usize::from_ne_bytes(buffer);
let answer : String = String::from(WORDS[secret % WORDS.len()]);
```


## Today

- [x] `const`
- [x] Character iteration
- [x] `/dev/urandom`
- [ ] `stdin()`
- [ ] "Fixes"


# stdin

## `input()`

- Python furnishes the straight-forward `input()` function.
- We don't have that in rust, but we do have"
    - `stdin()` - the "standard input" that represents text provided at terminal.
    - `.read_line()` - like Python `.read_line()` in that it reads to the next newline character, but a bit different in type.
- Essentially, `stdin()` is a function that returns a `File` the refers to the terminal.

```rs
std::io::stdin().read_line(&mut guess).unwrap();
```

- What happens if you don't unwrap?
- What type is `guess`? Array? `&str`? `String`?
```rs
let mut guess = String::new();
```

## `.trim()`

- Reading lines will return slightly longer strings that end with a newline character.
- This can be removed with `.trim()`.
- Try reading in e.g. `opera` or `tenet` and seeing the trimmed vs. untrimmed versions.
    - You may want to inspect their length, perhaps by converting to characters and using `.nth()`.

## `.contains()`

- You can check if a value is present in an array using `.contains()`.
- Check to see if the trimmed and untrimmed versions of `opera` or `tenet` are contained in the `WORDS` array.
    - You will need to fiddle with types a bit!
    - Will you need to use `&`? `&mut`? `String::from()`? Try each and see what happens - and consider why!

## `.clone()`

- Sometimes you will need to read a word from `stdin` and perhaps both compare it some other word and also decompose it into characters.
- If you need multiple copies, you may want to use `.clone()` or `cargo` may recommend use of `.clone()`.

# Closing Thoughts

## `range()`

- You may benefit from using `for` loops of fixed index.
- Rust has a syntactical rather than functional range.
- It follows the same start/stop rules as Python.

```{.rs filename="src/main.rs"}
fn main() {
    for i in 1..5 {
        println!("{:?}", i);
    }
}
```

## Vectors

- A lot of Rust programmers are extremely fond of the Vector, which completely coincidentally was not necessary for Wordle as everything in Wordle is fixed size.
- If you want to learn Vectors instead of arrays, simply consult this documentation.
- [Rust By Example: Vectors]
- You will find them similar to Python `list`.

## Today

- [x] `const`
- [x] Character iteration
- [x] `/dev/urandom`
- [x] `stdin()`
- [x] "Fixes"
