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
    if (ROOT / ".git").exists() and shutil.which("git"):
        proc = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z", "skills"],
            capture_output=True,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout:
            names: set[str] = set()
            for raw_rel in proc.stdout.decode("utf-8", errors="ignore").split("\0"):
                if not raw_rel:
                    continue
                parts = Path(raw_rel).parts
                if len(parts) >= 2 and parts[0] == "skills" and (SKILLS / parts[1]).is_dir():
                    names.add(parts[1])
            if names:
                return [SKILLS / n for n in sorted(names)]
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
        for skill_dir in skill_dirs():
            for path in skill_dir.rglob("*"):
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

    def test_mega_article_documents_dual_tools_and_frontmatter(self):
        path = SKILLS / "aim-mega-article" / "SKILL.md"
        self.assertTrue(path.is_file(), "aim-mega-article skill missing")
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        self.assertEqual(fm.get("name"), "aim-mega-article")
        for tool in GROK_IMAGE_TOOLS:
            self.assertIn(tool, text, f"aim-mega-article missing Grok image tool {tool}")
        self.assertTrue(any(t in text for t in AGY_IMAGE_TOOLS))
        self.assertTrue(any(t in text for t in GROK_FILE_TOOLS))
        self.assertTrue(any(t in text for t in AGY_FILE_TOOLS))
        self.assertIsNone(HOME_ABS_RE.search(text))

    def test_communicate_documents_both_skill_install_roots(self):
        text = (SKILLS / "aim-communicate" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(".grok/skills/aim-communicate", text)
        self.assertIn(".gemini/skills/aim-communicate", text)

    def test_communicate_v2_unifies_mailbox_and_removes_agy_override(self):
        self.assertFalse(
            (VESSELS / "agy" / "skills" / "aim-communicate").exists(),
            "divergent vessels/agy/skills/aim-communicate override must be removed (#17/#19/#24)",
        )
        skill_text = (SKILLS / "aim-communicate" / "SKILL.md").read_text(encoding="utf-8")
        for required_token in (
            "aim-mail send",
            "aim-mail inbox",
            "aim-mail read",
            "aim-mail reply",
            "aim-mail ack",
            "install-agy-sidecar",
        ):
            self.assertIn(required_token, skill_text)

        helper_text = (SKILLS / "aim-communicate" / "scripts" / "tmux_send.sh").read_text(encoding="utf-8")
        self.assertNotIn("send-keys -t \"$PANE_TARGET\" Escape", helper_text)
        self.assertIn("-S -300", helper_text)
        self.assertIn("aim-mailbox", (ROOT / "docs" / "COMPANIONS.md").read_text(encoding="utf-8"))

    def test_tmux_send_helper_enter_only_and_paste_verification(self):
        import os

        if os.name == "nt" or not shutil.which("bash"):
            self.skipTest("POSIX bash required for tmux_send.sh helper test")

        helper = SKILLS / "aim-communicate" / "scripts" / "tmux_send.sh"
        with tempfile.TemporaryDirectory() as tmp:
            tdir = Path(tmp)
            log_file = tdir / "tmux_calls.log"
            mode_file = tdir / "mode.txt"
            fake_tmux = tdir / "tmux"
            fake_tmux.write_text(
                "#!/usr/bin/env bash\n"
                f"LOG={str(log_file)!r}\n"
                f"MODE=$(cat {str(mode_file)!r} 2>/dev/null || echo ok)\n"
                "echo \"$*\" >> \"$LOG\"\n"
                "case \"$1\" in\n"
                "  has-session) exit 0 ;;\n"
                "  display-message) echo 'aim-joshua' ;;\n"
                "  list-panes) echo 'agy.real' ;;\n"
                "  set-buffer|paste-buffer|send-keys|delete-buffer) exit 0 ;;\n"
                "  capture-pane)\n"
                "    if [[ \"$MODE\" == \"empty_paste\" ]]; then\n"
                "      echo 'idle prompt'\n"
                "    elif [[ \"$MODE\" == \"stale_scrollback_fail\" ]]; then\n"
                "      echo '[FROM:aim-joshua] [REPLY_TO:aim-joshua] old message'\n"
                "      echo 'Thought for 3s'\n"
                "      echo '> '\n"
                "    elif grep -q 'send-keys' \"$LOG\"; then\n"
                "      echo '[FROM:aim-joshua] [REPLY_TO:aim-joshua] [Pasted text #1 +20 lines]'\n"
                "      echo 'Working...'\n"
                "    elif grep -q 'paste-buffer' \"$LOG\"; then\n"
                "      echo '> [Pasted text #1 +20 lines]'\n"
                "    else\n"
                "      echo '> '\n"
                "    fi\n"
                "    ;;\n"
                "esac\n",
                encoding="utf-8",
            )
            fake_tmux.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{tdir}:{env.get('PATH', '')}"
            env["TMPDIR"] = str(tdir)

            # 1) Multi-line paste chip ([Pasted text #1 +20 lines]) -> Enter ONLY (no Escape), rc=0, 1 turn
            mode_file.write_text("chip_ok", encoding="utf-8")
            msg_20 = "\n".join(f"Line {i}: audit payload" for i in range(1, 21))
            r_ok = subprocess.run(
                ["bash", str(helper), "--target", "aim-auditor", "--from", "aim-joshua", "--message", msg_20],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(r_ok.returncode, 0, f"expected rc=0:\n{r_ok.stdout}\n{r_ok.stderr}")
            calls = log_file.read_text(encoding="utf-8")
            self.assertNotIn("Escape", calls)
            self.assertEqual(calls.count("send-keys -t =aim-auditor: Enter"), 1)
            self.assertEqual(list(tdir.glob("aim_comm_verify.*")), [])

            # 2) Empty composer after paste -> PASTE_FAIL (rc=2) with zero Enter keys sent
            log_file.unlink()
            mode_file.write_text("empty_paste", encoding="utf-8")
            r_fail = subprocess.run(
                ["bash", str(helper), "--target", "aim-auditor", "--from", "aim-joshua", "--message", "ping"],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(r_fail.returncode, 2)
            self.assertIn("PASTE_FAIL", r_fail.stderr)
            self.assertNotIn("send-keys", log_file.read_text(encoding="utf-8"))

            # 3) Stale scrollback ([FROM:aim-joshua] + Thought for 3s) with failed paste -> PASTE_FAIL (rc=2)
            log_file.unlink()
            mode_file.write_text("stale_scrollback_fail", encoding="utf-8")
            r_stale = subprocess.run(
                ["bash", str(helper), "--target", "aim-auditor", "--from", "aim-joshua", "--message", "fresh ping"],
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(r_stale.returncode, 2)
            self.assertIn("PASTE_FAIL", r_stale.stderr)
            self.assertNotIn("send-keys", log_file.read_text(encoding="utf-8"))

    def test_tmux_send_helper_real_tmux_isolation_dnd_and_no_tmp_leaks(self):
        import os

        if os.name == "nt" or not shutil.which("bash") or not shutil.which("tmux"):
            self.skipTest("POSIX bash + tmux required for real tmux integration test")

        helper = SKILLS / "aim-communicate" / "scripts" / "tmux_send.sh"
        with tempfile.TemporaryDirectory() as tmp:
            tdir = Path(tmp)
            tmux_tmp = tdir / "tmux_sock"
            tmux_tmp.mkdir(mode=0o700)
            tmp_files = tdir / "tmp_files"
            tmp_files.mkdir(mode=0o700)

            env = os.environ.copy()
            env.pop("TMUX", None)
            env["TMUX_TMPDIR"] = str(tmux_tmp)
            env["TMPDIR"] = str(tmp_files)

            try:
                subprocess.run(
                    ["tmux", "new-session", "-d", "-s", "foo-extra", "cat"],
                    env=env,
                    check=True,
                    timeout=10,
                )
                subprocess.run(
                    ["tmux", "new-session", "-d", "-s", "foo", "cat"],
                    env=env,
                    check=True,
                    timeout=10,
                )

                # (a) Exact session match: sending to 'foo' delivers to 'foo' and never leaks to 'foo-extra'
                r_exact = subprocess.run(
                    [
                        "bash",
                        str(helper),
                        "--target",
                        "foo",
                        "--from",
                        "sender",
                        "--message",
                        "--unique-exact-check-123",
                    ],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                self.assertEqual(r_exact.returncode, 0, f"{r_exact.stdout}\n{r_exact.stderr}")
                cap_extra = subprocess.run(
                    ["tmux", "capture-pane", "-t", "=foo-extra:", "-p"],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertNotIn("unique-exact-check-123", cap_extra.stdout)

                # (b) Zero /tmp/aim_comm_* leaks
                self.assertEqual(list(tmp_files.glob("aim_comm_*")), [])

                # (c) DND session refusal + --allow-dnd override
                env_dnd = dict(env)
                env_dnd["AIM_DND_SESSIONS"] = "foo"
                r_dnd_block = subprocess.run(
                    ["bash", str(helper), "--target", "foo", "--from", "sender", "--message", "blocked"],
                    env=env_dnd,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                self.assertEqual(r_dnd_block.returncode, 2)
                self.assertIn("DND_BLOCKED", r_dnd_block.stderr)

                r_dnd_allow = subprocess.run(
                    [
                        "bash",
                        str(helper),
                        "--target",
                        "foo",
                        "--from",
                        "sender",
                        "--allow-dnd",
                        "--message",
                        "allowed override",
                    ],
                    env=env_dnd,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                self.assertEqual(r_dnd_allow.returncode, 0, f"{r_dnd_allow.stdout}\n{r_dnd_allow.stderr}")
            finally:
                sock_chk = subprocess.run(
                    ["tmux", "display-message", "-p", "#{socket_path}"],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                sock_p = sock_chk.stdout.strip()
                if "TMUX" not in env and sock_chk.returncode == 0 and sock_p and Path(sock_p).resolve().is_relative_to(tmux_tmp.resolve()):
                    subprocess.run(["tmux", "kill-server"], env=env, capture_output=True, timeout=10)

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
                exists = (SKILLS / sid).is_dir() or (VESSELS / vessel / "skills" / sid).is_dir()
                self.assertTrue(
                    exists,
                    f"vessel {vessel} lists {sid} but neither skills/{sid} nor vessels/{vessel}/skills/{sid} exists",
                )

    def test_registry_library_skills_exist_and_cover_manifests(self):
        reg = load_registry()
        library = {
            s["id"]: s for s in reg.get("skills", []) if s.get("type") == "library"
        }
        companions = {
            s["id"]: s for s in reg.get("companions", [])
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

        for vessel in ("agy", "grok", "opencode", "codex"):
            for sid in manifest_ids(vessel):
                if (SKILLS / sid).is_dir():
                    self.assertIn(sid, library, f"{vessel} manifest skill not in registry: {sid}")
                    self.assertIn(
                        vessel,
                        library[sid].get("vessels") or [],
                        f"{sid}: in {vessel} manifest but registry vessels omit {vessel}",
                    )
                else:
                    self.assertTrue(
                        (VESSELS / vessel / "skills" / sid).is_dir() or sid in companions,
                        f"{vessel} manifest override {sid} missing from vessels/{vessel}/skills/",
                    )

    def test_no_orphan_skill_suffix_dirs(self):
        bad = [d.name for d in skill_dirs() if d.name.endswith(".skill")]
        self.assertEqual(bad, [], f"rename *.skill dirs: {bad}")

    def test_skill_dirs_ignores_untracked_scratch_dirs_inside_git(self):
        untracked = SKILLS / "_tmp_untracked_scratch_skill"
        try:
            untracked.mkdir(exist_ok=True)
            (untracked / "SKILL.md").write_text("untracked scratch", encoding="utf-8")
            discovered = {d.name for d in skill_dirs()}
            self.assertNotIn("_tmp_untracked_scratch_skill", discovered)
        finally:
            if untracked.exists():
                shutil.rmtree(untracked)


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
        import os

        if os.name == "nt" or not shutil.which("bash"):
            self.skipTest("POSIX bash required for scripts/install.sh")
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

    def test_python_and_powershell_cross_platform_installers(self):
        import sys
        from unittest.mock import patch

        install_py = ROOT / "scripts" / "install.py"
        install_ps1 = ROOT / "scripts" / "install.ps1"
        self.assertTrue(install_py.is_file(), "scripts/install.py required for Windows/cross-platform installs")
        self.assertTrue(install_ps1.is_file(), "scripts/install.ps1 required for Windows PowerShell installs")
        self.assertIn("install.py", install_ps1.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as tmp:
            for vessel in ("agy", "grok", "opencode", "codex"):
                dest = Path(tmp) / f"py-{vessel}"
                proc = subprocess.run(
                    [sys.executable, str(install_py), "--vessel", vessel, "--dest", str(dest), "--mode", "copy"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(proc.returncode, 0, f"install.py {vessel} failed:\n{proc.stdout}\n{proc.stderr}")
                self.assertNotIn("SKIP ", proc.stdout)
                for sid in manifest_ids(vessel):
                    self.assertTrue((dest / sid / "SKILL.md").is_file(), f"{vessel} missing {sid}")

            # Verify Windows unprivileged symlink OSError gracefully falls back to copy
            scripts_dir = str(ROOT / "scripts")
            if scripts_dir not in sys.path:
                sys.path.insert(0, scripts_dir)
            import install as install_mod

            fallback_dest = Path(tmp) / "win-fallback"
            with patch("os.symlink", side_effect=OSError("WinError 1314: A required privilege is not held")):
                rc = install_mod.main(["--vessel", "codex", "--dest", str(fallback_dest), "--mode", "symlink"])
                self.assertEqual(rc, 0)
                self.assertTrue((fallback_dest / "aim-memory-wiki" / "SKILL.md").is_file())


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
