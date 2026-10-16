#!/usr/bin/env python3
"""Explicit, temporary-file-only side-effect evidence demonstration."""
from pathlib import Path
from tempfile import TemporaryDirectory
from code_atlas_causality import mark, observe_file, operation


def make_artifact(path: Path):
    path.write_bytes(b"code-atlas-test-fixture")


def run_demo():
    with TemporaryDirectory(prefix="uigs-atlas-proof-") as tmp:
        artifact = Path(tmp) / "result.bin"
        with operation("Temporary artifact"):
            mark("action", "create fixture")
            with observe_file("demo:artifact", artifact):
                make_artifact(artifact)


if __name__ == "__main__":
    run_demo()
