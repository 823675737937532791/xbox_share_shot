#!/bin/zsh
set -euo pipefail

TARGET_DIR="${HOME}/Pictures/GameScreenshots"
mkdir -p "$TARGET_DIR"
/usr/sbin/screencapture -x -D 1 "$TARGET_DIR/XboxScreenshot_$(date +%Y-%m-%d_%H-%M-%S).png"
