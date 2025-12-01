---
title: SCM
---

# Announcements

- Source Control Management
  - LCS / `diff` ongoing
  - Hash Trees covered, not yet deployed
  - A Pythonic (ew!) [reference solution](https://github.com/cd-c89/scmpy/tree/main).
    
## Today

- Requirements
    - [ ] `commit`
    - [ ] `revert`
- Nice-to-haves
    - [ ] `viewer`
    - [ ] `scrape`

## Never    

- Extensions
    - Hashing
    - Signatures
    - Branches

## Git Example
    
```{.sh}
$ tree .git
.git
├── COMMIT_EDITMSG
├── HEAD
├── branches
├── config
├── description
├── hooks
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── fsmonitor-watchman.sample
│   ├── post-update.sample
│   ├── pre-applypatch.sample
│   ├── pre-commit.sample
│   ├── pre-merge-commit.sample
│   ├── pre-push.sample
│   ├── pre-rebase.sample
│   ├── pre-receive.sample
│   ├── prepare-commit-msg.sample
│   ├── push-to-checkout.sample
│   └── update.sample
├── index
├── info
│   └── exclude
├── logs
│   ├── HEAD
│   └── refs
│       ├── heads
│       │   └── main
│       └── remotes
│           └── origin
│               ├── HEAD
│               └── main
├── objects
│   ├── 14
│   │   └── 699a133ae84e6c922ca69ffa74d4df47eae49f
│   ├── 4b
│   │   └── 41ec9ea0317e27beac7c2d77945e542c26f943
│   ├── a3
│   │   └── 1c05f02ab1855a2f7e420ee0f5b28c2d8c1008
│   ├── b9
│   │   └── 1bf6a71c95a125d9e0cd59e1149ad022b8baeb
│   ├── info
│   └── pack
│       ├── pack-6fbf46b3e979d9d021e11db53f6959e1178cbd97.idx
│       └── pack-6fbf46b3e979d9d021e11db53f6959e1178cbd97.pack
├── packed-refs
└── refs
    ├── heads
    │   └── main
    ├── remotes
    │   └── origin
    │       ├── HEAD
    │       └── main
    └── tags

20 directories, 33 files
```

- "Everything is a file" - Linux

## Counter proposal

- Via `./scm.py viewer`

```{.json}
{
  "latest": {
    "/home/user/tmp/scmpy/scm.py": [
      "#!/usr/bin/env python3",
      "",
      "import os, sys, json, subprocess, difflib",
      "",
      "SCM_NAME = \".scm\"",
      "DIFF_NAME = \".diff\"",
      "",
      "# diff helper",
      "diff_lines = lambda ls_0, ls_1: [line.rstrip() for line in list(difflib.unified_diff(ls_0, ls_1))]",
      "",
      "# saves current version to .scm",
      "def commit():",
      "    # Get all files that aren't hidden",
      "    tree = [node for node in os.walk(os.getcwd()) if \".\" not in node[0]]",
      "    fs = [os.path.join(node[0], n) for node in tree for n in node[2] if n[0] != \".\"]",
      "",
      "    # Get or create .scm file",
      "    if not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0:",
      "        # create",
      "        latest = {f: open(f).read().splitlines() for f in fs}",
      "        json.dump(",
      "            {\"latest\": latest, \"commit\": [{\"init\": latest, \"diff\": {}}]},",
      "            open(SCM_NAME, \"w\"),",
      "        )",
      "    else:",
      "        # get",
      "        scm = json.loads(open(SCM_NAME, \"r\").read())",
      "        late = scm[\"latest\"]",
      "        curr = scm[\"commit\"]",
      "        old_fs = [f for f in curr[-1][\"init\"]] + [f for f in curr[-1][\"diff\"]]",
      "        new_fs = [f for f in fs if fs not in old_fs]",
      "        init = {f: open(f).read().splitlines() for f in new_fs if f not in old_fs}",
      "        # We use unified diff from difflib since it still works with patch.",
      "        diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}",
      "        scm[\"latest\"] = {f: open(f).read().splitlines() for f in fs}",
      "        scm[\"commit\"].append({\"init\": init, \"diff\": diff})",
      "        json.dump(scm, open(SCM_NAME, \"w\"))",
      "",
      "",
      "# pops latest without caching.",
      "# not gonna ether novel files, that seems pointless?",
      "def scrape():",
      "    (not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0) and exit()",
      "    [",
      "        open(k, \"w\").write(\"\\n\".join(v))",
      "        for k, v in json.loads(open(SCM_NAME, \"r\").read())[\"latest\"].items()",
      "    ]",
      "",
      "",
      "# let's just roll back one, that's logically equivalent",
      "def revert():",
      "    scrape()",
      "    scm = json.loads(open(SCM_NAME, \"r\").read())",
      "    late = scm[\"latest\"]",
      "    curr = scm[\"commit\"]",
      "    len(curr) < 2 and exit()",
      "    last = curr.pop()[\"diff\"]",
      "    for k, v in last.items():",
      "        open(DIFF_NAME, \"w\").write(\"\\n\".join(v))",
      "        os.system(\"patch -R \" + k + \" \" + DIFF_NAME)",
      "    json.dump(scm, open(SCM_NAME, \"w\"))",
      "",
      "viewer = lambda: os.system(",
      "    \"jq . .scm\"",
      ")  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))",
      "",
      "# Trivial Comment",
      "",
      "# Another",
      "",
      "__name__ == \"__main__\" and len(sys.argv) == 2 and {",
      "    \"commit\": commit,",
      "    \"scrape\": scrape,",
      "    \"revert\": revert,",
      "    \"viewer\": viewer,",
      "}[sys.argv[1]]()",
      ""
    ],
    "/home/user/tmp/scmpy/scm.py.orig": [
      "#!/usr/bin/env python3",
      "",
      "import os, sys, json, subprocess, difflib",
      "",
      "SCM_NAME = \".scm\"",
      "DIFF_NAME = \".diff\"",
      "",
      "# diff helper",
      "diff_lines = lambda ls_0, ls_1: [line.rstrip() for line in list(difflib.unified_diff(ls_0, ls_1))]",
      "",
      "# saves current version to .scm",
      "def commit():",
      "    # Get all files that aren't hidden",
      "    tree = [node for node in os.walk(os.getcwd()) if \".\" not in node[0]]",
      "    fs = [os.path.join(node[0], n) for node in tree for n in node[2] if n[0] != \".\"]",
      "",
      "    # Get or create .scm file",
      "    if not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0:",
      "        # create",
      "        latest = {f: open(f).read().splitlines() for f in fs}",
      "        json.dump(",
      "            {\"latest\": latest, \"commit\": [{\"init\": latest, \"diff\": {}}]},",
      "            open(SCM_NAME, \"w\"),",
      "        )",
      "    else:",
      "        # get",
      "        scm = json.loads(open(SCM_NAME, \"r\").read())",
      "        late = scm[\"latest\"]",
      "        curr = scm[\"commit\"]",
      "        old_fs = [f for f in curr[-1][\"init\"]] + [f for f in curr[-1][\"diff\"]]",
      "        new_fs = [f for f in fs if fs not in old_fs]",
      "        init = {f: open(f).read().splitlines() for f in new_fs if f not in old_fs}",
      "        # We use unified diff from difflib since it still works with patch.",
      "        diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}",
      "        scm[\"latest\"] = {f: open(f).read().splitlines() for f in fs}",
      "        scm[\"commit\"].append({\"init\": init, \"diff\": diff})",
      "        json.dump(scm, open(SCM_NAME, \"w\"))",
      "",
      "",
      "# pops latest without caching.",
      "# not gonna ether novel files, that seems pointless?",
      "def scrape():",
      "    (not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0) and exit()",
      "    [",
      "        open(k, \"w\").write(\"\\n\".join(v))",
      "        for k, v in json.loads(open(SCM_NAME, \"r\").read())[\"latest\"].items()",
      "    ]",
      "",
      "",
      "# let's just roll back one, that's logically equivalent",
      "def revert():",
      "    scrape()",
      "    scm = json.loads(open(SCM_NAME, \"r\").read())",
      "    late = scm[\"latest\"]",
      "    curr = scm[\"commit\"]",
      "    len(curr) < 2 and exit()",
      "    last = curr.pop()[\"diff\"]",
      "    for k, v in last.items():",
      "        open(DIFF_NAME, \"w\").write(\"\\n\".join(v))",
      "        os.system(\"patch -R \" + k + \" \" + DIFF_NAME)",
      "",
      "",
      "viewer = lambda: os.system(",
      "    \"jq . .scm\"",
      ")  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))",
      "",
      "__name__ == \"__main__\" and len(sys.argv) == 2 and {",
      "    \"commit\": commit,",
      "    \"scrape\": scrape,",
      "    \"revert\": revert,",
      "    \"viewer\": viewer,",
      "}[sys.argv[1]]()",
      ""
    ]
  },
  "commit": [
    {
      "init": {
        "/home/user/tmp/scmpy/scm.py": [
          "#!/usr/bin/env python3",
          "",
          "import os, sys, json, subprocess, difflib",
          "",
          "SCM_NAME = \".scm\"",
          "DIFF_NAME = \".diff\"",
          "",
          "# diff helper",
          "diff_lines = lambda ls_0, ls_1: [line.strip() for line in list(difflib.unified_diff(ls_0, ls_1))]",
          "",
          "# saves current version to .scm",
          "def commit():",
          "    # Get all files that aren't hidden",
          "    tree = [node for node in os.walk(os.getcwd()) if \".\" not in node[0]]",
          "    fs = [os.path.join(node[0], n) for node in tree for n in node[2] if n[0] != \".\"]",
          "",
          "    # Get or create .scm file",
          "    if not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0:",
          "        # create",
          "        latest = {f: open(f).read().splitlines() for f in fs}",
          "        json.dump(",
          "            {\"latest\": latest, \"commit\": [{\"init\": latest, \"diff\": {}}]},",
          "            open(SCM_NAME, \"w\"),",
          "        )",
          "    else:",
          "        # get",
          "        scm = json.loads(open(SCM_NAME, \"r\").read())",
          "        late = scm[\"latest\"]",
          "        curr = scm[\"commit\"]",
          "        old_fs = [f for f in curr[-1][\"init\"]] + [f for f in curr[-1][\"diff\"]]",
          "        new_fs = [f for f in fs if fs not in old_fs]",
          "        init = {f: open(f).read().splitlines() for f in new_fs if f not in old_fs}",
          "        # We use unified diff from difflib since it still works with patch.",
          "        diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}",
          "        scm[\"latest\"] = {f: open(f).read().splitlines() for f in fs}",
          "        scm[\"commit\"].append({\"init\": init, \"diff\": diff})",
          "        print(diff)",
          "        json.dump(scm, open(SCM_NAME, \"w\"))",
          "",
          "",
          "# pops latest without caching.",
          "# not gonna ether novel files, that seems pointless?",
          "def scrape():",
          "    (not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0) and exit()",
          "    [",
          "        open(k, \"w\").write(\"\\n\".join(v))",
          "        for k, v in json.loads(open(SCM_NAME, \"r\").read())[\"latest\"].items()",
          "    ]",
          "",
          "",
          "# let's just roll back one, that's logically equivalent",
          "def revert():",
          "    scrape()",
          "    scm = json.loads(open(SCM_NAME, \"r\").read())",
          "    late = scm[\"latest\"]",
          "    curr = scm[\"commit\"]",
          "    len(curr) < 2 and exit()",
          "    last = curr.pop()[\"diff\"]",
          "    for k, v in last.items():",
          "        open(DIFF_NAME, \"w\").write(\"\\n\".join(v))",
          "        os.system(\"patch -R \" + k + \" \" + DIFF_NAME)",
          "",
          "",
          "viewer = lambda: os.system(",
          "    \"jq . .scm\"",
          ")  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))",
          "",
          "__name__ == \"__main__\" and len(sys.argv) == 2 and {",
          "    \"commit\": commit,",
          "    \"scrape\": scrape,",
          "    \"revert\": revert,",
          "    \"viewer\": viewer,",
          "}[sys.argv[1]]()"
        ]
      },
      "diff": {}
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -71,3 +71,5 @@",
          "\"revert\": revert,",
          "\"viewer\": viewer,",
          "}[sys.argv[1]]()",
          "+",
          "+# Trivial Comment"
        ]
      }
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -6,7 +6,7 @@",
          " DIFF_NAME = \".diff\"",
          "",
          " # diff helper",
          "-diff_lines = lambda ls_0, ls_1: [line.strip() for line in list(difflib.unified_diff(ls_0, ls_1))]",
          "+diff_lines = lambda ls_0, ls_1: [line.rstrip() for line in list(difflib.unified_diff(ls_0, ls_1))]",
          "",
          " # saves current version to .scm",
          " def commit():"
        ]
      }
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -34,7 +34,6 @@",
          "         diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}",
          "         scm[\"latest\"] = {f: open(f).read().splitlines() for f in fs}",
          "         scm[\"commit\"].append({\"init\": init, \"diff\": diff})",
          "-        print(diff)",
          "         json.dump(scm, open(SCM_NAME, \"w\"))",
          "",
          ""
        ]
      }
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -70,5 +70,3 @@",
          "     \"revert\": revert,",
          "     \"viewer\": viewer,",
          " }[sys.argv[1]]()",
          "-",
          "-# Trivial Comment"
        ]
      }
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -70,3 +70,7 @@",
          "     \"revert\": revert,",
          "     \"viewer\": viewer,",
          " }[sys.argv[1]]()",
          "+",
          "+# Trivial Comment",
          "+",
          "+"
        ]
      }
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -71,6 +71,5 @@",
          "     \"viewer\": viewer,",
          " }[sys.argv[1]]()",
          "",
          "-# Trivial Comment",
          "",
          ""
        ]
      }
    },
    {
      "init": {
        "/home/user/tmp/scmpy/scm.py.orig": [
          "#!/usr/bin/env python3",
          "",
          "import os, sys, json, subprocess, difflib",
          "",
          "SCM_NAME = \".scm\"",
          "DIFF_NAME = \".diff\"",
          "",
          "# diff helper",
          "diff_lines = lambda ls_0, ls_1: [line.rstrip() for line in list(difflib.unified_diff(ls_0, ls_1))]",
          "",
          "# saves current version to .scm",
          "def commit():",
          "    # Get all files that aren't hidden",
          "    tree = [node for node in os.walk(os.getcwd()) if \".\" not in node[0]]",
          "    fs = [os.path.join(node[0], n) for node in tree for n in node[2] if n[0] != \".\"]",
          "",
          "    # Get or create .scm file",
          "    if not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0:",
          "        # create",
          "        latest = {f: open(f).read().splitlines() for f in fs}",
          "        json.dump(",
          "            {\"latest\": latest, \"commit\": [{\"init\": latest, \"diff\": {}}]},",
          "            open(SCM_NAME, \"w\"),",
          "        )",
          "    else:",
          "        # get",
          "        scm = json.loads(open(SCM_NAME, \"r\").read())",
          "        late = scm[\"latest\"]",
          "        curr = scm[\"commit\"]",
          "        old_fs = [f for f in curr[-1][\"init\"]] + [f for f in curr[-1][\"diff\"]]",
          "        new_fs = [f for f in fs if fs not in old_fs]",
          "        init = {f: open(f).read().splitlines() for f in new_fs if f not in old_fs}",
          "        # We use unified diff from difflib since it still works with patch.",
          "        diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}",
          "        scm[\"latest\"] = {f: open(f).read().splitlines() for f in fs}",
          "        scm[\"commit\"].append({\"init\": init, \"diff\": diff})",
          "        json.dump(scm, open(SCM_NAME, \"w\"))",
          "",
          "",
          "# pops latest without caching.",
          "# not gonna ether novel files, that seems pointless?",
          "def scrape():",
          "    (not os.path.isfile(SCM_NAME) or os.path.getsize(\".scm\") == 0) and exit()",
          "    [",
          "        open(k, \"w\").write(\"\\n\".join(v))",
          "        for k, v in json.loads(open(SCM_NAME, \"r\").read())[\"latest\"].items()",
          "    ]",
          "",
          "",
          "# let's just roll back one, that's logically equivalent",
          "def revert():",
          "    scrape()",
          "    scm = json.loads(open(SCM_NAME, \"r\").read())",
          "    late = scm[\"latest\"]",
          "    curr = scm[\"commit\"]",
          "    len(curr) < 2 and exit()",
          "    last = curr.pop()[\"diff\"]",
          "    for k, v in last.items():",
          "        open(DIFF_NAME, \"w\").write(\"\\n\".join(v))",
          "        os.system(\"patch -R \" + k + \" \" + DIFF_NAME)",
          "",
          "",
          "viewer = lambda: os.system(",
          "    \"jq . .scm\"",
          ")  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))",
          "",
          "__name__ == \"__main__\" and len(sys.argv) == 2 and {",
          "    \"commit\": commit,",
          "    \"scrape\": scrape,",
          "    \"revert\": revert,",
          "    \"viewer\": viewer,",
          "}[sys.argv[1]]()",
          "",
          ""
        ]
      },
      "diff": {
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -58,7 +58,7 @@",
          "     for k, v in last.items():",
          "         open(DIFF_NAME, \"w\").write(\"\\n\".join(v))",
          "         os.system(\"patch -R \" + k + \" \" + DIFF_NAME)",
          "-",
          "+    json.dump(scm, open(SCM_NAME, \"w\"))",
          "",
          " viewer = lambda: os.system(",
          "     \"jq . .scm\"",
          "@@ -71,5 +71,5 @@",
          "     \"viewer\": viewer,",
          " }[sys.argv[1]]()",
          "",
          "+# Trivial Comment",
          "",
          "-"
        ]
      }
    },
    {
      "init": {},
      "diff": {
        "/home/user/tmp/scmpy/scm.py.orig": [
          "---",
          "+++",
          "@@ -71,4 +71,3 @@",
          "     \"viewer\": viewer,",
          " }[sys.argv[1]]()",
          "",
          "-"
        ],
        "/home/user/tmp/scmpy/scm.py": [
          "---",
          "+++",
          "@@ -64,6 +64,8 @@",
          "     \"jq . .scm\"",
          " )  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))",
          "",
          "+# Trivial Comment",
          "+",
          " __name__ == \"__main__\" and len(sys.argv) == 2 and {",
          "     \"commit\": commit,",
          "     \"scrape\": scrape,",
          "@@ -71,9 +73,3 @@",
          "     \"viewer\": viewer,",
          " }[sys.argv[1]]()",
          "",
          "-# Trivial Comment",
          "-",
          "-# Another",
          "-",
          "-",
          "-"
        ]
      }
    }
  ]
}
```

## Design Decision

> Decide whether you want to navigate a file system and crush text and be rad as heck, or learn `serde`, toss everything in a single file, and be cool as heck

- I liked JSON a lot for this, but there's no question there's benefits to using the file system!
    - But... what if you *don't have a file system* (is that CS-371: Operating Systems' theme?)
    
