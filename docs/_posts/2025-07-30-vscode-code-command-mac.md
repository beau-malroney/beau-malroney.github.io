---
layout: post
title: "Add VSCODE code to the command line on a Mac"
date: 2025-07-31
categories: [development, macOS, vscode]
tags: [code, vscode, visual studio code, visual studio, mac, homebrew, terminal]
---

## 🛠 Add VS Code `code` Command to macOS Terminal

If you're trying to run `code` in the terminal and see:

```bash
zsh: command not found: code
```

It means the VS Code command line tool isn’t in your PATH.

#### 1. Open VS Code

#### 2. Press `Cmd + Shift + P` to open the Command Palette

#### 3. Type and select:

```
Shell Command: Install 'code' command in PATH
```

You’ll see a message like:
> Shell command 'code' successfully installed in PATH.

#### 4. Run 
```
exec zsh
```

### 🧪 Test it

```bash
code .
```

This should open the current folder in VS Code.

You can also open a specific file using

```
code ./path-to-file
```

---