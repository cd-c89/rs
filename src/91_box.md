---
title: "Box"
format: html
---

## Preamble

You know what a stack is. Now make one in Rust.

- [ ] Use Rust `Box` to create a recursive data structure.
- [ ] Use functional programming to maintain references.
- [ ] Review pattern matching.
- [ ] Review the humble `tuple`

::: {.callout-caution}

## This is non-obvious.

After much angst, I have adopted a highly "functional" style of programming.

The `Stack` I provided testing scripts for uses no methods, does not persist state beyond end of ownership, and is never passed as a reference (except to `dbg!()`, which is also allowed in functional languages.

You may not be used to thinking or writing this way, but it is awesome and fun and worth trying.

:::

## Box

We may naively attempt the following [^1]


[^1]: By which I meant, this was my plan for this lab until it didn't work.

```{.rs filename="src/lib.rs"}
#[derive(Debug)]
struct Node {
    data: String,
    next: Option<Node>,
}
```

- `#[derive(Debug)]` is in the slides but wasn't covered in lecture. 
- It allows using `dbg!()`.

To my dismay this wasn't allowed.

```sh
error[E0072]: recursive type `Node` has infinite size
 --> stuff.rs:1:1
  |
1 | struct Node {
  | ^^^^^^^^^^^
2 |     data: String,
3 |     next: Option<Node>,
  |                  ---- recursive without indirection
  |
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
3 |     next: Option<Box<Node>>,
  |                  ++++    +
```

### On Box

- To put some `x` in a `Box`, simply:
```rs
let x = String::from("I'm a capital-S String.");
let b = Box::new(x);
```
- To remove `x` from the `Box, simply use the special "unary asterisk" operator, also called "dereference".
```rs
let s : String = *b;
```

::: {.callout-caution}

### This is about the stack, the heap, and references.

- Without using `Box` misdirection, a `Stack` is of potentially infinite size.
- Box creates a distinct data structure on the heap for each "layer" of the stack.
- So every `struct` contains only 1 data value and the location of the next data value.
- This should remind you of something (linked lists).

:::


## Starter Code

### `src/main.rs`

- A testing script:

```{.rs filename="src/main.rs"}
use stack::*;

fn main() {
    let mut s = init();
    dbg!(&s);
    s = push(String::from("0"), s);
    dbg!(&s);
    s = push(String::from("1"), s);
    dbg!(&s);
    let (popped, mut s) = pop(s);
    dbg!(popped);
    dbg!(&s);
    s = push(String::from("n"), s);
    dbg!(&s);
}
```

- We note:
    - Every stack operation returns the stack.
    - `pop` returns a tuple to return the popped value and the stack.
    - No references are used in computation.
        - They are used for debug.

### A `src/lib.rs` excerpt

- You don't have to use this if the tester still works; it is simply what I used.

```{.rs filename="src/lib.rs"}
#[derive(Debug)]
struct Node {
    data: String,
    next: Option<Box<Node>>,
}

#[derive(Debug)]
pub struct Stack {
    vals: Option<Node>,
}

pub fn init() -> Stack {
    return Stack {
        vals: None,
    };
}

pub fn push(val: String, mut s: Stack) -> Stack {
    todo!();
}

pub fn pop(mut s: Stack) -> (Option<String>, Stack) {
    todo!();
}
```

- We note:
    - Every function returns its stack.

### Sample output

- It's not pretty because I didn't write a print formatter.
    - I do not love doing that in Rust.
    - You may.
```sh
[src/main.rs:5:5] &s = Stack {
    vals: None,
}
[src/main.rs:7:5] &s = Stack {
    vals: Some(
        Node {
            data: "0",
            next: None,
        },
    ),
}
[src/main.rs:9:5] &s = Stack {
    vals: Some(
        Node {
            data: "1",
            next: Some(
                Node {
                    data: "0",
                    next: None,
                },
            ),
        },
    ),
}
[src/main.rs:11:5] popped = Some(
    "1",
)
[src/main.rs:12:5] &s = Stack {
    vals: Some(
        Node {
            data: "0",
            next: None,
        },
    ),
}
[src/main.rs:14:5] &s = Stack {
    vals: Some(
        Node {
            data: "n",
            next: Some(
                Node {
                    data: "0",
                    next: None,
                },
            ),
        },
    ),
}
```

### Python equivalent

- This is object-oriented rather than functional.

```py
>>> s = []
>>> s.append('0')
>>> s
['0']
>>> s.append('1')
>>> s
['0', '1']
>>> s.pop()
'1'
>>> s
['0']
>>> s.append('n')
>>> s
['0', 'n']
```

- The functional implementation is left as an exercise to the interested student, beyond this snippet:

```py
push = lambda val, s : lambda a : val if a else s
```