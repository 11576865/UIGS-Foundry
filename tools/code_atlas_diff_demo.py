#!/usr/bin/env python3
"""Explicitly chosen, deterministic success/failure evidence fixture."""
import sys
from code_atlas_causality import mark, operation, observe_state


def successful_path(value: int) -> int:
    return value + 1


def failing_path(value: int) -> int:
    return value - 1


def run() -> None:
    state = {"count": 0}
    with operation("Code Atlas comparison example"):
        mark("action", "start comparison fixture")
        with observe_state("fixture:count", lambda: state):
            if "--fail" in sys.argv:
                state["count"] = failing_path(3)
                raise RuntimeError("deliberate synthetic failure")
            state["count"] = successful_path(3)


if __name__ == "__main__":
    run()
