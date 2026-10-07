#!/usr/bin/env python3
from pathlib import PurePosixPath, PureWindowsPath
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from build_visual_evidence_index import stable_path_sort

def names(items):
    return [p.name for p in stable_path_sort(items)]

def main():
    raw=[
        "VISUAL.PRODUCTION.ASS.FONT_REQUIREMENTS_TOOL.FIXTURE_LANDSCAPE.json",
        "VISUAL.PRODUCTION.ASS.FONTS_TOOL.FIXTURE_LANDSCAPE.json",
    ]
    expected=[
        "VISUAL.PRODUCTION.ASS.FONTS_TOOL.FIXTURE_LANDSCAPE.json",
        "VISUAL.PRODUCTION.ASS.FONT_REQUIREMENTS_TOOL.FIXTURE_LANDSCAPE.json",
    ]
    assert names([PurePosixPath(x) for x in raw])==expected
    assert names([PureWindowsPath(x) for x in raw])==expected
    assert names([PurePosixPath(x) for x in raw])==names([PureWindowsPath(x) for x in raw])
    print("visual evidence path ordering is platform-stable")

if __name__=="__main__":
    main()
