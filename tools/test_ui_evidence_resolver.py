#!/usr/bin/env python3
from __future__ import annotations
import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import query_ui_composition as composition
import resolve_ui_request as resolver
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/"domains/interface-grammar/search/index.json").read_text(encoding="utf-8"))
S=json.loads((ROOT/"domains/interface-grammar/inventory/index.json").read_text(encoding="utf-8"))
R=composition.load_recipes()

class ResolverTests(unittest.TestCase):
    def test_sticky_request_returns_real_product_surfaces(self):
        out=resolver.resolve("右边停住左边滚",P,S,R)
        ids={x["id"] for x in out["patterns"]};surfaces={x["id"] for x in out["concrete_surfaces"]}
        self.assertIn("UIGS.WORKSPACE.STICKY_SUPPORTING_PANE",ids)
        self.assertIn("MKV.STAGE.OUTPUT_HUB",surfaces)
        self.assertIn("QHE.STATUS.TASK_OVERVIEW",surfaces)

    def test_concrete_surface_can_lift_linked_patterns(self):
        out=resolver.resolve("字幕样式工作台",P,S,R)
        surfaces={x["id"] for x in out["concrete_surfaces"]};patterns={x["id"] for x in out["patterns"]}
        self.assertIn("HSR.WORKSPACE.LAYOUT",surfaces)
        self.assertIn("UIGS.COMPOSITION.PREVIEW_INSPECTOR_SPLIT",patterns)
        self.assertIn("UIGS.INSPECTOR.PROGRESSIVE_CONTROL_DISCLOSURE",patterns)

    def test_resolver_exposes_implementation_and_visual_gap_separately(self):
        out=resolver.resolve("检查与封装",P,S,R)
        self.assertTrue(out["production_realizations"])
        self.assertTrue(any(x["kind"]=="production-visual-evidence" for x in out["evidence_gaps"]))

if __name__=="__main__":unittest.main()
