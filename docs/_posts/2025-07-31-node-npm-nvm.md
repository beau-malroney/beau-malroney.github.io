---
layout: post
title: "How to Install npm on a Mac"
date: 2025-07-31
categories: [development, macOS, node]
tags: [npm, nodejs, mac, homebrew, terminal]
---

If you're developing with JavaScript or Node.js on a Mac, you'll need `npm`, the Node Package Manager. Here's a quick guide to help you get started.

### 1. Install Homebrew (if you haven't yet)

Open your terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Node.js (npm comes with it)

```bash
brew install node
```

### 3. Verify the installation

```bash
node -v   # Outputs the Node.js version
npm -v    # Outputs the npm version
```

---

## Optional: Use `nvm` for Node Version Management

If you plan to work with multiple versions of Node.js, `nvm` (Node Version Manager) is a great tool.

### 1. Install `nvm`

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

After the installation, restart your terminal or run:

```bash
source ~/.nvm/nvm.sh
```

### 2. Install Node.js using `nvm`

```bash
nvm install node
```

### 3. Check versions

```bash
node -v   # Outputs the Node.js version
npm -v    # Outputs the npm version
```

---

## ⚠️ Avoid Using `sudo`

Do **not** use `sudo` to install Node.js or npm globally. It can lead to permission problems and messy environments. Stick with Homebrew or `nvm` for a clean setup.

---