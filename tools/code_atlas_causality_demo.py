#!/usr/bin/env python3
"""Safe opt-in operation illustration; no external effects."""
from code_atlas_causality import mark, operation, observe_state


def compute_value(value: int) -> int:
    return value * 2


def calculate() -> int:
    state = {"result": None}
    with operation("Example calculation"):
        mark("action", "execute example")
        with observe_state("example:result", lambda: state):
            state["result"] = compute_value(3)
        mark("checkpoint", "result calculated", subject="example:result")
        return state["result"]


if __name__ == "__main__":
    assert calculate() == 6
