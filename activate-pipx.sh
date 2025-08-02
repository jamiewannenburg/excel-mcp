#!/usr/bin/env bash
# Run this script to set pipx paths for this project

export PIPX_HOME="$PWD/.pipx_home"
export PIPX_BIN_DIR="$PWD/.pipx_bin"
export PATH="$PIPX_BIN_DIR:$PATH"