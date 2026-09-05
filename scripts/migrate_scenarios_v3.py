#!/usr/bin/env python3
"""
Migrate LlmExpl scenario YAML files to Scenario YAML v1.

V3 fixes two YAML layouts discovered by the V2 dry-run:
- flow mappings such as:  - {id: x, name: Dog, emoji: ...}
- zero-indent lists such as:
      concepts:
      - Dog
      - Wolf

Default mode is DRY RUN. No file is modified unless --apply is used.

The migration is deliberately mechanical:
    objects: -> concepts:
    name:    -> concept:
    scalar concept entries -> mappings with concept:

PyYAML is used before and after the textual migration to prove that the
ordered semantic strings sent to the model are exactly unchanged.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class FileResult:
    path: Path
    changed: bool = False
    before_strings: list[str] = field(default_factory=list)
    after_strings: list[str] = field(default_factory=list)
    migrated_objects: int = 0
    migrated_names: int = 0
    migrated_scalars: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    new_text: str | None = None


def load_yaml_text(text: str, source: str) -> dict[str, Any]:
    try:
        data = yaml.safe_load(text)
    except Exception as exc:
        raise ValueError(f"YAML parse error in {source}: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"{source}: top-level YAML value must be a mapping")
    return data


def semantic_strings(data: dict[str, Any]) -> list[str]:
    if "objects" in data and "concepts" in data:
        raise ValueError("scenario contains both 'objects' and 'concepts'")

    if "objects" in data:
        entries = data["objects"]
        legacy = True
    elif "concepts" in data:
        entries = data["concepts"]
        legacy = False
    else:
        raise ValueError("scenario contains neither 'objects' nor 'concepts'")

    if not isinstance(entries, list):
        raise ValueError("scenario entries must be a list")

    result: list[str] = []
    for i, entry in enumerate(entries, 1):
        if isinstance(entry, str):
            result.append(entry)
            continue
        if not isinstance(entry, dict):
            raise ValueError(f"entry #{i} must be a string or mapping")

        if legacy:
            value = entry.get("name")
        else:
            value = entry.get("concept", entry.get("name"))

        if not isinstance(value, str) or value == "":
            raise ValueError(f"entry #{i} has no non-empty semantic string")
        result.append(value)

    return result


TOP_LEVEL_OBJECTS_RE = re.compile(r"^objects:(\s*(?:#.*)?)$", re.MULTILINE)

# Ordinary block-mapping key:
#     name: Dog
#   - name: Dog
BLOCK_NAME_RE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<prefix>-\s+)?name:(?P<rest>[ \t]*.*)$",
    re.MULTILINE,
)

# Flow mapping:
#   - {id: dog, name: Dog, emoji: ...}
#   - {name: Dog}
FLOW_NAME_RE = re.compile(r"(?P<prefix>[{,][ \t]*)name(?P<colon>[ \t]*:)")


def migrate_scalar_concepts(text: str) -> tuple[str, int]:
    """
    Convert scalar list items directly under top-level concepts:.

    Handles both:
        concepts:
          - Dog
    and:
        concepts:
        - Dog
    """
    lines = text.splitlines(keepends=True)
    header_index = None

    for i, line in enumerate(lines):
        if re.match(r"^concepts:(\s*(?:#.*)?)\r?\n?$", line):
            header_index = i
            break

    if header_index is None:
        return text, 0

    converted = 0
    list_indent: int | None = None

    for i in range(header_index + 1, len(lines)):
        raw = lines[i]
        content = raw.rstrip("\r\n")
        newline = raw[len(content):]

        if not content.strip() or content.lstrip().startswith("#"):
            continue

        m = re.match(r"^(?P<indent>[ \t]*)-\s+(?P<body>.*)$", content)

        # A non-list line at indentation 0 starts the next top-level key.
        if not m:
            if len(content) == len(content.lstrip(" \t")):
                break
            continue

        indent_len = len(m.group("indent"))
        if list_indent is None:
            list_indent = indent_len

        # Nested list item: not a direct concept entry.
        if indent_len != list_indent:
            continue

        body = m.group("body")

        # Existing mapping / flow structure: leave alone.
        if re.match(r"""^(?:['"][^'"]+['"]|[A-Za-z0-9_.-]+)\s*:""", body):
            continue
        if body.lstrip().startswith(("{", "[")):
            continue

        lines[i] = f"{m.group('indent')}- concept: {body}{newline}"
        converted += 1

    return "".join(lines), converted


def migrate_text(text: str) -> tuple[str, int, int, int]:
    migrated, n_objects = TOP_LEVEL_OBJECTS_RE.subn(r"concepts:\1", text, count=1)

    migrated, n_block_names = BLOCK_NAME_RE.subn(
        lambda m: (
            f"{m.group('indent')}{m.group('prefix') or ''}"
            f"concept:{m.group('rest')}"
        ),
        migrated,
    )

    migrated, n_flow_names = FLOW_NAME_RE.subn(
        lambda m: f"{m.group('prefix')}concept{m.group('colon')}",
        migrated,
    )

    migrated, n_scalars = migrate_scalar_concepts(migrated)

    return migrated, n_objects, n_block_names + n_flow_names, n_scalars


LANGUAGE_SUFFIX_RE = re.compile(r"_([a-z]{2,3})\.ya?ml$", re.IGNORECASE)


def validate_metadata(path: Path, data: dict[str, Any], result: FileResult) -> None:
    language = data.get("language")
    if language is not None and not isinstance(language, str):
        result.warnings.append("top-level 'language' is not a string")
        return

    if "multilingual" in path.stem.lower():
        return

    match = LANGUAGE_SUFFIX_RE.search(path.name)
    if match and language:
        suffix = match.group(1).lower()
        if suffix != language.lower():
            result.warnings.append(
                f"filename language suffix '{suffix}' != YAML language '{language}'"
            )


def validate_ids(data: dict[str, Any], result: FileResult) -> None:
    entries = data.get("concepts", [])
    if not isinstance(entries, list):
        return

    seen: set[str] = set()
    duplicates: set[str] = set()

    for entry in entries:
        if isinstance(entry, dict):
            value = entry.get("id")
            if isinstance(value, str) and value:
                if value in seen:
                    duplicates.add(value)
                seen.add(value)

    if duplicates:
        result.warnings.append(
            "duplicate ids in file: " + ", ".join(sorted(duplicates))
        )


def validate_canonical_schema(data: dict[str, Any]) -> None:
    if "objects" in data:
        raise ValueError("legacy top-level 'objects' remains after migration")
    if "concepts" not in data:
        raise ValueError("top-level 'concepts' missing after migration")

    entries = data["concepts"]
    if not isinstance(entries, list):
        raise ValueError("'concepts' must be a list")

    for i, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"entry #{i} is not a mapping after migration")
        if "name" in entry:
            raise ValueError(f"entry #{i} still contains legacy 'name'")
        concept = entry.get("concept")
        if not isinstance(concept, str) or concept == "":
            raise ValueError(f"entry #{i} has no non-empty string 'concept'")


def process_file(path: Path, apply: bool) -> FileResult:
    result = FileResult(path=path)

    try:
        old_text = path.read_text(encoding="utf-8")
        before_data = load_yaml_text(old_text, str(path))
        result.before_strings = semantic_strings(before_data)

        new_text, n_objects, n_names, n_scalars = migrate_text(old_text)
        result.migrated_objects = n_objects
        result.migrated_names = n_names
        result.migrated_scalars = n_scalars
        result.new_text = new_text
        result.changed = new_text != old_text

        after_data = load_yaml_text(new_text, f"{path} after migration")
        result.after_strings = semantic_strings(after_data)

        if result.before_strings != result.after_strings:
            raise ValueError(
                "SEMANTIC STRING MISMATCH: model inputs changed during migration"
            )

        validate_canonical_schema(after_data)
        validate_metadata(path, after_data, result)
        validate_ids(after_data, result)

        if apply and result.changed:
            # newline="" means: preserve the line endings already present in new_text.
            with path.open("w", encoding="utf-8", newline="") as f:
                f.write(new_text)

    except Exception as exc:
        result.errors.append(str(exc))

    return result


def discover_files(root: Path) -> list[Path]:
    return [
        p for p in sorted(root.rglob("*.yaml"))
        if p.name != "_template.yaml"
    ]


def print_diff_preview(result: FileResult, root: Path) -> None:
    old_text = result.path.read_text(encoding="utf-8")
    new_text = result.new_text or old_text
    rel = result.path.relative_to(root)

    for line in difflib.unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile=str(rel),
        tofile=str(rel),
        lineterm="",
    ):
        print(line)


def print_report(
    results: list[FileResult],
    root: Path,
    apply: bool,
    verbose: bool,
    show_diff: bool,
) -> int:
    total_files = len(results)
    changed_files = sum(r.changed for r in results)
    total_before = sum(len(r.before_strings) for r in results if not r.errors)
    total_after = sum(len(r.after_strings) for r in results if not r.errors)
    migrated_objects = sum(r.migrated_objects for r in results)
    migrated_names = sum(r.migrated_names for r in results)
    migrated_scalars = sum(r.migrated_scalars for r in results)
    error_count = sum(len(r.errors) for r in results)
    warning_count = sum(len(r.warnings) for r in results)

    print()
    print("=" * 72)
    print("LlmExpl — Scenario YAML v1 migration — V3")
    print("=" * 72)
    print(f"Mode                       : {'APPLY' if apply else 'DRY RUN'}")
    print(f"Scenario directory         : {root}")
    print(f"YAML files examined        : {total_files}")
    print(f"Files that would change    : {changed_files}")
    print()
    print(f"'objects' keys to migrate  : {migrated_objects}")
    print(f"'name' fields to migrate   : {migrated_names}")
    print(f"scalar concept entries     : {migrated_scalars}")
    print()
    print(f"Semantic strings before    : {total_before}")
    print(f"Semantic strings after     : {total_after}")
    print(
        "Changed semantic strings   : "
        + ("0  ✓" if total_before == total_after and error_count == 0
           else "CHECK ERRORS")
    )
    print()
    print(f"Warnings                   : {warning_count}")
    print(f"Errors                     : {error_count}")

    if verbose or error_count or warning_count:
        print()
        print("-" * 72)
        print("Per-file details")
        print("-" * 72)

        for r in results:
            if not (verbose or r.errors or r.warnings):
                continue

            rel = r.path.relative_to(root)
            status = "ERROR" if r.errors else ("CHANGE" if r.changed else "OK")
            print(f"{status:7} {rel}")

            if verbose and not r.errors:
                details = []
                if r.migrated_objects:
                    details.append(f"{r.migrated_objects} objects→concepts")
                if r.migrated_names:
                    details.append(f"{r.migrated_names} name→concept")
                if r.migrated_scalars:
                    details.append(f"{r.migrated_scalars} scalar→mapping")
                if details:
                    print("         " + ", ".join(details))

            for warning in r.warnings:
                print(f"         WARNING: {warning}")
            for error in r.errors:
                print(f"         ERROR:   {error}")

    if show_diff:
        print()
        print("-" * 72)
        print("Unified diff preview")
        print("-" * 72)
        for r in results:
            if r.changed and not r.errors:
                print_diff_preview(r, root)

    print()
    if error_count:
        print("RESULT: migration NOT safe — no files should be committed.")
        return 1

    if apply:
        print("RESULT: migration applied successfully.")
        print("Next recommended check:")
        print("    git diff --stat -- explorer/scenarios")
        print("    git diff -- explorer/scenarios")
    else:
        print("RESULT: dry run successful — no file was modified.")
        print("To inspect exact changes:")
        print("    python scripts/migrate_scenarios_v3.py --diff")
        print("To apply:")
        print("    python scripts/migrate_scenarios_v3.py --apply")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate LlmExpl scenario YAML files to Scenario YAML v1."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("explorer/scenarios"),
        help="scenario directory (default: explorer/scenarios)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write migrated files; default is dry run",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="show per-file migration details",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="show unified diff preview without modifying files",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.exists():
        print(f"ERROR: scenario directory does not exist: {root}", file=sys.stderr)
        return 2

    files = discover_files(root)
    if not files:
        print(f"ERROR: no YAML scenario files found under: {root}", file=sys.stderr)
        return 2

    results = [process_file(path, apply=args.apply) for path in files]
    return print_report(
        results, root, args.apply, args.verbose, args.diff
    )


if __name__ == "__main__":
    raise SystemExit(main())
