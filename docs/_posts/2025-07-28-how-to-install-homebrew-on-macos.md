---
layout: post
title: "How to Install Homebrew on macOS"
date: 2025-07-28
categories: tutorial macos tools
tags: [homebrew, mac, terminal, package-manager]
description: "A simple step-by-step guide to installing Homebrew, the popular macOS package manager, using the Terminal."
keywords: "Homebrew, macOS, install Homebrew, package manager, Terminal, brew install"
author: "Beau Malroney"
robots: "index, follow"
canonical_url: "https://beau-malroney.github.io/2025-07-28-how-to-install-homebrew-on-macos"
---

Homebrew is the most popular package manager for macOS. It makes installing software easy and fast by handling all dependencies for you.

Here’s a step-by-step guide to install Homebrew on your Mac.

## Step 1: Open Terminal

Open the **Terminal** app on your Mac. You can find it in:

- Applications > Utilities > Terminal  
- Or press **Cmd + Space** and type “Terminal” to open Spotlight Search, then hit Enter.

## Step 2: Run the Homebrew Installation Command

Paste the following command into your Terminal and press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
This script will download and install Homebrew.

## Step 3: Follow On-Screen Instructions

You may be asked for your Mac user password (the one you use to log in).
The installer will download files and install the necessary components.
## Step 4: Add Homebrew to Your PATH

After installation, the script will output commands to add Homebrew to your shell environment. For example:

```
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```
Copy and paste these commands into your Terminal to ensure brew works properly.

## Step 5: Verify Your Installation

Run this command to check if Homebrew was installed correctly:

`brew --version`

You should see the version number printed, like this:
`Homebrew 4.3.0`

That’s it! You now have Homebrew installed on your Mac, ready to help you install software easily.

For example, you can install Node.js by running:

`brew install node`

Happy brewing! 🍺