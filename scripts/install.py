#!/usr/bin/env python3
"""
Cross-platform skill pack installer for `aim-skill-library` (Windows 10/11, macOS, Linux, WSL).

Usage:
  python scripts/install.py --vessel agy --dest ~/.gemini/skills --mode auto
  python scripts/install.py --vessel opencode --dest ~/.config/opencode/skills --mode auto
  python scripts/install.py --vessel codex --dest ~/.agents/skills --mode copy
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE_SKILL_ID_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")


def _remove_target(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _extract_skill_description(skill_md: Path, fallback_id: str) -> str:
    """Extract a concise single-line YAML frontmatter description without third-party dependencies."""
    default_desc = f"Load and execute the {fallback_id} skill"
    try:
        head = skill_md.read_text(encoding="utf-8", errors="ignore")[:3072]
    except OSError:
        return default_desc

    lines = head.splitlines()
    if not lines or lines[0].strip() != "---":
        return default_desc

    fm_lines: list[str] = []
    for ln in lines[1:]:
        if ln.strip() == "---":
            break
        fm_lines.append(ln)

    in_block = False
    parts: list[str] = []
    raw_desc = ""
    for ln in fm_lines:
        stripped = ln.strip()
        if in_block:
            if ln.startswith((" ", "\t")) and stripped:
                parts.append(stripped)
                continue
            break
        if ln.lower().startswith("description:"):
            val = ln.split(":", 1)[1].strip()
            if val in (">", "|", ">-", "|-"):
                in_block = True
            else:
                raw_desc = val.strip("'\"")
                break

    if parts:
        raw_desc = " ".join(parts)
    cleaned = re.sub(r"\s+", " ", raw_desc).strip()
    if not cleaned:
        return default_desc
    if len(cleaned) > 140:
        cleaned = cleaned[:137].rstrip() + "..."
    return cleaned


def _yaml_double_quote(val: str) -> str:
    escaped = val.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def sync_opencode_commands(skills_dest: Path, commands_dest: Path) -> int:
    """Generate OpenCode `/` slash-command wrappers (`commands/*.md`) for all skills in `skills_dest`."""
    if not skills_dest.is_dir():
        return 0

    commands_dest.mkdir(parents=True, exist_ok=True)
    written = 0
    for entry in sorted(skills_dest.iterdir(), key=lambda p: p.name.lower()):
        if not entry.is_dir():
            continue
        skill_id = entry.name
        if not SAFE_SKILL_ID_RE.match(skill_id):
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            continue

        desc = _extract_skill_description(skill_md, skill_id)
        wrapper_path = commands_dest / f"{skill_id}.md"
        wrapper_body = (
            "---\n"
            f"description: {_yaml_double_quote(desc)}\n"
            "---\n"
            f"Use the `{skill_id}` skill via the `skill` tool and follow its instructions. $ARGUMENTS\n"
        )
        wrapper_path.write_text(wrapper_body, encoding="utf-8", newline="\n")
        written += 1

    generic_path = commands_dest / "aim.md"
    generic_body = (
        "---\n"
        'description: "Load and run an installed A.I.M. skill by ID (e.g. /aim aim-handoff)"\n'
        "---\n"
        "The user invoked `/aim` with: $ARGUMENTS\n"
        "Treat the first token as the skill ID, load that skill via the `skill` tool, "
        "and follow its instructions for the remaining request.\n"
    )
    generic_path.write_text(generic_body, encoding="utf-8", newline="\n")
    print(f"commands {commands_dest} ({written} skill wrappers + aim.md)")
    return written


def _resolve_opencode_commands_dest(
    skills_dest: Path,
    explicit_commands_dest: Path | None = None,
    no_commands: bool = False,
) -> Path | None:
    if no_commands:
        return None
    if explicit_commands_dest is not None:
        return explicit_commands_dest
    if skills_dest.name.lower() == "skills":
        return skills_dest.parent / "commands"
    return None


def install_vessel_pack(
    vessel: str,
    dest: Path,
    mode: str = "auto",
    root: Path = ROOT,
    *,
    commands_dest: Path | None = None,
    no_commands: bool = False,
) -> int:
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

    if vessel == "opencode":
        eff_cmds = _resolve_opencode_commands_dest(dest, commands_dest, no_commands=no_commands)
        if eff_cmds is not None:
            sync_opencode_commands(dest, eff_cmds)

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
    parser.add_argument(
        "--commands-dest",
        default="",
        help="Optional explicit OpenCode commands directory (defaults to <dest>/../commands when <dest> ends in /skills)",
    )
    parser.add_argument(
        "--no-commands",
        action="store_true",
        help="Skip OpenCode slash-command wrapper generation",
    )
    parser.add_argument(
        "--sync-commands-only",
        action="store_true",
        help="Only regenerate OpenCode commands/*.md wrappers from an existing skills directory",
    )
    args = parser.parse_args(argv)
    dest_path = Path(os.path.expanduser(args.dest))
    cmd_dest = Path(os.path.expanduser(args.commands_dest)) if args.commands_dest.strip() else None

    if args.sync_commands_only:
        eff = _resolve_opencode_commands_dest(dest_path, cmd_dest, no_commands=args.no_commands)
        if eff is not None:
            sync_opencode_commands(dest_path, eff)
        return 0

    return install_vessel_pack(
        args.vessel.strip(),
        dest_path,
        mode=args.mode,
        commands_dest=cmd_dest,
        no_commands=args.no_commands,
    )


if __name__ == "__main__":
    raise SystemExit(main())
