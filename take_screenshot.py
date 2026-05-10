#!/usr/bin/env python3

from __future__ import annotations

import argparse
import configparser
from datetime import datetime
from pathlib import Path
import subprocess
import sys


DEFAULT_PREFIX = "XboxScreenshot"


def load_config(path: Path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return config


def build_output_path(config: configparser.ConfigParser) -> Path:
    save_dir = Path(
        config.get("screenshot", "save_dir", fallback="~/Desktop/游戏截图")
    ).expanduser()
    save_dir.mkdir(parents=True, exist_ok=True)

    prefix = config.get("screenshot", "filename_prefix", fallback=DEFAULT_PREFIX)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return save_dir / f"{prefix}_{timestamp}.png"


def main() -> int:
    parser = argparse.ArgumentParser(description="Take one macOS screenshot.")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to config.ini",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config).expanduser())
    output_path = build_output_path(config)

    result = subprocess.run(
        ["/usr/sbin/screencapture", "-x", str(output_path)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(output_path)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
