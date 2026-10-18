#!/usr/bin/env python3
"""Statically map the event adapter to a pinned SGLang source checkout."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import sys


DEFAULT_ROOT = Path("/private/tmp/sglang-audit.0LSjXl")
FILES = {
    "unified_radix_cache": "python/sglang/srt/mem_cache/unified_radix_cache.py",
    "transfer_pipeline": "python/sglang/srt/mem_cache/buffer_mode/pipeline.py",
    "schedule_policy": "python/sglang/srt/managers/schedule_policy.py",
}
TARGETS = {
    "unified_radix_cache": ["UnifiedRadixCache", "load_back", "init_load_back",
                             "loading_check", "ongoing_prefetch", "ongoing_load_back",
                             "prefetch_threshold", "load_back_threshold"],
    "transfer_pipeline": ["PoolTransfer", "allocate_and_queue_prefetch",
                           "stage_completed_prefetch", "init_load_back",
                           "_transfer_tokens", "prefetch_buffer"],
    "schedule_policy": ["tree_cache", "finish_storage_prefetch_admission",
                         "discard_storage_prefetch_accounting", "build_hicache_transfers"],
}


def source_symbols(path: Path) -> dict[str, list[int]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    symbols: dict[str, list[int]] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.setdefault(node.name, []).append(node.lineno)
        elif isinstance(node, ast.Name):
            symbols.setdefault(node.id, []).append(node.lineno)
        elif isinstance(node, ast.Attribute):
            symbols.setdefault(node.attr, []).append(node.lineno)
    return {name: sorted(set(lines)) for name, lines in symbols.items()}


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    files = {}
    checks = []
    for label, relative in FILES.items():
        path = root / relative
        row = {"label": label, "path": str(path), "exists": path.exists()}
        if path.exists():
            symbols = source_symbols(path)
            row["targets"] = {
                target: {"present": target in symbols, "lines": symbols.get(target, [])}
                for target in TARGETS[label]
            }
            row["parse_error"] = None
        else:
            row["targets"] = {target: {"present": False, "lines": []}
                               for target in TARGETS[label]}
            row["parse_error"] = "missing source file"
        files[label] = row
        checks.extend(row["targets"].values())

    result = {
        "protocol": "SGLANG-EVENT-SURFACE-AUDIT-v1",
        "source_root": str(root),
        "source_commit": "3b34d9f8b6edc23216f29c1edf02d1ff0306f9de",
        "method": "Python AST only; no import, model load, CUDA or engine mutation",
        "files": files,
        "all_files_present": all(row["exists"] for row in files.values()),
        "target_presence": sum(item["present"] for item in checks),
        "target_count": len(checks),
    }
    out = Path(__file__).parents[1] / "results" / "sglang_event_surface_audit.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
