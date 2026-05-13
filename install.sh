#!/bin/zsh
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/xbox-share-shot"
CONFIG_PATH="$CONFIG_DIR/config.ini"
APP_DIR="$HOME/Applications"
SHORTCUT_LAUNCHER="$APP_DIR/Main Screen Screenshot.command"

mkdir -p "$CONFIG_DIR" "$APP_DIR"

if [[ ! -f "$CONFIG_PATH" ]]; then
  cp "$PROJECT_DIR/config.example.ini" "$CONFIG_PATH"
  echo "Created config: $CONFIG_PATH"
else
  echo "Keeping existing config: $CONFIG_PATH"
fi

chmod +x "$PROJECT_DIR/main_screen_screenshot.sh"

cat > "$SHORTCUT_LAUNCHER" <<EOF
#!/bin/zsh
zsh "$PROJECT_DIR/main_screen_screenshot.sh"
EOF

chmod +x "$SHORTCUT_LAUNCHER"

echo
echo "Install complete."
echo "Screenshot script: $PROJECT_DIR/main_screen_screenshot.sh"
echo "Test launcher: $SHORTCUT_LAUNCHER"
echo "Config file: $CONFIG_PATH"
echo
echo "Next step:"
echo "Open SHORTCUT_SETUP.md and create one macOS Shortcut that runs:"
echo "zsh \"$PROJECT_DIR/main_screen_screenshot.sh\""
