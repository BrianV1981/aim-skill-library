#!/usr/bin/env python3
"""
Skill library compatibility tests (TDD).

Guards:
- Grok vessel pack is installable and frontmatter-valid
- AGY vessel pack remains installable
- No machine-local absolute home paths in skill bodies
- Dual-vessel skills document both Grok and AGY tools where required
- Registry/manifest/disk consistency for library skills
"""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
VESSELS = ROOT / "vessels"
REGISTRY = ROOT / "registry" / "skills.yaml"
INSTALL = ROOT / "scripts" / "install.sh"

HOME_ABS_RE = re.compile(r"/home/[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+")
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

# Skills that must document both hosts' file/image tools (dual body strategy).
DUAL_FILE_EDIT_SKILLS = {"aim-memory-wiki"}
DUAL_IMAGE_SKILLS = {"aim-mega-guide"}

GROK_FILE_TOOLS = ("search_replace", "write")
AGY_FILE_TOOLS = (
    "replace_file_content",
    "write_to_file",
    "multi_replace_file_content",
)
GROK_IMAGE_TOOLS = ("image_gen",)
# AGY / other hosts may use generate_image; keep if present for dual docs.
AGY_IMAGE_TOOLS = ("generate_image",)


def skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise AssertionError("missing YAML frontmatter")
    if yaml is None:
        # Minimal fallback: name + description presence
        body = m.group(1)
        name_m = re.search(r"^name:\s*(.+)$", body, re.M)
        desc_m = re.search(r"^description:\s*", body, re.M)
        return {
            "name": name_m.group(1).strip().strip("\"'") if name_m else None,
            "description": "present" if desc_m else None,
            "_raw": body,
        }
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict):
        raise AssertionError("frontmatter is not a mapping")
    return data


def manifest_ids(vessel: str) -> list[str]:
    path = VESSELS / vessel / "manifest.txt"
    ids: list[str] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.append(line)
    return ids


def load_registry() -> dict:
    text = REGISTRY.read_text()
    if yaml is None:
        raise unittest.SkipTest("PyYAML required for registry tests")
    return yaml.safe_load(text)


class TestFrontmatterAndLayout(unittest.TestCase):
    def test_every_skill_has_valid_frontmatter(self):
        self.assertTrue(skill_dirs(), "no skills found")
        for d in skill_dirs():
            skill_md = d / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"missing SKILL.md in {d.name}")
            text = skill_md.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            name = fm.get("name")
            desc = fm.get("description")
            self.assertTrue(name, f"{d.name}: missing name")
            self.assertTrue(desc, f"{d.name}: missing description")
            self.assertRegex(str(name), NAME_RE, f"{d.name}: invalid name {name!r}")
            # Directory name should match skill name (no .skill suffix dirs).
            self.assertEqual(
                d.name,
                str(name),
                f"dir {d.name!r} must equal frontmatter name {name!r}",
            )
            self.assertRegex(d.name, NAME_RE, f"dir name not skill-safe: {d.name}")

    def test_no_machine_absolute_home_paths(self):
        offenders: list[str] = []
        for path in SKILLS.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in {".md", ".sh", ".py", ".txt", ".yaml", ".yml"}:
                continue
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for i, line in enumerate(text.splitlines(), 1):
                # Allow example placeholders that are clearly non-machine
                if re.search(r"/home/user\b|/home/YOU\b|/Users/you\b", line, re.I):
                    continue
                if HOME_ABS_RE.search(line):
                    offenders.append(f"{path.relative_to(ROOT)}:{i}: {line.strip()}")
        self.assertEqual(
            offenders,
            [],
            "machine-local absolute home paths forbidden:\n" + "\n".join(offenders),
        )


class TestDualVesselTools(unittest.TestCase):
    def test_memory_wiki_documents_grok_and_agy_file_tools(self):
        text = (SKILLS / "aim-memory-wiki" / "SKILL.md").read_text(encoding="utf-8")
        for tool in GROK_FILE_TOOLS:
            self.assertIn(tool, text, f"aim-memory-wiki missing Grok tool {tool}")
        # Preserve AGY compatibility: at least one AGY tool must remain documented
        self.assertTrue(
            any(t in text for t in AGY_FILE_TOOLS),
            "aim-memory-wiki must still document AGY file tools",
        )

    def test_mega_guide_documents_grok_image_tool(self):
        path = SKILLS / "aim-mega-guide" / "SKILL.md"
        self.assertTrue(path.is_file(), "aim-mega-guide skill missing (rename from .skill)")
        text = path.read_text(encoding="utf-8")
        for tool in GROK_IMAGE_TOOLS:
            self.assertIn(tool, text, f"aim-mega-guide missing Grok image tool {tool}")
        # Dual: keep or mention AGY/other generate_image when applicable
        self.assertTrue(
            any(t in text for t in AGY_IMAGE_TOOLS) or "vessel" in text.lower(),
            "aim-mega-guide should dual-document image tools or vessel table",
        )

    def test_communicate_documents_both_skill_install_roots(self):
        text = (SKILLS / "aim-communicate" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".grok/skills/aim-communicate", text)
        self.assertIn(".gemini/skills/aim-communicate", text)

    def test_calc_documents_both_skill_install_roots(self):
        text = (SKILLS / "aim-calc" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".grok/skills", text)
        self.assertIn(".gemini/skills", text)