## Aside: Python

- Python is cringe or bad or whatever, I just used a language you knew to give a reference that is "self-documentating".
- It also makes a few system calls, directly using `patch` for example (this will probably explode on Windows, which is a you-problem).

## Python Quality

- I also put some effort into making the Python "look like Python" so all examples here are:
    - Open source.
    - Licensed GPLv3 (ask me after class)
    - [`black`](https://github.com/psf/black) formatted.
    
## Differences
    
- You shouldn't use system calls like `patch`
    - Those aren't written in Rust, and therefore we can't use them.
- You are writing actually usable code and should use a license and `cargo fmt`
    - You'll see why formatting is so nice as soon as you start looking a SCM diffs!

# Requirements

## An SCM

> [Version control (also known as revision control, source control, and source code management) is the software engineering practice of controlling, organizing, and tracking different versions in history of computer files; primarily source code text files, but generally any type of file.](https://en.wikipedia.org/wiki/Version_control)

## A Minimal SCM

> Version control includes options to view old versions and to revert a file to a previous version. 

- For the final, we implement an SCM that does two things:
    - Saves old versions of files, somehow
    - Can "roll back" changes to files to older versions.
    - Provides some form of visibility into past files
    
## My terminology

- I use the following verbs, ish, to describe these:
    - `commit` saves the current version of the files under control/management
    - `revert` overwrites the *current* version with the *previous* version.
- I am not a pretty-print enthusiast and simply dump JSON unaltered to meet the "visibility" requirement.
    - This can be a fun thing to extend to look nicer if you want!
    - Check out e.g. `git log`
    
## My Commit

- Read every non-hidden (non-`.` prefixed) file and folder in the current path, recursively.
- Check to see if the system is already under version control by checking for a `.scm` file
    - In the case the file (vs. JSON) implementation, this would be a folder, like `.git`
- Either create a JSON file containing all file contents if `.scm` does not exist, or
- Append a diff to the JSON file for every change.
    
## Design Decisions

- This is not a `git commit`!
- Git has both `init` and `add` - I use neither
    - The first time commit is called, it runs an initializer instead of a standard commit.
    - All files are automatically included.
- You don't have to do either of these, but should probably provide an alias to similar to `./scm.py commit` just to test equivalencies.

## Get All Files

- I didn't even initially include commit in a function since it was the first thing I wrote!
- But now, it starts like this:

```{.py filename="scm.py"}
# Get all files that aren't hidden
tree = [node for node in os.walk(os.getcwd()) if "." not in node[0]]
fs = [os.path.join(node[0], n) for node in tree for n in node[2] if n[0] != "."]
```

- `fs` is the Python list (so a Rust `Vec`) that contains the *full paths* as strings of all non-hidden files, recursively.
    - Recursively means current directory and any sub-directories.
    
## Cases

- I quickly check the file system for the presence of a hidden `.scm` file (or folder) which I use to save versions.

```{.py filename="scm.py"}
if not os.path.isfile(SCM_NAME) or os.path.getsize(".scm") == 0:
```

- You'll figure out in testing why you need this, and also why it is worthwhile to test if a file exists but is of size zero.
    - Any bad code between file opening and writing well-formed JSON will be very annoying.
- I'd expect a Rust `match` here, but you do you!

## Aside: `.scm`

- Git's hidden cache is called `.git`
- You don't have to call your SCM `scm`
- I just had two globals I used so it was easy to change:

```{.py filename="scm.py"}
SCM_NAME = ".scm"
DIFF_NAME = ".diff"
```

- Obviously the code explodes if anything else uses those names, but `git` gets away with it, so...

## Initializing

- Initializing was straightforward.
- Rip every file, I did into lists of lines (prints out better) and slam it into a Python dictionary (so a Rust `HashMap` or a `serde_json::Map`)
- Then dump to the JSON formatted `.scm` file.

```{.py filename="scm.py"}
latest = {f: open(f).read().splitlines() for f in fs}
json.dump(
    {"latest": latest, "commit": [{"init": latest, "diff": {}}]},
    open(SCM_NAME, "w"),
)
```

## Subleties

- I do two things here that make more sense as you get further in the project:
    - I create a "latest" key, which stores the most recent `commit`ed version of all files.
    - I *separately* create a "commit" key, which stores a JSON array (so a Python list or Rust `Vec`)
        - This list contains itself an "init" key, for new files, and a "diff" key, for changed files.
- Think about why you would want to get these things separate!

## Accessing `.scm`

- Once some commit has been made, latter submits require appending to the JSON file.
    - Which of course I do by completely overwriting it, because that is easier.
- First I read it in a slice it up.
```{.py filename="scm.py"}
scm = json.loads(open(SCM_NAME, "r").read())
late = scm["latest"]
curr = scm["commit"]
```
- Hard to understate how much nicer it is to allow yourself some niceties like caching the latest files.

## Checking for files

- At this point, I already determined `fs` - the current eligible files.
- I also check:
    - What files are already under version control, and
    - Which ones aren't.
    
```{.py filename="scm.py"}
old_fs = [f for f in curr[-1]["init"]] + [f for f in curr[-1]["diff"]]
new_fs = [f for f in fs if fs not in old_fs]
```

## Aside: Diff

- The `diff` I like can't be used gracefully from Python.
    - Either `diff` in a `subprocess.check_output`, or
    - Use `difflib` which makes unified diffs.
- I did this, which you will not and should not do - use your own Rust code from class.
```{.py filename="scm.py"}
diff_lines = lambda ls_0, ls_1: [line.rstrip() for line in list(difflib.unified_diff(ls_0, ls_1))]
```
- When you look at the `.scm` files in that repository, the diffs are `-u` diffs, and may appear "messy"

## Aside: `\n`

- If you play around with `scm.py` it will explode if you don't have an empty line at the end of your file.
- The combination of `difflib` and `patch` can't handle files that end without a trailing new line.
- This is bad, and your SCM should not contain this bug (and I don't think it will if you do all the steps properly).
    - (Do check)
    
## Build `.scm`

- Put all the `diff` in a JSON object / Python Dictionary / Rust `HashMap` / `serde_json::Map`
- Overwrite "latest"'s value with all the new versions.
    - We can get the old ones back since we have the diffs.
- Append a entry to "commit" containing an "init" and "diff", either of which may be empty.

```{.py filename="scm.py"}
diff = {f: diff_lines(late[f], open(f).read().splitlines()) for f in old_fs}
scm["latest"] = {f: open(f).read().splitlines() for f in fs}
scm["commit"].append({"init": init, "diff": diff})
```

## Update `.scm`

- Write to `.scm` using your preferred JSON library...
    - Or do some shenanigans with text files and a nested file system if you are Git-like.
- Manage all your files appropriately and gracefully exit.

```{.py filename="scm.py"}
json.dump(scm, open(SCM_NAME, "w"))
```

- Oh and save your work - I did so using `git commit` - since you will explode your code all the time.

## My Revert

- My revert had a dependencies on a nicety, so I will do niceties than return to revert.

## Today


- Requirements
    - [x] `commit`
    - [ ] `revert`
- Nice-to-haves
    - [ ] `viewer`
    - [ ] `scrape`
    
# Niceties

## My scrape

- When I write code, a lot of times I write bad code.
    - So I delete it.
- This is easier if you happen to working under control/management and can just type `./scm.py scrape` and get back the latest good version.
    - I think of it as "scraping off" my honk-honk-silly-goose era.
- If you aren't doing it already, this could change your life!

## Dependency

- It also so happens that to successfully apply a diff, you need to do so against one of the two files that are, well, `diff`'ed.
- The current file version isn't necessarily one of those!
- So keep track of a file version that that can receive a diff, so you can go back further than to the latest commit!

## Easy-mode

- I just open `.scm`, and unconditionally write everything in "latest" to the file system.
- It's a single (`black`-exploded) line.
    - I do add a gracefully exit if there's been no commit yet.

```{.py filename="scm.py"}
(not os.path.isfile(SCM_NAME) or os.path.getsize(".scm") == 0) and exit()
[
    open(k, "w").write("\n".join(v))
    for k, v in json.loads(open(SCM_NAME, "r").read())["latest"].items()
]
```

## Recall

- I'm not actually saving block text, I'm only saving lines.
- So when I write to file, I rebuild the text blocks by combining lines with intermediate new-lines.
```{.py filename="scm.py"}
"\n".join(v) # v was "value" - the JSON array of strings (lines)
```
- This is mildly annoying but makes the JSON easier to read, so I did it.
- I highlight this as an example of how you should make your own choices.

## Design Decision

- This would be quite difficult (as in your would be recursively applying diffs along the entirety of the `.scm` file) if you did not keep "latest" around.
- Work smart not hard!

## Today


- Requirements
    - [x] `commit`
    - [ ] `revert`
- Nice-to-haves
    - [ ] `viewer`
    - [x] `scrape`
    
# Requirements

## My Revert

- Revert isn't too bad once you have a scraper.
    - Scrape, then...
    - Look at the most recent commit, and
    - Look at all its diffs, then
    - Apply them all reverse style (`patch -R`)
    - Pop that commit off the JSON array and rewrite `.scm`
        - That is, destroy all traces.
        - (You can keep traces; I didn't want to)

## Get started

- Scrape and open `.scm`

```{.py filename="scm.py"}
scrape()
scm = json.loads(open(SCM_NAME, "r").read())
late = scm["latest"]
curr = scm["commit"]
```

## Case handling

- By the way, you can't revert if you only have one commit.
    - Think about why not!
    
```{.py filename="scm.py"}
len(curr) < 2 and exit()
```

- In general, make some effort to use your SCM as you write it to find this fun little corner cases.


## Pop a commit

- I didn't destroy any new files.
- Hard to care about that. Maybe I should?
- So I just look at the "diff" values only, and destructive update the "commit" JSON array.

```{.py filename="scm.py"}
last = curr.pop()["diff"]
```

- This contains all we need to go back in time.

## This is gross

- I don't think there's a baseline Python `patch` so I had to hack a bit.
- I throw the diff into the filesystem, use `os.system` to call `patch`, then clean up latter.
- This is bad, don't do this, write `patch` in Rust.
    - It is *very close* to diff!
    
```{.py filename="scm.py"}
for k, v in last.items():
    open(DIFF_NAME, "w").write("\n".join(v))
    os.system("patch -R " + k + " " + DIFF_NAME)
```

## Clean up

- Rewrite `.scm`, remove `.diff`, and exit gracefully.

```{.py filename="scm.py"}
json.dump(scm, open(SCM_NAME, "w"))
os.delete(DIFF_NAME)
```

## Understanding check

- My revert is wrong and puts the SCM into an unstable state.
- How?

## Answer

- I don't rewrite "latest" after a revert!
    - I forgot this and didn't uncover it in testing!
    - Test your code!
    - I just noticed when writing these slides!
- [Read me](https://github.com/cd-c89/scmpy/issues/1)

## Hint

- The code to fix this already exists in `scm.py`
- It should be factored!

## Today

- Requirements
    - [x] `commit`
    - [x] `revert`
- Nice-to-haves
    - [ ] `viewer`
    - [x] `scrape`
    
# Niceties

## My Viewer

- I don't think pretty-print is interesting, but...
- We did play around with it a bit on Wordle, and it can be fun.
- Engage at your own discretion.
- Just got tired of using `python3 -m json-tool` and it was ugly so I played around a bit.

## I just use `jq`

- I hear just about every system has `jq` on it.

```{.py filename="scm.py"}
viewer = lambda: os.system(
    "jq . .scm"
)  # print(json.dumps(json.load(open(SCM_NAME)), indent=4))
```

- And if not I just used `json`, so
- Anyways, if you don't use JSON, you have to write something yourself.
    - It must show what a previous version would look like, some how.
    
## `git show --stat`

- I don't love this.
    - Can't tell *what* the changes are, but...
    - It is good enough if you don't go the JSON route.

```{.sh}
$ git show --stat
commit 9b1cd0fc410b50a25370b5bcaa57ceb407e51bff (HEAD -> main, origin/main, origin/HEAD)
Author: c <ckdeutschbein@willamette.edu>
Date:   Sat Nov 29 12:44:40 2025 -0800

    think this is good enough

 .scm   | 2 +-
 scm.py | 8 ++++----
 2 files changed, 5 insertions(+), 5 deletions(-)
```

## Minimal

- First 3 lines are of course hash stuff, and now optional.
- Next line is a commit message, which I didn't require (or even support, though it would be trivial to do so)
- This would be fine for the final.

```{.sh}
$ ./scm viewer # assuming you name your binary `scm`
.scm   | 2 +-
scm.py | 8 ++++----
```

## Today

- Requirements
    - [x] `commit`
    - [x] `revert`
- Nice-to-haves
    - [x] `viewer`
    - [x] `scrape`