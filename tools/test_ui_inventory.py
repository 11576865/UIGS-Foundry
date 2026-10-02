#!/usr/bin/env python3
from __future__ import annotations
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import collect_ui_inventory as c
class InventoryTests(unittest.TestCase):
    def sample(self):
        adapter={"project":"P","ui_inventory":{"path":".uigs/ui-surfaces.json","authority":"this repository"}}
        inv={"project":"P","repository":"o/r","platform":"web","surface_count":1,"surfaces":[{"id":"P.X","kind":"panel","name":"X","status":"implemented","intent":"x","implementation_effect":"y","source_refs":[{"path":"index.html"}],"patterns":[],"visual_evidence":[]}]}
        return adapter,inv
    def test_count_must_match(self):
        adapter,inv=self.sample();inv["surface_count"]=2
        with self.assertRaises(ValueError):c.normalize_inventory("o/r","main","abc",adapter,inv)
    def test_normalize_attaches_source_head(self):
        adapter,inv=self.sample();source,items=c.normalize_inventory("o/r","main","abc",adapter,inv)
        self.assertEqual(source["surface_count"],1);self.assertEqual(items[0]["source_head"],"abc")
    def test_coverage_distinguishes_missing_inventory(self):
        sources=[{"repository":"o/a","status":"available"},{"repository":"o/b","status":"ui-inventory-missing"}]
        surfaces=[{"id":"A","project":"P","kind":"panel","patterns":[],"visual_evidence":[]}]
        cov=c.build_coverage(sources,surfaces);self.assertEqual(cov["with_ui_inventory"],1);self.assertEqual(cov["total_surfaces"],1)
if __name__=="__main__":unittest.main()
