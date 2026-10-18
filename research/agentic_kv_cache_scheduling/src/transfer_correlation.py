"""Stable transfer identifiers for the SGLang event adapter."""
from __future__ import annotations


def transfer_id(direction: str, operation_id: int) -> str:
    if direction not in {"prefetch", "load_back", "backup"}:
        raise ValueError(f"unsupported transfer direction: {direction}")
    if int(operation_id) < 0:
        raise ValueError("operation_id must be non-negative")
    return f"{direction}-{int(operation_id)}"


def correlate_start_complete(direction: str, operation_id: int) -> tuple[str, str]:
    identifier = transfer_id(direction, operation_id)
    return identifier, identifier
