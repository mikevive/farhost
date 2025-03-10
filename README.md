# Farhost

Farhost is a lightweight, script-driven project that automates the installation and configuration of your development environment. With Farhost, you can quickly set up all the essential tools you need for development, including Homebrew, Ghostty Terminal, oh-my-zsh, powerlevel10k, nvm, Node.js, neovim, tmux, tpm, Python, Poetry, pyenv, Docker, and more.

## Features

- **Automated Setup:** Installs and configures a suite of development tools.
- **Environment Isolation:** Configures your setup within `~/.farhost` to keep your system organized.
- **Customization Ready:** Easily extend or modify the installation process to suit your workflow.
- **One-Command Bootstrap:** Get started by executing a single command in your terminal.

## Tools Installed

Farhost installs and configures the following tools:

- **[Homebrew](https://brew.sh/):** The missing package manager for macOS (and Linux).
- **Ghostty Terminal:** A modern terminal emulator (customize as needed).
- **[oh-my-zsh](https://ohmyz.sh/):** A framework for managing your Zsh configuration.
- **[powerlevel10k](https://github.com/romkatv/powerlevel10k):** A fast and highly customizable Zsh theme.
- **[nvm](https://github.com/nvm-sh/nvm):** Node Version Manager.
- **[Node.js](https://nodejs.org/):** A JavaScript runtime built on Chrome's V8 engine.
- **[neovim](https://neovim.io/):** A hyperextensible Vim-based text editor.
- **[tmux](https://github.com/tmux/tmux):** A terminal multiplexer.
- **[tpm](https://github.com/tmux-plugins/tpm):** Tmux Plugin Manager.
- **[Python](https://www.python.org/):** The programming language.
- **[poetry](https://python-poetry.org/):** Python dependency management and packaging.
- **[pyenv](https://github.com/pyenv/pyenv):** Python version management.
- **[Docker](https://www.docker.com/):** An open platform for developing, shipping, and running applications.

## Installation

To install Farhost, run the following command in your terminal:

```bash
curl -s https://raw.githubusercontent.com/mikevive/farhost/refs/heads/main/setup.sh | bash

