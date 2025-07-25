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
        - Windows key -> "Terminal" -> Enter -> `wsl`

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

## Repository

- Create a repository for this class.
- Requirements
    - Name is `271rs`
    - Use [this template](https://github.com/new?template_name=271rs&template_owner=cd-c89)
    - May be public or private to you and me ([cd-public](https://github.com/cd-public/)).
        - [Read more](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository)
    - Must email me a link to your repository from your @willamette.edu email.
```{.email}
https://github.com/cd-example/271rs
```

## Remote

- We have now created a *remote* repository on GitHub.
	- Remote as in "not on our computer we are using right now"
	- As in "on a web server somewhere"
- No we will make a *local* repository on our own computer.
- Then connect them!


# ssh 

- We know how to deal with a very important topic:
- *Security*
- When moving executable code between websites and our system, we have to be careful that it is:
  	- Not tampered with
	- Made by who said made it

---

## Security Concession

- We will use SSH, the "Secure Shell Protocol"
- It is supported by `git`/GitHub and all major operating systems.

---

## Keygen

- SSH is based around having "keys"
  	- Under the hood, these are special numbers with special properties related to primes, basically.
- We generate a special unique key we can use as a password or signature.
```{.bash code-line-numbers="false"}
ssh-keygen
```

---

## Prompts

- This example uses (1) the default location and (2) no passphrase.
	- This is less secure but easier to manage.
	- Work in a passphrase as soon as you can!

```{.bash code-line-numbers="false"}
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/calvin/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/calvin/.ssh/id_ed25519
$ cat ~/.ssh/id_ed25519.pub 
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIE5cnx/tgBp8v/LnuHz28evmnRPrnlz3cvYaAAM4G0ik calvin@calvin-Precision-3490
```

- You now have a key! Let's find a lock.

---

## GitHub

- The purpose of this exercise is to connect to GitHub!
- We will mostly use `git` for that, but we can check if we have a connection easily:

```{.bash code-line-numbers="false"}
ssh -T git@github.com
```
- [Read more](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)

---

## Example

- This is what I see:

```{.bash code-line-numbers="false"}
The authenticity of host 'github.com (140.82.116.3)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

- Before saying "yes" or "no" compare versus the "public SSH key fingerprints"
	- Check them [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)
- By default, the modern keygen uses "Ed25519" so compare those keys, and click "yes" if they match!

---

## Connecting

- After confirming the key correctness, you will likely see this.

```{.bash code-line-numbers="false"}
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
git@github.com: Permission denied (publickey).
```

---

## One Way

- Now we have instructed *our* computer to trust GitHub.
- To save our code to GitHub, we must also get GitHub to trust *our* computer.
- We generated our key, now we must match it to our lock on GitHub!

---

## GitHub pt 1

- We follow [this guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- Return to GitHub and in the top right click your profile.
  	- For me, a picture of myself.
- Scroll down to "Settings" and click.
  	- Last in 2nd grouping, for me.

---

## GitHub pt 2

- Within settings left-side menu click "SSH and GPG keys"
  	- Middle of 2nd group (Access) for me.
- Within the center block click <span style="background-color:#238636;color:white">New SSH key</span> in the top right of the block. 

---

## Prompt

- I get a page "Add new SSH Key".
- I provide a title (like "For 271rs class" or "Laptop")
- Now we'll get our key from our system to use.
- Recall we previously generated a key to the default location, like 
`/home/calvin/.ssh/id_ed25519`
	- If you don't remember, just type `ssh-keygen` and it'll show you.

---

## Copy/Paste

- To get the key for GitHub, we can can 
  - `cat` that file in the command line
  - Copy from the command line
  - Paste into the GitHub "Key" field
  - Click <span style="background-color:#238636;color:white">Add SSH key</span> 

---

## SSH Test

- After adding the key to the account, I confirm via SSH like so:

```{.bash code-line-numbers="false"}
ssh -T git@github.com
```

- I see the following:

```{.bash code-line-numbers="false"}
Hi cd-public! You've successfully authenticated, but GitHub does not provide shell access.
```

# Clone

- With `ssh` configured on your local device and on the remote service, you can clone your `271rs`.
    - This will be a another copy of the same repository you use.
    - It based off of (templated off of) a repository I made under my account.
    - Template $\neq$ clone.

---

## Clone pt1

- Navigate to the repository webpage, like `github.com/cd-example/271rs`
- Find the <span style="background-color:#238636;color:white">\<\> Code</span> button in the top right.
- Click it:
    - Select the top "local" tab (for or local repository)
    - Select the SSH option (for our SSH key)
    - Copy the name, like 

> git@github.com:cd-example/271rs

---

## Clone pt2

- Within terminal, where you keep files for this class.
    - Probably just do
```{.bash}
cd ~
git clone git@github.com:cd-example/271rs 
```
- Verify by listing the contents of the `271rs` directory via:
```{.bash}
ls 271rs
```
- You should see a `README.md` and a `LICENSE`

## Enter the Repository

- To change the directory within which you are working in the commandline from your home to the repository for this class, do:
```{.bash}
cd 271rs
```
- Verify the change via
```{.bash}
pwd
```
- This will give the full address of your class folder, ending in `271rs`

# Exercise

## Today

- To complete the lab today, add a `01/rustup.md` file to your `271rs`
- Send me a link to a `271rs` repository I have permission to view.
    - To be clear:
        - I must receive an email with a hyperlink to a GitHub repository.
        - I must have view access to public repository or a repository on which I am added as a collaborator.

## Names Matter

- Your submission will be tested be a script.
    - The file must be named `rustup.md`
    - It must be in a folder named `01`
    - The repository must be named `271rs`
    - No other arrangement constitutes a lab submission.
    - The contents of `rustup.md` are not relevant.

## File Editor

- Let's make a new file.
- I recommend using `vim`, `neovim`, or `helix`.
- *Probably* already have it on MacOS.
- On WSL install via
```{.bash code-line-numbers="false"}
sudo apt install vim
```

## File Editting

- To create said file, type `vim` then the name of the file.
- If you just cloned `271rs`, there will be a `271rs` folder into which you should create a `01` folder.
    - Stands for week 0, day 1
```{.bash}
vim 01/rustup.md

## Using `vim`

- There's more to life that using `vim` but basically:
    - Press `i` to enter "insert mode" (so you can type)
    - When you are done typing, press ESC then type `:x` to save and exit.
    - [Read more](https://cd-public.github.io/scicom/02_neovim.html)
- Just type some notes you have from today.

## Check Status

- You have now added a new file to your repository.
- I consult status often, yours will likely look like this:
```{.bash code-line-numbers="false"}
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        01/rustup.md

nothing added to commit but untracked files present (use "git add" to track)
```

## Add

- The first thing we not is that there are "Untracked files"
- While we made a `hello.py` and have it in our `hello-world` directory, it isn't yet "tracked" by `git`!
- By default, `git` only keeps track of what we tell it to!
- So, we tell it to track our code!

```{.bash code-line-numbers="false"}
git add 01/rustup.md
```

## Status

- I check status again	

```{.bash code-line-numbers="false"}
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   01_rustup.md
```

## Commit

- With `git` now aware of `hello.py`, we need to commit or changes for `git` to save them.
  	- Similar to saving files to the file system.
	- There are, of course, ways to automate this.
- This probably won't work at first (next slide!) but try:

```{.bash code-line-numbers="false"}
git commit -a -m "first commit"
```

## "-a -m"

- Commits require a commit message (like a version name or number) so specify with `-m`
- Usually I provide `-a` to commit "all" files.
- I usually make some effort to make my life easier with specific commit messages, perhaps listing:
	- What I'm trying to do
	- Why?

## Config

- If you haven't used `git` on your system before, you'll have to tell `git` who you are.
	- In `git` there are no *anonymous* changes - you have to sign every change you make.
- You'll be prompted to provide something like this:
  

```{.bash code-line-numbers="false"}
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
```

## My name

- I often include which computer I'm using in my name and also don't use a real email address.
  	- My GitHub account is already attached to an email address, so I use a throwaway for commits.

```{.bash code-line-numbers="false"}
git config --global user.email "prof_calvin@c89>rs.edu"
git config --global user.name "Calvin for Class"
```

## Looping Back

- Once you have provided your identity, you can successfuly complete a commit.

```{.bash code-line-numbers="false"}
git commit -a -m "first commit"
```
- This will:
  	- Mark current code as a version, named by your commit message.
- This won't:
  	- Do *anything* to GitHub.

## Push

- A commit saves changing on your computer.
- To save on GitHub, push changes to the cloud

```{.bash code-line-numbers="false"}
git push
```

- After a moment and some diagnostic text, you should be able to see your code on GitHub, possibly after refreshing the page!

## Diagnostics

- For example, you might see the following:

```{.bash code-line-numbers="false"}
Enumerating objects: 27, done.
Counting objects: 100% (27/27), done.
Delta compression using up to 22 threads
Compressing objects: 100% (15/15), done.
Writing objects: 100% (16/16), 98.54 KiB | 2.46 MiB/s, done.
Total 16 (delta 11), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (11/11), completed with 10 local objects.
To github.com:cd-example/271rs.git
   adaa3a7..ba3c794  main -> main
```

## Verify

- [ ] Ensure you have a `01/rustup.md`
- [ ] Email me.


# Everyday Use

## Easier After

- A lot of what we did, we only have to do once:
  	- `git config`
	- `ssh-keygen`
	- `set origin`
- Many are special cases:
  	- Only have to make new repositories for... new repositories (likely projects)
	- Only have to `git add` for new files.

## Quick Example

- Let's add `02/hi_world.rs`
- We'll create a new file at the command line.
```{.bash code-line-numbers="false"}
vim 02/hi_world.rs
```
- Add any text
```{.python filename="hi_world.rs"}
Wait I don't know rust yet.
```

## Add, Commit, Push

- To get the code onto Github, add to the repo:
```{.bash code-line-numbers="false"}
git add hi_world.rs 
```
- Commit changes to a version:

```{.bash code-line-numbers="false"}
git commit -a -m "You say hello, I say goodbye"
```

- Push to GitHub

```{.bash code-line-numbers="false"}
git push
```

- And that's that!

## Altogether

- For a single copy/paste
```{.bash code-line-numbers="false"}
git add bye.py
git commit -a -m "You say hello, I say goodbye"
git push
```

- If it works, you'll see the change on GitHub!


## Again

- Perhaps we wish to be more correct with a well-formed Rust comment.
```{.python filename="bye.py"}
// TODO: Homework 0 
```
- We'll learn Rust latter.

## No Add

- Don't need an add this time!

```{.bash code-line-numbers="false"}
git commit -a -m "Rust comment"
git push
```

## Pulling

- To get remote changes reflected locally, simply use
```{.bash code-line-numbers="false"}
git pull
```
- This will be how assignment feedback is distributed.
- Just `git pull` every time you start working, basically.
- Also good when you are working on multiple devices.

# Fin
