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
POLL_INTERVAL_SECONDS = 0.01
RECONNECT_INTERVAL_SECONDS = 1.0


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


def init_pygame() -> None:
    pygame.init()
    pygame.joystick.init()


def refresh_joysticks() -> None:
    pygame.joystick.quit()
    pygame.joystick.init()


def wait_for_first_joystick():
    announced_wait = False
    while True:
        refresh_joysticks()
        count = pygame.joystick.get_count()
        if count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            return joystick
        if not announced_wait:
            print("Waiting for controller...", flush=True)
            announced_wait = True
        time.sleep(RECONNECT_INTERVAL_SECONDS)


def detect_mode() -> None:
    while True:
        joystick = wait_for_first_joystick()
        print(f"Connected joystick: {joystick.get_name()}", flush=True)
        print("Press controller buttons. Ctrl+C to exit.", flush=True)
        seen = set()
        active_instance_id = joystick.get_instance_id()
        while True:
            pygame.event.pump()
            if not joystick.get_attached():
                print("Controller disconnected.", flush=True)
                break
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN and event.button not in seen:
                    seen.add(event.button)
                    print(f"Button index: {event.button}", flush=True)
                if (
                    event.type == pygame.JOYDEVICEREMOVED
                    and getattr(event, "instance_id", None) == active_instance_id
                ):
                    print("Controller disconnected.", flush=True)
                    break
            else:
                time.sleep(POLL_INTERVAL_SECONDS)
                continue
            break


def watch_mode(button_index: int, debounce_seconds: float, config_path: Path) -> None:
    last_trigger = 0.0
    while True:
        joystick = wait_for_first_joystick()
        active_instance_id = joystick.get_instance_id()
        print(
            f"Watching {joystick.get_name()} for button: {button_index}",
            flush=True,
        )
        while True:
            pygame.event.pump()
            if not joystick.get_attached():
                print("Controller disconnected. Waiting to reconnect...", flush=True)
                break
            disconnected = False
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
                if (
                    event.type == pygame.JOYDEVICEREMOVED
                    and getattr(event, "instance_id", None) == active_instance_id
                ):
                    print("Controller disconnected. Waiting to reconnect...", flush=True)
                    disconnected = True
                    break
            if disconnected:
                break
            time.sleep(POLL_INTERVAL_SECONDS)


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
    init_pygame()

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
