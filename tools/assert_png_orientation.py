#!/usr/bin/env python3
from __future__ import annotations
import struct,sys
from pathlib import Path

def png_size(path:Path)->tuple[int,int]:
    raw=path.read_bytes()
    if len(raw)<24 or raw[:8]!=b"\x89PNG\r\n\x1a\n" or raw[12:16]!=b"IHDR":
        raise SystemExit(f"not a PNG: {path}")
    return struct.unpack(">II",raw[16:24])

if len(sys.argv)!=3 or sys.argv[2] not in {"landscape","portrait"}:
    raise SystemExit("usage: assert_png_orientation.py <png> <landscape|portrait>")
path=Path(sys.argv[1]);wanted=sys.argv[2];w,h=png_size(path)
ok=(w>h) if wanted=="landscape" else (h>w)
print(f"{path}: {w}x{h}; expected={wanted}")
if not ok:raise SystemExit(f"orientation mismatch: expected {wanted}, got {w}x{h}")
