---
title: "DAG"
format: html
---

# Preamble

You know what a DAG is. Now make one in Rust.

- [ ] Implement a relatively non-trivial graph.
- [ ] Review Rust `Box` to create a recursive data structure.
- [ ] Review how to maintain references.
- [ ] Review the CS major requirements.

::: {.callout-caution}

## Review: Box

- To put some `x` in a `Box`, simply:
```rs
let x = String::from("I'm a capital-S String.");
let b = Box::new(x);
```
- To remove `x` from the `Box, simply use the special "unary asterisk" operator, also called "dereference".
```rs
let s : String = *b;
```

<!--

# The BS CS

- New for 2025,

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

-->