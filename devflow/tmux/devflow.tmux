#!/usr/bin/env bash
# DevFlow tmux plugin
# - Adds timer status to the status bar
# - Binds prefix + T to toggle a floating DevFlow window

CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read user-configurable command path, default to 'devflow' on PATH
devflow_cmd="$(tmux show-option -gqv @devflow_cmd)"
if [ -z "$devflow_cmd" ]; then
    devflow_cmd="devflow"
fi

# Status bar interpolation
# Users add #{devflow_status} to their status-right or status-left
tmux set-option -g @devflow_status "#($devflow_cmd --status)"

# Keybinding: prefix + T to toggle a floating DevFlow window
tmux bind-key T display-popup -E -w 80% -h 80% "$devflow_cmd"
