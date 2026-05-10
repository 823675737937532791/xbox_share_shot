#!/usr/bin/env python3

from __future__ import annotations

import argparse
import configparser
from datetime import datetime
from pathlib import Path
import signal
import subprocess
import sys
import time

import pygame


DEFAULT_CONFIG_PATH = Path("~/.config/xbox-share-shot/config.ini").expanduser()
DEFAULT_BUTTON_INDEX = 15
DEFAULT_DEBOUNCE_SECONDS = 0.7


def load_config(path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return config


def get_button_index(config: configparser.ConfigParser, override: int | None) -> int:
    if override is not None:
        return override
    return config.getint("mapper", "button_index", fallback=DEFAULT_BUTTON_INDEX)


def get_debounce_seconds(
    config: configparser.ConfigParser,
    override: float | None,
) -> float:
    if override is not None:
        return override
    return config.getfloat(
        "mapper",
        "debounce_seconds",
        fallback=DEFAULT_DEBOUNCE_SECONDS,
    )


def trigger_screenshot(config_path: Path) -> int:
    print(
        f"{datetime.now().isoformat(timespec='seconds')} trigger screenshot helper",
        flush=True,
    )
    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("take_screenshot.py")),
            "--config",
            str(config_path),
        ],
        check=False,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    if result.returncode != 0:
        print(
            f"{datetime.now().isoformat(timespec='seconds')} screenshot failed",
            flush=True,
        )
    return result.returncode


def wait_for_first_joystick():
    pygame.init()
    pygame.joystick.init()
    announced_wait = False
    while True:
        pygame.joystick.quit()
        pygame.joystick.init()
        count = pygame.joystick.get_count()
        if count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            return joystick
        if not announced_wait:
            print("Waiting for controller...", flush=True)
            announced_wait = True
        time.sleep(1.0)


def detect_mode() -> None:
    joystick = wait_for_first_joystick()
    print(f"Connected joystick: {joystick.get_name()}", flush=True)
    print("Press controller buttons. Ctrl+C to exit.", flush=True)
    seen = set()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and event.button not in seen:
                seen.add(event.button)
                print(f"Button index: {event.button}", flush=True)
        time.sleep(0.01)


def watch_mode(button_index: int, debounce_seconds: float, config_path: Path) -> None:
    joystick = wait_for_first_joystick()
    print(
        f"Watching {joystick.get_name()} for button: {button_index}",
        flush=True,
    )
    last_trigger = 0.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN and event.button == button_index:
                now = time.monotonic()
                if now - last_trigger >= debounce_seconds:
                    print(
                        f"{datetime.now().isoformat(timespec='seconds')} "
                        f"button {event.button} down",
                        flush=True,
                    )
                    trigger_screenshot(config_path)
                    last_trigger = now
        time.sleep(0.01)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Map one controller button to macOS screenshots."
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to config.ini",
    )
    parser.add_argument(
        "--detect",
        action="store_true",
        help="Print button indexes as you press controller buttons.",
    )
    parser.add_argument(
        "--button-index",
        type=int,
        help="Override the configured button index.",
    )
    parser.add_argument(
        "--debounce",
        type=float,
        help="Override the configured debounce seconds.",
    )
    args = parser.parse_args()

    config_path = Path(args.config).expanduser()
    config = load_config(config_path)

    def handle_signal(_signum, _frame):
        pygame.quit()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        if args.detect:
            detect_mode()
        else:
            watch_mode(
                get_button_index(config, args.button_index),
                get_debounce_seconds(config, args.debounce),
                config_path,
            )
    finally:
        pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
