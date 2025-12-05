---
title: Final
format: 
  html:
    code-line-numbers: false
---

**Due 09 Dec @ 5 PM PT**

# A Simple SCM

Realistically, consult the slides, but...

Your SCM should support minimally:

- Commit
    - Which must subsume:
        - `git init`
        - `git add <file>`
        - `git commit -m <message>`
- Revert
    - Which must subsume:
        - `git checkout`

It may optionally support:

- Viewer
    - Akin to:
        - `git log`
        - `git diff`
- Scrape
    - Akin to:
        - `git reset`

You are not required to implement integrity or confidentiality checks, but are encouraged to do so.

- Integrity:
    - Cache SHA2 checksums of all commits.
    - Store checksums in a Merkle tree
- Confidentiality:
    - Sign all commits using Ed25519 to encrypt the hash of the commit with a private key.
        - Likely in `.ssh/id_ed25519`
    - Verify signatures using the corresponding public key.

In each case you should only allow an `scm revert` if the integrity and/or confidentiality checks pass (depending on which you implement).

# Demo

## On `PATH`

For the sakes of this demonstration, after creating a binary - which in my case was named `scm` - I added it to "path" variable `PATH` which allows using it directly from terminal.

For example, say beginning in my home directory I made a a new crate named `scmrs` then used `cargo build release` to create the binary.

```{.sh}
export PATH=~/scm/target/release/:$PATH
```

Read more on [Stack Overflow](https://unix.stackexchange.com/questions/138504/setting-path-vs-exporting-path-in-bash-profile?noredirect=1&lq=1).

## Demo

A perfect final (100/100) will be able to do the following.

```{.sh}
$ vi file.txt
$ cat file.txt
#000001 line
#000002 line
#FF0000 line
#0000FF line

$ scm commit
$ vi file.txt
$ cat file.txt
One line
Two line
Red line
Blu line

$ scm commit
$ scm revert
$ cat file.txt
#000001 line
#000002 line
#FF0000 line
#0000FF line
```

In brief:

- Create some version of a file which we term version $v$
- `scm commit`
- Issue some changes to the file, to a version we term version $v'$
- `scm commit`
- `scm revert`
- Verify that the version of the file is now restored to the earlier, version $v$