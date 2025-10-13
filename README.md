# Farhost

Farhost is a lightweight, script-driven project that automates the installation and configuration of your development environment. With Farhost, you can quickly set up all the essential tools you need for development, including Homebrew, Ghostty Terminal, oh-my-zsh, powerlevel10k, nvm, Node.js, neovim, tmux, tpm, UV, Podman, and more.

## Features

- **Automated Setup:** Installs and configures a suite of development tools.
- **Environment Isolation:** Configures your setup within `~/.farhost` to keep your system organized.
- **Optional Backups:** Optionally backs up existing configuration files before linking new ones with the `-b` flag.
- **Customization Ready:** Easily extend or modify the installation process to suit your workflow.
- **One-Command Bootstrap:** Get started by executing a single command in your terminal.

## Tools Installed

Farhost installs and configures the following tools:

- **[Homebrew](https://brew.sh/):** The missing package manager for macOS (and Linux).
- **[Ghostty Terminal](https://ghostty.org/):** A modern, fast terminal emulator with custom configuration.
- **[oh-my-zsh](https://ohmyz.sh/):** A framework for managing your Zsh configuration.
- **[powerlevel10k](https://github.com/romkatv/powerlevel10k):** A fast and highly customizable Zsh theme.
- **[nvm](https://github.com/nvm-sh/nvm):** Node Version Manager.
- **[RVM](https://rvm.io/):** Ruby Version Manager.
- **[Ruby](https://www.ruby-lang.org/):** A dynamic, open source programming language with a focus on simplicity and productivity.
- **[Node.js](https://nodejs.org/):** A JavaScript runtime built on Chrome's V8 engine (latest version via NVM).
- **[neovim](https://neovim.io/):** A hyperextensible Vim-based text editor.
- **[tmux](https://github.com/tmux/tmux):** A terminal multiplexer.
- **[tpm](https://github.com/tmux-plugins/tpm):** Tmux Plugin Manager.
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package installer and resolver.
- **[Gemini](https://gemini.google.com/):** A powerful, multimodal AI model from Google.
- **[Podman Desktop](https://podman-desktop.io/):** A container management tool for developing and managing containers.
- **[Bruno](https://www.usebruno.com/):** A fast and Git-friendly open-source API client.
- **[Specify CLI](https://github.com/github/spec-kit):** A command-line interface for the GitHub Specification.

### Zsh Plugins

The setup includes the following Zsh plugins:

- **[zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions):** Fish-like autosuggestions for Zsh.
- **[zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting):** Syntax highlighting for Zsh.
- **[zsh-autocomplete](https://github.com/marlonrichert/zsh-autocomplete):** Real-time type-ahead completion for Zsh.
- **[fast-syntax-highlighting](https://github.com/zdharma-continuum/fast-syntax-highlighting):** Feature-rich syntax highlighting for Zsh.
- **[pyautoenv](https://github.com/hsaunders1904/pyautoenv):** Automatically activates Python virtual environments.
- **[zsh-vi-mode](https://github.com/jeffreytse/zsh-vi-mode):** Better Vi(m) mode plugin for Zsh.

## Installation

To install Farhost, run the following command in your terminal:

```bash
curl -s https://raw.githubusercontent.com/mikevive/farhost/refs/heads/main/setup.sh | bash
```

### Backup Flag

By default, the setup script will replace existing configuration files. To backup your existing configurations before linking new ones, use the `-b` flag:

```bash
./setup.sh -b
```

This will create timestamped backups of:
- `.zshrc`
- `.p10k.zsh`
- `.tmux.conf`
- Ghostty config folder (`~/.config/ghostty`)
- Neovim config folder (`~/.config/nvim`)

