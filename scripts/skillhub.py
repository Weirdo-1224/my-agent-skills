#!/usr/bin/env python3
"""Skill Hub: manage personal Agent Skills across Claude Code, Codex, and Kimi Code.

No third-party dependencies. Compatible with Python 3.8+ on Windows and Linux/macOS.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
STATE_FILE = Path.home() / ".skillhub" / "state.json"

SCOPES = ["shared", "claude-only", "kimi-only", "codex-only"]

# Map scope -> list of (agent_label, target_dir_name_under_home)
SCOPE_TARGETS: Dict[str, List[Tuple[str, str]]] = {
    "shared": [
        ("agents", ".agents/skills"),
        ("claude", ".claude/skills"),
        ("kimi", ".kimi-code/skills"),
    ],
    "claude-only": [
        ("claude", ".claude/skills"),
    ],
    "kimi-only": [
        ("kimi", ".kimi-code/skills"),
    ],
    # Codex-only skills are not deployed in the first phase.
    "codex-only": [],
}


@dataclass
class Skill:
    name: str
    scope: str
    path: Path
    frontmatter: Dict[str, Any] = field(default_factory=dict)

    def skill_md_path(self) -> Path:
        return self.path / "SKILL.md"

    def source_md_path(self) -> Path:
        return self.path / "SOURCE.md"


def home_dir() -> Path:
    return Path.home()


def agent_target(agent_dir: str) -> Path:
    return home_dir() / agent_dir


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        try:
            with STATE_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"[WARN] Failed to read state file {STATE_FILE}: {e}", file=sys.stderr)
    return {"managed": []}


def save_state(state: Dict[str, Any]) -> None:
    ensure_dir(STATE_FILE.parent)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def parse_frontmatter(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    if not text.startswith("---"):
        return None

    end = text.find("---", 3)
    if end == -1:
        return None

    fm_text = text[3:end].strip()
    frontmatter: Dict[str, Any] = {}

    # Minimal YAML parser for the flat/nested frontmatter used in SKILL.md.
    in_nested_block = False
    nested_key: Optional[str] = None

    for line in fm_text.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        is_indented = line.startswith(" ") or line.startswith("\t")

        # Strip surrounding quotes.
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        if is_indented and in_nested_block and nested_key:
            frontmatter[key] = value
            continue

        in_nested_block = False
        nested_key = None

        if value == "":
            in_nested_block = True
            nested_key = key
            continue

        frontmatter[key] = value

    return frontmatter


def discover_skills() -> List[Skill]:
    skills: List[Skill] = []
    for scope in SCOPES:
        scope_dir = SKILLS_DIR / scope
        if not scope_dir.exists():
            continue
        for item in sorted(scope_dir.iterdir()):
            if not item.is_dir():
                continue
            skill_md = item / "SKILL.md"
            frontmatter = parse_frontmatter(skill_md) if skill_md.exists() else {}
            if frontmatter is None:
                frontmatter = {}
            name = frontmatter.get("name", item.name)
            skills.append(Skill(name=name, scope=scope, path=item, frontmatter=frontmatter))
    return skills


def find_duplicates(skills: List[Skill]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for skill in skills:
        counts[skill.name] = counts.get(skill.name, 0) + 1
    return {name: count for name, count in counts.items() if count > 1}


def is_managed_link(path: Path, managed: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    abs_path = path.resolve()
    for entry in managed:
        if Path(entry["target"]).resolve() == abs_path:
            return entry
    return None


def create_link(source: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"target already exists: {target}")

    if sys.platform == "win32":
        # Prefer junctions because they do not require administrator privileges.
        try:
            import _winapi

            _winapi.CreateJunction(str(source), str(target))
            return
        except Exception:
            pass

        # Fallback to directory symbolic link if possible.
        try:
            os.symlink(source, target, target_is_directory=True)
            return
        except OSError as e:
            raise RuntimeError(
                f"Failed to create junction/symlink on Windows: {e}. "
                "Try running with --mode copy."
            ) from e
    else:
        try:
            os.symlink(source, target)
        except OSError as e:
            raise RuntimeError(
                f"Failed to create symlink on {sys.platform}: {e}. "
                "Try running with --mode copy."
            ) from e


def remove_link_or_copy(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    try:
        # unlink() removes symlinks and Windows junctions without touching targets.
        path.unlink()
    except (IsADirectoryError, PermissionError):
        # On Windows unlink() on a directory raises PermissionError.
        # Copy mode: remove the actual directory tree.
        shutil.rmtree(path)


def link_exists_and_valid(target: Path, expected_source: Path, mode: str = "link") -> bool:
    if not target.exists() and not target.is_symlink():
        return False

    if mode == "copy":
        return target.is_dir()

    # For links (symlinks or junctions), verify they point to the expected source.
    if target.is_symlink() or target.is_dir():
        try:
            return target.resolve() == expected_source.resolve()
        except OSError:
            return False

    return False


def cmd_list(_args: argparse.Namespace) -> int:
    skills = discover_skills()
    print(f"{'NAME':<30} {'SCOPE':<15} {'STATUS'}")
    for skill in skills:
        status = "valid"
        if not skill.skill_md_path().exists():
            status = "missing-skill-md"
        elif not skill.frontmatter.get("name"):
            status = "missing-name"
        elif skill.name != skill.path.name:
            status = "name-mismatch"
        elif not skill.frontmatter.get("description"):
            status = "missing-description"
        print(f"{skill.name:<30} {skill.scope:<15} {status}")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    mode = args.mode
    if mode not in ("link", "copy"):
        print(f"[FAIL] Unknown install mode: {mode}", file=sys.stderr)
        return 1

    skills = discover_skills()
    if not skills:
        print("[INFO] No skills found to install.")
        return 0

    state = load_state()
    managed: List[Dict[str, Any]] = list(state.get("managed", []))
    new_entries: List[Dict[str, Any]] = []

    for skill in skills:
        targets = SCOPE_TARGETS.get(skill.scope, [])
        for agent_label, agent_dir in targets:
            target_dir = agent_target(agent_dir)
            ensure_dir(target_dir)
            target = target_dir / skill.name

            existing = is_managed_link(target, managed)
            if target.exists() or target.is_symlink():
                if existing:
                    remove_link_or_copy(target)
                    managed = [e for e in managed if e is not existing]
                else:
                    print(
                        f"[SKIP] {skill.name} -> {target} (already exists, not managed by Skill Hub)",
                        file=sys.stderr,
                    )
                    continue

            try:
                if mode == "link":
                    create_link(skill.path, target)
                    link_type = "junction" if sys.platform == "win32" else "symlink"
                else:
                    shutil.copytree(skill.path, target)
                    link_type = "copy"

                entry = {
                    "name": skill.name,
                    "scope": skill.scope,
                    "agent": agent_label,
                    "source": str(skill.path),
                    "target": str(target),
                    "mode": link_type,
                }
                managed.append(entry)
                new_entries.append(entry)
                print(f"[OK] {skill.name} -> {target} ({link_type})")
            except Exception as e:
                print(f"[FAIL] {skill.name} -> {target}: {e}", file=sys.stderr)

    state["managed"] = managed
    save_state(state)

    if new_entries:
        print(f"\n[INFO] Installed {len(new_entries)} skill target(s).")
    else:
        print("\n[INFO] No new skill targets installed.")
    return 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    skills = discover_skills()
    state = load_state()
    managed = state.get("managed", [])
    duplicates = find_duplicates(skills)

    exit_code = 0

    for skill in skills:
        issues: List[str] = []

        if not skill.skill_md_path().exists():
            issues.append("missing SKILL.md")

        if not skill.frontmatter:
            issues.append("missing or unparsable frontmatter")
        else:
            if not skill.frontmatter.get("name"):
                issues.append("frontmatter missing 'name'")
            elif skill.name != skill.path.name:
                issues.append(f"name '{skill.name}' does not match directory '{skill.path.name}'")

            if not skill.frontmatter.get("description"):
                issues.append("frontmatter missing 'description'")

        if skill.name in duplicates:
            issues.append(f"duplicate skill name across scopes")

        source_type = skill.frontmatter.get("source-type", "")
        if source_type in ("external", "curated-external") and not skill.source_md_path().exists():
            issues.append("external skill missing SOURCE.md")

        if (skill.path / "scripts").exists():
            issues.append("contains scripts/ directory; review manually")

        # Check managed links for this skill.
        for entry in managed:
            if entry["name"] == skill.name and entry["scope"] == skill.scope:
                target = Path(entry["target"])
                source = Path(entry["source"])
                if not link_exists_and_valid(target, source, entry.get("mode", "link")):
                    issues.append(f"managed link broken: {target}")

        if not issues:
            print(f"[PASS] {skill.name}")
        else:
            is_fail = any(
                issue.startswith("missing")
                or issue.startswith("duplicate")
                or "broken" in issue
                for issue in issues
            )
            max_severity = "FAIL" if is_fail else "WARN"
            print(f"[{max_severity}] {skill.name}: {'; '.join(issues)}")
            if max_severity == "FAIL":
                exit_code = 1

    # Check target directories are writable.
    for agent_dir in [".agents/skills", ".claude/skills", ".kimi-code/skills"]:
        target = agent_target(agent_dir)
        if target.exists() and not os.access(target, os.W_OK):
            print(f"[FAIL] {target} is not writable")
            exit_code = 1

    return exit_code


def cmd_status(_args: argparse.Namespace) -> int:
    skills = discover_skills()
    state = load_state()
    managed = state.get("managed", [])

    if not skills:
        print("[INFO] No skills found.")
        return 0

    for skill in skills:
        print(skill.name)
        print(f"  Source: {skill.path}")

        targets = SCOPE_TARGETS.get(skill.scope, [])
        for agent_label, agent_dir in targets:
            target_dir = agent_target(agent_dir)
            target = target_dir / skill.name

            status = "missing"
            for entry in managed:
                if entry["name"] == skill.name and entry["agent"] == agent_label:
                    mode = entry.get("mode", "link")
                    if link_exists_and_valid(target, Path(entry["source"]), mode):
                        status = mode
                    else:
                        status = "broken"
                    break
            else:
                if target.exists() or target.is_symlink():
                    status = "unmanaged"

            print(f"  {agent_label.capitalize():<7} {status}")
    return 0


def cmd_uninstall(_args: argparse.Namespace) -> int:
    state = load_state()
    managed = state.get("managed", [])

    if not managed:
        print("[INFO] Nothing managed by Skill Hub to uninstall.")
        return 0

    removed = 0
    for entry in managed:
        target = Path(entry["target"])
        try:
            remove_link_or_copy(target)
            print(f"[OK] Removed {target}")
            removed += 1
        except Exception as e:
            print(f"[FAIL] Could not remove {target}: {e}", file=sys.stderr)

    save_state({"managed": []})
    print(f"\n[INFO] Removed {removed} managed target(s).")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skillhub",
        description="Manage personal Agent Skills across Claude Code, Codex, and Kimi Code.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all skills in the repository.")

    install_parser = subparsers.add_parser("install", help="Deploy skills to agent directories.")
    install_parser.add_argument(
        "--mode",
        choices=["link", "copy"],
        default="link",
        help="Deployment mode: link (default) or copy.",
    )

    subparsers.add_parser("doctor", help="Validate skill structure and deployment health.")
    subparsers.add_parser("status", help="Show deployment status for each skill.")
    subparsers.add_parser("uninstall", help="Remove all Skill Hub managed links/copies.")

    args = parser.parse_args(argv)

    command_map = {
        "list": cmd_list,
        "install": cmd_install,
        "doctor": cmd_doctor,
        "status": cmd_status,
        "uninstall": cmd_uninstall,
    }

    return command_map[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
