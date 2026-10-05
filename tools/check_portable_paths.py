"""Check tracked repository paths against common Windows checkout rules.

Run from the repository root. This checks Git's tracked names, which catches
portable-path regressions before a Windows checkout or a cross-platform package
is created.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

INVALID_COMPONENT = re.compile(r'[<>:"|?*]')
RESERVED_NAMES = {
    "AUX",
    "CLOCK$",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "CON",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
    "NUL",
    "PRN",
}


def tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def invalid_components(path: str) -> list[str]:
    violations: list[str] = []
    for component in path.replace("\\", "/").split("/"):
        if not component:
            continue
        if INVALID_COMPONENT.search(component):
            violations.append("contains a Windows-invalid character")
        if component.endswith((" ", ".")):
            violations.append("ends with a space or dot")
        device_name = component.rstrip(" .").split(".", 1)[0].upper()
        if device_name in RESERVED_NAMES:
            violations.append("uses a reserved Windows device name")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    violations = [
        (path, reason)
        for path in tracked_paths(root)
        for reason in invalid_components(path)
    ]
    if violations:
        print("Non-portable tracked paths detected:")
        for path, reason in violations:
            print(f"- {path}: {reason}")
        return 1
    print("All tracked paths are portable for Windows checkout/evaluation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
