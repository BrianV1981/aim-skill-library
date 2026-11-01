#!/usr/bin/env python3
"""
Cross-platform skill pack installer for `aim-skill-library` (Windows 10/11, macOS, Linux, WSL).

Usage:
  python scripts/install.py --vessel agy --dest ~/.gemini/skills --mode auto
  python scripts/install.py --vessel codex --dest ~/.agents/skills --mode copy
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _remove_target(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def install_vessel_pack(vessel: str, dest: Path, mode: str = "auto", root: Path = ROOT) -> int:
    manifest = root / "vessels" / vessel / "manifest.txt"
    if not manifest.is_file():
        print(f"No manifest for vessel: {vessel}", file=sys.stderr)
        return 1

    effective_mode = ("copy" if os.name == "nt" else "symlink") if mode == "auto" else mode
    dest.mkdir(parents=True, exist_ok=True)
    print(f"Vessel={vessel} dest={dest} mode={effective_mode} root={root}")

    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        skill_id = raw_line.strip()
        if not skill_id or skill_id.startswith("#"):
            continue

        src_override = root / "vessels" / vessel / "skills" / skill_id
        src_global = root / "skills" / skill_id
        if src_override.is_dir():
            src = src_override
            print(f"Using vessel override for {skill_id}")
        elif src_global.is_dir():
            src = src_global
        else:
            print(f"SKIP {skill_id} (missing skills/{skill_id} — not in this library)")
            continue

        target = dest / skill_id
        legacy_target = dest / f"{skill_id}.skill"
        if legacy_target.exists() or legacy_target.is_symlink():
            _remove_target(legacy_target)
            print(f"clean  {legacy_target} (removed legacy directory)")

        src_real = src.resolve()
        if effective_mode == "symlink" and target.is_symlink():
            try:
                if target.resolve() == src_real:
                    print(f"keep   {target}")
                    continue
            except OSError:
                pass

        if target.exists() or target.is_symlink():
            _remove_target(target)

        if effective_mode == "symlink":
            try:
                os.symlink(str(src_real), str(target), target_is_directory=True)
                print(f"symlink {target} -> {src_real}")
                continue
            except OSError as exc:
                print(
                    f"[NOTICE] Symlink unavailable ({exc}); falling back to copy for {skill_id}",
                    file=sys.stderr,
                )

        shutil.copytree(src_real, target)
        print(f"copied  {target}")

    print("Done. Companion tools (browser suite, google Workspace, …) install from their own repos — see docs/COMPANIONS.md")
    print(f"Ensure the host CLI scans: {dest}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Install aim-skill-library pack for a target CLI/IDE vessel.")
    parser.add_argument("--vessel", required=True, help="Target vessel: agy | grok | opencode | codex")
    parser.add_argument("--dest", required=True, help="Destination skills directory")
    parser.add_argument(
        "--mode",
        choices=["auto", "symlink", "copy"],
        default="auto",
        help="Install mode: auto (copy on Windows, symlink on POSIX), symlink, or copy",
    )
    args = parser.parse_args(argv)
    dest_path = Path(os.path.expanduser(args.dest))
    return install_vessel_pack(args.vessel.strip(), dest_path, mode=args.mode)


if __name__ == "__main__":
    raise SystemExit(main())
