# Claude Code, Bash and Git - beginner cheat sheet

For delegates on **Practical AI for Actuaries**. The Markdown and PDF are generated from the same command lists. Copy terminal commands from this Markdown file so every command stays on one unbroken line.

## Page 1 - Useful Claude Code commands

| Command | What it does | Example |
|---|---|---|
| `/help` | Show available commands and help. | `/help` |
| `/model` | View or change the Claude model. | `/model` |
| `/context` | Show what is using the context window. | `/context` |
| `/compact` | Summarise the conversation to free context space. | `/compact Keep the agreed requirements` |
| `/clear` | Start a fresh conversation in this terminal. | `/clear` |
| `/resume` | Reopen an earlier Claude Code conversation. | `/resume` |
| `/permissions` | Review or change tool permissions. | `/permissions` |
| `/memory` | Open Claude Code memory files. | `/memory` |
| `! command` | Run Bash without leaving Claude Code. | `! git status` |

### Essential controls

| Keys or syntax | Use |
|---|---|
| `Ctrl+C` | Interrupt the current response or command; again at the idle prompt exits Claude Code. |
| `Ctrl+D or /exit` | Exit Claude Code cleanly. |
| `Esc` | Interrupt Claude while it is working. |
| `Esc twice` | Open rewind options for earlier conversation or code state. |
| `Ctrl+Z` | Suspend a Unix/WSL process; beginners should normally avoid it. |
| `@path/to/file` | Add a file or folder to the prompt. |
| `/btw question` | Ask a side question without adding it to the main conversation. |
| `Ctrl+B` | Move a running Bash task to the background. |

### Scheduling in Claude Code

These work only while that Claude Code session remains open. Scheduled tasks expire after seven days.

```text
/loop 5m check whether the tests have finished
```

```text
/schedule review open pull requests every weekday at 9am
```

Ask Claude in ordinary language to list or cancel scheduled tasks.

<div style="page-break-after: always;"></div>

## Page 2 - Useful Bash commands

| Command | What it does | Example |
|---|---|---|
| `pwd` | Show the current folder. | `pwd` |
| `ls` | List files; -l adds detail and -a includes hidden files. | `ls -la` |
| `cd` | Change to another folder. | `cd docs` |
| `cd -` | Return to the directory you were in immediately before. | `cd -` |
| `mkdir` | Create a new folder. | `mkdir outputs` |
| `touch` | Create an empty file or update an existing file's timestamp. | `touch notes.txt` |
| `echo` | Display text or send it into a file using > or >>. | `echo "Hello"` |
| `cat` | Display a small text file. | `cat README.md` |
| `grep` | Search for text inside a file. | `grep -n "premium" report.md` |
| `code` | Open a file or folder in VS Code. | `code .` |
| `nano` | Open a simple terminal text editor. | `nano notes.txt` |
| `cp` | Copy a file; use -r to copy a folder. | `cp report.md backup.md` |
| `mv` | Move or rename a file or folder. | `mv draft.md final.md` |
| `rm` | Permanently delete a file. | `rm old_notes.txt` |
| `pushd` | Save the current directory and move to another one. | `pushd docs` |
| `popd` | Return to the directory saved by pushd. | `popd` |
| `dirs -v` | Show the numbered directory stack used by pushd/popd. | `dirs -v` |

### Directory navigation

- `cd -` switches between your current directory and the directory you were in immediately before.
- `pushd docs` saves the current directory on a stack and moves to `docs`.
- `dirs -v` displays that stack with numbered entries.
- `popd` removes the top entry and returns to the saved directory.

### Paths and spaces

Put quotes around a path containing spaces:

```bash
cd "My Documents/project"
```

Use `/` in Git Bash paths. If `code` is not recognised, reinstall VS Code with **Add to PATH** selected. If `nano` is unavailable, use `code filename`.

### Danger: recursive deletion

```bash
rm -rf folder_name
```

This permanently deletes the folder and everything inside it without using the Recycle Bin. Check `pwd` and `ls` first. Never use `rm -rf` with a blank, uncertain, broad or copied path.

<div style="page-break-after: always;"></div>

## Page 3 - Useful Git commands

| Command | What it does | Example |
|---|---|---|
| `git clone URL` | Download a repository into a new folder, usually once. | `git clone https://github.com/example/project.git` |
| `git status` | Show changed, staged and untracked files. | `git status` |
| `git remote -v` | Show the remote repository addresses. | `git remote -v` |
| `git branch --show-current` | Show the name of the current branch. | `git branch --show-current` |
| `git pull` | Fetch, then integrate by merge or configured rebase. | `git pull` |
| `git fetch` | Download remote information without changing working files. | `git fetch` |
| `git log HEAD..origin/main --oneline` | Inspect new remote commits before integrating. | `git log HEAD..origin/main --oneline` |
| `git diff HEAD..origin/main` | Inspect remote line changes before integrating. | `git diff HEAD..origin/main` |
| `git merge origin/main` | Integrate fetched remote main after inspection. | `git merge origin/main` |
| `git diff` | Review unstaged line-by-line changes. | `git diff` |
| `git add FILE` | Stage one selected file for the next commit. | `git add report.md` |
| `git commit -m "message"` | Record staged changes with a meaningful message. | `git commit -m "Update report"` |
| `git log --oneline` | Show a compact commit history. | `git log --oneline -10` |
| `git switch -c NAME` | Create a new branch and switch to it. | `git switch -c update-report` |
| `git push` | Publish commits to the tracked remote branch. | `git push` |

### Inspect before integrating

```bash
git fetch
git log HEAD..origin/main --oneline
git diff HEAD..origin/main
git merge origin/main
```

Replace `main` if the remote branch has a different name. A normal `git pull` combines fetching and integration; Git may merge or rebase depending on its configuration.

### First push

Check the current branch before using `main`:

```bash
git branch --show-current
git push -u origin main
```

If the branch is not `main`, substitute its actual name. After the upstream is set, plain `git push` is normally sufficient.

### Safe everyday sequence

```bash
git status
git pull
# edit files
git diff
git add report.md
git status
git commit -m "Describe the change"
git push
```

Prefer `git add filename` while learning. `git add .` may stage files you did not intend to commit.

## Official references

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/overview)
- [GNU Bash directory stack](https://www.gnu.org/software/bash/manual/html_node/Directory-Stack-Builtins.html)
- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [VS Code command-line interface](https://code.visualstudio.com/docs/editor/command-line)
- [Git command reference](https://git-scm.com/docs)
