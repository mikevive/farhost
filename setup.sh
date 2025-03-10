#!bin/bash
set -e

# Farhost
if [ ! -d "$HOME/.farhost" ]; then
  echo "Installing Farshost..."
  git clone https://github.com/mikevive/farhost.git "$HOME/.farhost"
fi

# Backup .zshrc
if [ -f "$HOME/.zshrc" ]; then
  echo "Backing up .zshrc..."
  mv "$HOME/.zshrc" "$HOME/.zshrc.backup_$(date +%s)"
fi

# Link .zshrc
echo "Linking .zshrc..."
ln -sf "$(pwd)/.zshrc" "$HOME/.zshrc"

# Hombrew
if ! command -v brew &> /dev/null; then
  echo "Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Ghosty
if ! brew list --cask ghostty &> /dev/null; then
  echo "Installing Ghostty..."
  brew install --cask ghostty
fi

# Backup Ghostty config folder
GHOSTTY_CONFIG_DIR="$HOME/.config/ghostty"
if [ -d "$GHOSTTY_CONFIG_DIR" ]; then
  echo "Backing up Ghostty config folder..."
  mv "$GHOSTTY_CONFIG_DIR" "${GHOSTTY_CONFIG_DIR}_backup_$(date +%s)"
fi

# Link Ghostty config folder
echo "Linking Ghostty config folder..."
ln -s "$(pwd)/ghostty" "$GHOSTTY_CONFIG_DIR"

# Oh My Zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo "Installing Oh My Zsh..."
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Zsh Autosuggestion plugin
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" ]; then
  echo "Installing zsh-autosuggestions plugin..."
  git clone https://github.com/zsh-users/zsh-autosuggestions.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
fi

# Zsh Syntax Highlighting plugin
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting" ]; then
  echo "Installing zsh-autosuggestions plugin..."
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
fi

# Zsh Autocomplete plugin
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autocomplete" ]; then
  echo "Installing zsh-autocomplete plugin..."
  git clone https://github.com/marlonrichert/zsh-autocomplete.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autocomplete
fi

# Zsh Fast Syntax Highlighting plugin
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting" ]; then
  echo "Installing fast-syntax-highlighting plugin..."
  git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting
fi

# Zsh pyautoenv plugin
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/pyautoenv" ]; then
  echo "Installing pyautoenv plugin..."
  git clone https://github.com/hsaunders1904/pyautoenv.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/pyautoenv
fi

# Powerlevel10k
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]; then
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
fi

# Backup .p10k.zsh
if [ -f "$HOME/.p10k.zsh" ]; then
  echo "Backing up .p10k.zsh..."
  cp "$HOME/.p10k.zsh" "$HOME/.p10k.zsh.backup_$(date +%s)"
fi

# Link .p10k.zsh
echo "Linking .p10k.zsh..."
ln -sf "$(pwd)/.p10k.zsh" "$HOME/.p10k.zsh"

# Tmux
if ! command -v tmux &> /dev/null; then
  echo "Installing Tmux..."
  brew install tmux
fi

# Backup .tmux.conf
if [ -f "$HOME/.tmux.conf" ]; then
  echo "Backing up .tmux.conf..."
  cp "$HOME/.tmux.conf" "$HOME/.tmux.conf.backup_$(date +%s)"
fi

# Link .tmux.conf
echo "Linking .tmux.conf..."
ln -sf "$(pwd)/.tmux.conf" "$HOME/.tmux.conf"

# tpm (Tmux Plugin Manager)
if ! command -v tmux &> /dev/null; then
  echo "Installing Tmux..."
  brew install tmux
fi

# Backup tpm config folder
TPM_CONFIG_DIR="$HOME/.tmux"
if [ -d "$TPM_CONFIG_DIR" ]; then
  echo "Backing up tpm config folder..."
  mv "$TPM_CONFIG_DIR" "${TPM_CONFIG_DIR}_backup_$(date +%s)"
fi

# Link tpm config folder
echo "Linking tpm config folder..."
ln -s "$(pwd)/.tmux" "$TPM_CONFIG_DIR"

# Neovim
if ! command -v nvim &> /dev/null; then
  echo "Installing Neovim..."
  brew install neovim
fi

# Backup Neovim config folder
NVIM_CONFIG_DIR="$HOME/.config/nvim"
if [ -d "$NVIM_CONFIG_DIR" ]; then
  echo "Backing up Neovim config folder..."
  mv "$NVIM_CONFIG_DIR" "${NVIM_CONFIG_DIR}_backup_$(date +%s)"
fi

# Link Neovim config folder
echo "Linking Neovim config folder..."
ln -s "$(pwd)/nvim" "$NVIM_CONFIG_DIR"

# NVM (Node Version Manager)
if [ ! -d "$HOME/.nvm" ]; then
  echo "Installing NVM..."
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
  # Load NVM for the current session
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# Node JS
if ! command -v node &> /dev/null; then
  echo "Installing latest Node.js via NVM..."
  nvm install node
fi

# Pyenv
if ! command -v pyenv &> /dev/null; then
  echo "Installing pyenv..."
  brew install pyenv
fi

# Pyenv Virtualenv Plugin
if ! brew list | grep -q "pyenv-virtualenv"; then
  echo "Installing pyenv-virtualenv plugin..."
  brew install pyenv-virtualenv
fi

# Poetry
if ! brew list | grep -q "poetry"; then
  echo "Installing Poetry..."
  brew install poetry
  # use pyenv local env
  poetry config virtualenvs.in-project true
fi

# Python
LATEST_PYTHON=$(pyenv install --list | grep -E "^\s*[0-9]+\.[0-9]+\.[0-9]+$" | tail -1 | tr -d ' ')
if ! pyenv versions | grep -q "$LATEST_PYTHON"; then
  echo "Installing Python $LATEST_PYTHON..."
  pyenv install "$LATEST_PYTHON"
fi

# Docker
if ! brew list | grep -q "docker"; then
  echo "Installing Docker..."
  brew install --cask docker
fi

echo "Development environment setup complete."

# New TS project script
# Raycast
# 1P
# moom
# alt-tab