class TestBwrapForgeNotStub(unittest.TestCase):
    def test_bwrap_has_runnable_command_shape(self):
        text = (SKILLS / "aim-bwrap-forge" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("aim-joshua", text)
        self.assertNotIn("bwrap --unshare-all ...", text)
        # Must include concrete bwrap invocation pieces
        self.assertIn("bwrap", text)
        self.assertIn("--unshare-all", text)
        self.assertIn("tmux", text)


class TestRegistryAndManifests(unittest.TestCase):
    def test_manifest_skills_exist_on_disk(self):
        for vessel in ("agy", "grok", "opencode", "codex"):
            for sid in manifest_ids(vessel):
                self.assertTrue(
                    (SKILLS / sid).is_dir(),
                    f"vessel {vessel} lists {sid} but skills/{sid} missing",
                )

    def test_registry_library_skills_exist_and_cover_manifests(self):
        reg = load_registry()
        library = {
            s["id"]: s for s in reg.get("skills", []) if s.get("type") == "library"
        }
        # Every on-disk skill (except optional orphans we ban) must be registered
        on_disk = {d.name for d in skill_dirs()}
        self.assertEqual(
            on_disk - set(library.keys()),
            set(),
            f"on-disk skills missing from registry: {on_disk - set(library.keys())}",
        )
        for sid, meta in library.items():
            self.assertTrue((SKILLS / sid).is_dir(), f"registry id missing on disk: {sid}")
            vessels = set(meta.get("vessels") or [])
            self.assertTrue(vessels, f"{sid}: registry vessels empty")

        # Grok manifest ids must list grok in registry vessels
        for sid in manifest_ids("grok"):
            self.assertIn(sid, library, f"grok manifest skill not in registry: {sid}")
            self.assertIn(
                "grok",
                library[sid].get("vessels") or [],
                f"{sid}: in grok manifest but registry vessels omit grok",
            )

        # AGY manifest ids must list agy
        for sid in manifest_ids("agy"):
            self.assertIn(sid, library, f"agy manifest skill not in registry: {sid}")
            self.assertIn(
                "agy",
                library[sid].get("vessels") or [],
                f"{sid}: in agy manifest but registry vessels omit agy",
            )

    def test_no_orphan_skill_suffix_dirs(self):
        bad = [d.name for d in skill_dirs() if d.name.endswith(".skill")]
        self.assertEqual(bad, [], f"rename *.skill dirs: {bad}")


class TestInstallSmoke(unittest.TestCase):
    def _install(self, vessel: str, dest: Path) -> str:
        proc = subprocess.run(
            [str(INSTALL), "--vessel", vessel, "--dest", str(dest), "--mode", "copy"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"install {vessel} failed:\n{proc.stdout}\n{proc.stderr}",
        )
        self.assertNotIn("SKIP ", proc.stdout, f"install {vessel} skipped skills:\n{proc.stdout}")
        return proc.stdout

    def test_install_grok_and_agy_no_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            grok_dest = Path(tmp) / "grok"
            agy_dest = Path(tmp) / "agy"
            self._install("grok", grok_dest)
            self._install("agy", agy_dest)
            for sid in manifest_ids("grok"):
                self.assertTrue((grok_dest / sid / "SKILL.md").is_file(), sid)
            for sid in manifest_ids("agy"):
                self.assertTrue((agy_dest / sid / "SKILL.md").is_file(), sid)
            # AGY pack must not lose wiki dual tools after install copy
            wiki = (agy_dest / "aim-memory-wiki" / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(any(t in wiki for t in AGY_FILE_TOOLS))
            self.assertTrue(any(t in wiki for t in GROK_FILE_TOOLS))


class TestPolicyDoc(unittest.TestCase):
    def test_dual_compat_policy_exists(self):
        path = ROOT / "docs" / "VESSEL_DUAL_COMPAT.md"
        self.assertTrue(path.is_file(), "docs/VESSEL_DUAL_COMPAT.md required")
        text = path.read_text(encoding="utf-8")
        self.assertIn("AGY", text)
        self.assertIn("Grok", text)
        self.assertIn("dual", text.lower())


if __name__ == "__main__":
    unittest.main()
