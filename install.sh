#!/bin/zsh
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_DIR="$HOME/.config/xbox-share-shot"
CONFIG_PATH="$CONFIG_DIR/config.ini"
VENV_DIR="$PROJECT_DIR/.venv"
APP_DIR="$HOME/Applications"

mkdir -p "$CONFIG_DIR" "$APP_DIR"

if [[ ! -f "$CONFIG_PATH" ]]; then
  cp "$PROJECT_DIR/config.example.ini" "$CONFIG_PATH"
  echo "Created config: $CONFIG_PATH"
else
  echo "Keeping existing config: $CONFIG_PATH"
fi

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r "$PROJECT_DIR/requirements.txt"

cat > "$APP_DIR/Xbox Share Shot.command" <<EOF
#!/bin/zsh
cd "$PROJECT_DIR"
if pgrep -f "$PROJECT_DIR/xbox_share_shot.py --config $CONFIG_PATH" >/dev/null 2>&1; then
  echo "Xbox Share Shot is already running."
  echo "Press Enter to close this window."
  read
  exit 0
fi
echo "Starting Xbox Share Shot..."
"$VENV_DIR/bin/python3" "$PROJECT_DIR/xbox_share_shot.py" --config "$CONFIG_PATH"
status=\$?
echo
echo "Xbox Share Shot exited with status \$status"
echo "Press Enter to close this window."
read
EOF

cat > "$APP_DIR/Detect Xbox Share Button.command" <<EOF
#!/bin/zsh
cd "$PROJECT_DIR"
echo "Starting detect mode..."
"$VENV_DIR/bin/python3" "$PROJECT_DIR/xbox_share_shot.py" --config "$CONFIG_PATH" --detect
status=\$?
echo
echo "Detect mode exited with status \$status"
echo "Press Enter to close this window."
read
EOF

cat > "$APP_DIR/Stop Xbox Share Shot.command" <<EOF
#!/bin/zsh
if pkill -f "$PROJECT_DIR/xbox_share_shot.py" >/dev/null 2>&1; then
  echo "Stopped Xbox Share Shot."
else
  echo "Xbox Share Shot was not running."
fi
echo "Press Enter to close this window."
read
EOF

chmod +x \
  "$APP_DIR/Xbox Share Shot.command" \
  "$APP_DIR/Detect Xbox Share Button.command" \
  "$APP_DIR/Stop Xbox Share Shot.command"

echo
echo "Install complete."
echo "Start launcher: $APP_DIR/Xbox Share Shot.command"
echo "Detect launcher: $APP_DIR/Detect Xbox Share Button.command"
echo "Stop launcher: $APP_DIR/Stop Xbox Share Shot.command"
echo "Config file: $CONFIG_PATH"
