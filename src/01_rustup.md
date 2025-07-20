---
title: Rustup
---

## Announcements

- Lab Day
    - Set up environment

## Homework

- The first homework, "Hi world", is ready after this class.
  - It is comically trivial.
  - Mostly makes sure you have everything set up.
- Due Friday, 1 Sept. at 1440 ET.

## Today

- Set up your operating system, if it is not UNIX-based.
- Install Rust.
- Install Git
- Bonus!
    - Install Vim, Neovim, or Helix.

# Systems

## Windows

- Windows usage is not supported in the course.
- If you are using Windows, you must:
    - Use Windows Subsystem for Linux (Recommended)
    - Use Docker or Podman 
    - Use Git Bash or Mingw in some other way (Discouraged)
    - Use Cygwin (Discouraged)

---

### WSL 2

- Windows Subsystem for Linux
- Follow [this guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- Notes:
    - Use WSL 2. It is the default.
    - I recommend using Ubuntu distribution. You will be asked.
    - I prefer [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-US&gl=US).
        - Windows key -> "Terminal" -> Enter
        - Type `wsl`
---

### Docker or Podman

- Both will require WSL 2, but install for you
- Docker has better Windows support, I believe Podman is seeing more use.
- Follow [this guide](https://docs.docker.com/desktop/setup/install/windows-install/).
- Notes:
    - Use WSL 2 backend.
    - You are responsible for teaching yourself containers.
    - [Slides for last year.](https://cd-public.github.io/courses/old/c89s25/qmd/podman.html#/what-is-podman)
---

### Git Bash

- I have set up guide for Git Bash for [another course](https://cd-public.github.io/scicom/qmd/A1_gitbash.html)
- This seemed like it could work. I won't be checking.
---

### Cygwin

- I have no idea how Cygwin works but it's pretty cool.
- Basically no longer in use due to WSL 2 and Docker.
- Follow [this guide](https://www.cygwin.com/install.html)
---

## MacOS

- MacOS should mostly work out-of-the-box.
- You need one thing: XCode

# Rust

## Rustup

- On your UNIX-based OS:
    - Linux
    - MacOS
    - WSL 2
    - FreeBSD
- Open the command line and run the following:
```{.bash}
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```
- [Read more](https://doc.rust-lang.org/book/ch01-01-installation.html)

## Verify

- To ensure you have a Rust installation, run:
```{.bash}
rustc --version
```
- At time of slide creation, I saw this version:
```{.bash}
rustc 1.87.0 (17067e9ac 2025-05-09)
```

# Git

## Git Installation

- Ensure you have a Git installation:
    - Windows:
        - Launch WSL
```{.powershell}
wsl ~
```
        - Install `git` within WSL
        ```{.bash}
sudo apt install git
```
    - MacOS:
        - [Launch the terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac) and then: 
```{.zsh}
xcode-select --install
```

## Verify

- Verify install via:
```{.bash}
git --version
```
- I had:
```{.bash}
git version 2.34.1
```

# GitHub

## Account

- Ensure you have an account on GitHub.
- [Read More](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)


