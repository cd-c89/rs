---
title: "Wordle"
author: ""
subtitle: "Due Friday, 19 Sep 1440 ET"
format: html
---

# Setup

## Citation

- The idea to do Wordle as the first Rust assignment was inspired by the Chapter 2 of the Rust Book, [Guessing Game](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html)
- The idea to do Wordle as a programming assignment is inspired by the Nifty Assignment of the [same name](http://nifty.stanford.edu/2022/eroberts-spelling-bee-wordle/).

## Pre-flight Checks

- Wordle exercises the following:
    - Strings in Rust
    - Collection types, like arrays or vectors
    - Scalar types, like integers or characters
    - File I/O and the UNIX-based file system
    - Loops

## Requirements

- To complete this assignment, you must:
    - Create a `22` directory in your `271rs` repository.
    - This folder must be a Cargo package.
    - It must leverage no *other* Cargo packages, namely it may not use packages for randomization.
```bash
cargo new 22 --name wordle --vcs none
```

## Requirements

- [ ] Character coloring via ANSI escape codes
- [ ] File I/O for randomization
- [ ] File I/O for input
- [ ] Consistency with a randomized answer
- [ ] Consistency with word list
- [ ] Consistency with prior guesses
- [ ] Styling using [Box-drawing_characters](https://en.wikipedia.org/iki/Box-drawing_characters)

*The following is a staged screenshot in VS Code, showing the expected terminal appearance.*

<center>
![](img/wordle.png)
</center>

*The following is a staged screenshot in WSL2, showing the expected terminal appearance.*

<center>
![](img/word_l.png)
</center>

# Summary

## Nifty Assignment Description

> The object of the Wordle puzzle is to figure out the hidden word for the day using no more than six guesses. When you type in a word and then hit the RETURN or ENTER key, the website gives you information about how close your guess is by coloring the background of the letters. For every letter in your guess that is in its correct position, Wordle colors the [letter green, the "correct color"]. For every
letter that appears in the word but is not in the correct position, Wordle colors the [letter yellow, the "present color"]. All letters in the guess that don’t appear in the word are colored [red, the "missing color"]

- I will assume your familiarity with Wordle, or [Read more](http://nifty.stanford.edu/2022/eroberts-spelling-bee-wordle/Wordle/python/WordleAssignment.pdf).

## Aside

- I take an extremely literal interpretation of the following.

> For every letter that appears in the word but is not in the correct position.

- I implemented this in Python as:

```py
guess[i] in answer
```

- I implemented this in JavaScript as:

```js
answer.include(guess[i])
```

- I did not engage with any complicated rules involving double letters, as I was unaware of those rules as a casual player and do not find them algorithmically interesting.
- So, in the case that a guess or an answer contains multiples of any letter, the precise correctness of any usage of the "missing color" (in our case yellow) is left undefined and to the discretion of the student.

# Reference Solution

## Python

- The following Python solution meets all assignment requirements except for usage of `/dev/random` (I wanted the example to work on Windows).
- It is not manually written Python, but created by providing a Rust reference solution to an LLM, translating to Python, and editting for correctness.
    - I did not find LLMs could go the other direction. You may find otherwise.
- A few notes:
    - The box drawing characters are spaced such that guessed letters have a space between them to the nearest horizontal box drawing character.
    - I maintain all letters in lower case. This is implicitly enforced by the requirement that guesses be members of `WORDS`
    - This is a 5 word Latin word list. You are encouraged to use the actual wordlist, which I can't find in it's original form but is present on [this webpage](https://reichel.dev/blog/reverse-engineering-wordle.html#looking-at-the-source) (Scroll to bottom).
        - Playing using this word list was relatively more challenging, as it omits many common words and plurals.

```{.py filename="wordle.py"}
# A list of valid words, truncated for this example.
WORDS = ["sator", "arepo", "tenet", "opera", "rotas"]

# ANSI color codes for colored text
# 31: Red, 32: Green, 33: Yellow
R = 31  # Red (letter not in word)
G = 32  # Green (letter in correct position)
Y = 33  # Yellow (letter in word but wrong position)

# Box-drawing characters for the game board
T = "┌───┬───┬───┬───┬───┐"  # Top border
M = "├───┼───┼───┼───┼───┤"  # Middle border
B = "└───┴───┴───┴───┴───┘"  # Bottom border

def letter(a: str, c: int):
    """
    Prints a single letter with a specified ANSI color.

    Args:
        a: The letter to print.
        c: The ANSI color code.
    """
    print(f"│ \u001b[{c}m{a}\u001b[0m ", end="")

def colors(s: str, answer: str):
    """
    Analyzes a guessed word and prints it with the appropriate colors.

    Args:
        s: The guessed word.
        answer: The correct answer word.
    """
    for i in range(5):
        char = s[i]
        color_code = R
        if answer[i] == char:
            color_code = G
        elif char in answer:
            color_code = Y
        letter(char, color_code)
    print("│")

def game(words: list[str], answer: str):
    """
    Clears the screen and draws the game board with the current guesses.

    Args:
        words: A list of guessed words.
        answer: The correct answer word.
    """
    print("\u001b[2J")  # Clear the screen
    print(T)
    for i in range(5):
        colors(words[i], answer)
        print(M)
    colors(words[5], answer)
    print(B)

def main():
    """
    The main game loop.
    """
    words = ["     "] * 6

    ###############################################
    #                                             #
    # You are required to use /dev/random in Rust #
    #                                             #
    ###############################################
    import random
    answer = random.choice(WORDS)

    attempts = 0

    print("\u001b[2J", end="")  # Clear the screen
    print("Use lowercase only btw.")

    while words[5] == "     ":
        guess = input().strip()  # Convert input to lowercase
        if guess in WORDS:
            words[attempts] = guess
            game(words, answer)
            if guess == answer:
                print("Winner")
                return
            attempts += 1
        else:
            print("Not a valid word!")

    print("Game over :(")

if __name__ == "__main__":
    main()
```

