#!/usr/bin/env bash

# DevFlow tmux plugin
# Binds prefix + T to toggle a floating DevFlow window
tmux bind-key T display-popup -E -w 80% -h 80% "devflow"
