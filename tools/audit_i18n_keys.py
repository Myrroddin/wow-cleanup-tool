#!/usr/bin/env python3
from __future__ import annotations

import ast
import os
import re
import sys
from pathlib import Path
from typing import Iterable, Set, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
LOCALE_FILE = SRC_DIR / "localization" / "en_us.py"

# Heuristics for "translation function" calls in your codebase.
# Add/rename patterns here to match your actual API (t, tr, translate, i18n.t, etc).
FUNC_NAME_PATTERNS = {"t", "tr", "translate", "gettext", "_"}
ATTR_CALL_PATTERNS = {
    ("i18n", "t"),
    ("i18n", "tr"),
    ("localization", "t"),
    ("localizer", "t"),
}

# Some projects also use dict-style access: t["key"] or TRANSLATIONS["key"]
SUBSCRIPT_NAME_PATTERNS = {"t", "TRANSLATIONS", "translations"}


def load_defined_keys(locale_file: Path) -> Set[str]:
    if not locale_file.exists():
        raise FileNotFoundError(f"Missing locale file: {locale_file}")

    src = locale_file.read_text(encoding="utf-8")
    mod = ast.parse(src, filename=str(locale_file))
    keys: Set[str] = set()

    class Visitor(ast.NodeVisitor):
        def visit_Assign(self, node: ast.Assign) -> None:
            # Look for TRANSLATIONS = {...}
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "TRANSLATIONS":
                    if isinstance(node.value, ast.Dict):
                        for k in node.value.keys:
                            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                                keys.add(k.value)
            self.generic_visit(node)

    Visitor().visit(mod)
    return keys


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        # Skip venvs, build dirs, caches, etc.
        parts = {p.lower() for p in path.parts}
        if any(
            x in parts
            for x in {".venv", "venv", "__pycache__", "dist", "build", ".git"}
        ):
            continue
        yield path


def extract_used_keys_from_ast(py_file: Path) -> Set[str]:
    text = py_file.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(text, filename=str(py_file))
    except SyntaxError:
        # Still try regex fallback if a file is mid-edit.
        return extract_used_keys_regex(text)

    used: Set[str] = set()

    def add_const_str(arg: ast.AST) -> None:
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            used.add(arg.value)

    class V(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            # t("key")
            if isinstance(node.func, ast.Name) and node.func.id in FUNC_NAME_PATTERNS:
                if node.args:
                    add_const_str(node.args[0])

            # i18n.t("key") / localizer.t("key")
            if isinstance(node.func, ast.Attribute) and isinstance(
                node.func.value, ast.Name
            ):
                obj = node.func.value.id
                attr = node.func.attr
                if (obj, attr) in ATTR_CALL_PATTERNS and node.args:
                    add_const_str(node.args[0])

            self.generic_visit(node)

        def visit_Subscript(self, node: ast.Subscript) -> None:
            # TRANSLATIONS["key"] or t["key"]
            if (
                isinstance(node.value, ast.Name)
                and node.value.id in SUBSCRIPT_NAME_PATTERNS
            ):
                # slice can be Constant or Index(Constant) depending on Python version/AST
                sl = node.slice
                if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                    used.add(sl.value)
            self.generic_visit(node)

    V().visit(tree)

    # Add regex fallback too (catches fancier patterns AST misses)
    used |= extract_used_keys_regex(text)
    return used


def extract_used_keys_regex(text: str) -> Set[str]:
    used: Set[str] = set()
    # i18n.t("key") / t("key") / _("key") etc.
    for m in re.finditer(
        r"""(?:\b(?:i18n|localizer|localization)\.(?:t|tr)|\b(?:t|tr|translate|gettext|_))\(\s*["']([^"']+)["']\s*[\),]""",
        text,
    ):
        used.add(m.group(1))
    # TRANSLATIONS["key"]
    for m in re.finditer(r"""\bTRANSLATIONS\[\s*["']([^"']+)["']\s*\]""", text):
        used.add(m.group(1))
    return used


def main() -> int:
    defined = load_defined_keys(LOCALE_FILE)

    used: Set[str] = set()
    used_by_file: Dict[str, Set[str]] = {}

    for py in iter_python_files(SRC_DIR):
        keys = extract_used_keys_from_ast(py)
        if keys:
            used |= keys
            used_by_file[str(py.relative_to(REPO_ROOT))] = keys

    missing = sorted(used - defined)
    unused = sorted(defined - used)

    print(f"Defined keys (enUS): {len(defined)}")
    print(f"Used keys (code scan): {len(used)}")
    print()

    if missing:
        print("MISSING KEYS (used in code, not defined in enUS TRANSLATIONS):")
        for k in missing:
            print(f"  - {k}")
        print()
    else:
        print("No missing keys found.\n")

    if unused:
        print("UNUSED KEYS (defined in enUS, not found in code scan):")
        for k in unused:
            print(f"  - {k}")
        print()

    # Optional: show which files reference missing keys
    if missing:
        print("WHERE MISSING KEYS ARE REFERENCED:")
        missing_set = set(missing)
        for file, keys in sorted(used_by_file.items()):
            hit = sorted(keys & missing_set)
            if hit:
                print(f"- {file}:")
                for k in hit:
                    print(f"    {k}")

    # exit code makes it CI-friendly
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
