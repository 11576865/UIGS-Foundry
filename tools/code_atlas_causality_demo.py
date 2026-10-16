#!/usr/bin/env python3
"""Safe opt-in operation illustration; no external effects."""
from code_atlas_causality import mark, operation


def compute_value(value: int) -> int:
    return value * 2


def calculate() -> int:
    with operation("Example calculation"):
        mark("action", "execute example")
        result = compute_value(3)
        mark("checkpoint", "result calculated", subject="example:result")
        return result


if __name__ == "__main__":
    assert calculate() == 6
