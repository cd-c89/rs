---
title: "Hi world"
author: ""
subtitle: "Due 5 Sep 1440 ET"
format: html
---

# Setup

## Sketch

- By convention, the first program in a new language is "Hello, world!"
- Rust follows this convention in the Rust Book.
    - We basically do [Chapter 1.2](https://doc.rust-lang.org/book/ch01-02-hello-world.html)

## Pre-flight Checks

- You should have
    - `git` installed and working.
    - A repository named `271rs`, both a local repository on your device and a remote repository on GitHub.
    - An editor, which really should be text-based, in-console text editor, but I can't actually ban you from using VS Code.
    - `rustc` installed and working.
- If you miss any of this, back to [lab](01_rustup.md).

## Requirements

- To complete this assignment, you must:
    - Create a `02/hiworld.rs` file in your `271rs` repository.
    - Ensure this file:
        - Is present in the remote repository on GitHub, to which I have access after the lab, and...
        - That the file can be compiled, as specified below, and...
        - The executable produced by compilation prints "Hi world".
        
# Review

## New Folder

- You will need to make an `02` folder in `271rs` to save your work.
- Ensure your shell/terminal/console/command line is in the `271rs` repository.
    - Review the [lab](01_rustup.md).
    - Review the [shell](https://cd-public.github.io/scicom/03_shell.html).
- Use:
```{.bash}
mkdir 02
```

## New File

- You will need to edit a `hi_world.rs` file in the `02` folder.
- Use something like:
```{.bash}
vim 02/hi_world.rs
```
- Or perhaps:
```{.bash}
cd 02
vim hi_world.rs
```
- We recall that to save and exit vim we press the ESC key then type `:x` then press ENTER.
    - Read more [here](https://cd-public.github.io/scicom/02_neovim.html#modes)

## New Program

- You should have `rustc` installed.
- If I were you, I'd leave open a terminal window with `vim` and create another to use `rustc`
- For example, when you first create and save an empty file as `hiworld.rs`, you can use `rustc`:
```{.bash}
rustc hi_world.rs
```
- You'll see the following:
```{.bash}
error[E0601]: `main` function not found in crate `hi_world`
  |
  = note: consider adding a `main` function to `hi_world.rs`

error: aborting due to 1 previous error

For more information about this error, try `rustc --explain E0601`.
```
- This is good enough for now.

# Hi world

## Citation

- The following content is lifted directly from the Rust Book

## Writing and Running a Rust Program

### .rs

- Rust files always end with the `.rs` extension.
- If you’re using more than one word in your filename, the
convention is to use an underscore to separate them. For example, use
`hi_world.rs` rather than `hi_world.rs`.
- In `hi_world.rs` enter the following:

```{.rust filename="hi_world.rs"}
fn main() {
    println!("Hello, world!");
}
```

### rustc

- Save (ESC + `:w` in vim) the file and go back to your terminal window.
- Enter the following commands to compile the file:

```{.bash}
rustc hi_world.c
```

::: {.callout-note}
Rust is a compiled language, unlike Python, bash, or R. To create programs in Rust, we first "compile" the source code in an executable. We do not "run" `.rs` files, as we do with `.py` files using the `python3` command.
:::

### Verify

- Verify that compilation was successful by using `ls` to list the files in your folder.
```{.bash}
ls
```
- You should see the following.

```{.bash}
hi_world  hi_world.rs
```

- `hi_world` is a program, and `hi_world.rs` is source code.

### Run

- To use a Rust program, we do not have to call `rustc` like we do with Python `.py` scripts!
- We use `./` notation to have the shell interpret `hi_world` as a program to be run
    - `.` means use the current folder (should be `02`)
    - `/` means find the file by name in the current folder.
```{.bash}
./hi_world
```
- You should see:
```{.bash}
Hello, world!
```

::: {.callout-note}
If you created your `hi_world.rs` file using e.g. `vim 02/hi_world.rs`, then the file will be in a different folder. You may need to run `rustc 02/hi_world.rs` or `./02/hi_world`. Review [the file system](https://cd-public.github.io/scicom/03_shell.html#the-file-system) if you get stuck.
:::

# Anatomy of a Rust Program

## The first piece

```rust
fn main() {

}
```

- These lines define a function named `main`. 
- The `main` function is special:
    - It is always the first code that runs in every executable Rust program. 
- The first line declares a function named `main` that has no parameters and returns
nothing.
- If there were parameters, they would go inside the parentheses `()`.

## White space and `{}`

```rust
fn main() {

}
```

- The function body is wrapped in `{}`. 
- Rust requires curly brackets around all
function bodies. It’s good style to place the opening curly bracket on the same
line as the function declaration, adding one space in between.

## rustfmt

> Note: If you want to stick to a standard style across Rust projects, you can
> use an automatic formatter tool called `rustfmt` to format your code in a
> particular style. The Rust team has included this tool
> with the standard Rust distribution, as `rustc` is, so it should already be
> installed on your computer!

## Function Body

- The body of the `main` function holds the following code:

```rust
println!("Hello, world!");
```

- This line does all the work in this little program: it prints text to the
screen. 
- There are three important details to notice here.

## Printing

- First, `println!` calls a Rust macro. 
- If it had called a function instead, it
would be entered as `println` (without the `!`). 
- Rust macros are a way to writecode that generates code to extend Rust syntax, a latter topic. 
- It is common for printing to be uncommonly complex when learning new programming languages; Rust follows this trend. 
- For now, you just need to know that using a `!` means that you’re calling a macro instead of a normal
function and that macros don’t always follow the same rules as functions.

## Strings

- Second, you see the `"Hello, world!"` string. 
- We pass this string as an argument to `println!`.
- Then string is printed to the screen.

## Semicolons

- Third, we end the line with a semicolon (`;`), which indicates that this
expression is over and the next one is ready to begin. 
    - An expression is the atomic unit of code.
        - This is an expression:
        
            ```{.py}
            x = 1
            ```
        - This is not, it is divisible into valid code (two expressions)
        
            ```{.py}
            x = 1
            print(x)
            ```
        - THis is not, it is not independently valid code.
        
            ```{.py}
            x = 
            ```
- Most lines of Rust code end with a semicolon.
    - This is legal in Python:
    
        ```{.py}
        x = 1;
        print(x);
        ```
        
# Fin

- You are done *coding* once your `hi_world.rs` file:
    - Compiles, and
    - When run, prints "Hello, world!" or some other string that is school appropriate
        - The complete text of *Infinite Jest* is the boundary between appropriate and inappropriate.
        - Emojis that are supported on some but not all of MacOS, Linux, and Windows form the boundary between some string and not a string.
            - 🖾��￼fo9i?⛔󠀰🩷🫴✍
- You are done with the *homework* once said `.rs` file is:
    - Visible, to me, 
    - On the GitHub `271rs` repository you shared for the lab
- If you need to review how to get files onto GitHub, review [the lab](01_rustup.md)