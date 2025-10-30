---
title: "Traits"
format: html
---

## Preamble

You know what a queue is. Now make one in Rust.

- [ ] Use generics to create a stack and heap that can store any type.
- [ ] Use traits to implement push and pop operations for both data types.
- [ ] Review pattern matching.
- [ ] Review the humble `tuple`
- [ ] Review ownership.

::: {.callout-caution}

## Design Decision

- With the addition of a queue, you get to decide:
    - Whether to head push and tail pop, or...
    ```py
>>> # Tail push, head pop
>>> _ = [q.append(i) for i in range(3)]
>>> q
[0, 1, 2]
>>> q.pop(0)
0
```
    - Whether to tail push and head pop.
    ```py
>>> # Head push, tail pop
>>> q = list()
>>> _ = [q.insert(0,i) for i in range(3)]
>>> q
[2, 1, 0]
>>> q.pop(-1)
0
```

- This is the added difficulty incurred by adding a queue.

:::

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

## Novel: Generics

- You are welcome to read Rustbook on [Generics](https://doc.rust-lang.org/book/ch10-01-syntax.html)
- We previously "hard-coded" the `Stack` to accept strings.
```rs
pub struct Stack {
    data: String...
```
- We instead append a type annotation to the end of stack, like so:
```rs
pub struct Stack<T> ...
```
- By convention, Rust uses `T` to refer to a type variable.
- Then, within the declaration we may refer to `T`:
```rs
pub struct Stack<T> {
    data: T...
```
- Upon making this change, you will get a series of `rustc` complaints about not specifying types in a variety of locations.
- You will have relatively little difficulty working through these, and should learn something valuable in the process.

## Novel: Traits

- It is customary for programmers with a background in object-oriented langauges, such as Python, JavaScript, or Java, to have an affinity for methods.
- In the lab, we used functional style:
```rs
s = push(val, s);
```
- Now we will use traits to implement methods to get the following style:
```rs
s = s.push(val);
```
- It is not required to use traits to achieve this, and possible to write methods directly, I simply found this uninteresting.
- Have two parts:
1. A declaration:
```rs
pub trait Push<T> {
    fn push(self, val: T) -> Self;
}
```
2. An implementation:
```rs
impl<T> Push<T> for Stack<T> {
    fn push(mut self, val: T) -> Stack<T> {
        todo!();
    }
}
```
- An astute observer will notice that `T` occurs **seven (7)** times just within the declarations.
    - Form your own opinion about that.
    


## Starter Code

### `src/main.rs`

- I am providing a fairly enormous testing script via [Gist](https://gist.github.com/cd-public/729970751c03c57a9a15ad0c7ef566c0).

<style>
/* https://github.com/lonekorean/gist-syntax-themes */
@import url('https://cdn.rawgit.com/lonekorean/gist-syntax-themes/d49b91b3/stylesheets/idle-fingers.css');

@import url('https://fonts.googleapis.com/css?family=Open+Sans');
body {
  font: 16px 'Open Sans', sans-serif;
}
body .gist .gist-file {
  border-color: #555 #555 #444
}
body .gist .gist-data {
  border-color: #555
}
body .gist .gist-meta {
  color: #ffffff;
  background: #373737; 
}
body .gist .gist-meta a {
  color: #ffffff
}
body .gist .gist-data .pl-s .pl-s1 {
  color: #a5c261
}
</style>
<script src="your-gist-embed"></script>

<script src="https://gist.github.com/cd-public/729970751c03c57a9a15ad0c7ef566c0.js"></script>

- I have removed `dbg!()` calls and simply check popped values.