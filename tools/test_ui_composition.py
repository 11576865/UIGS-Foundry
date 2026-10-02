#!/usr/bin/env python3
from __future__ import annotations
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_ui_search_index as bi
import query_ui_composition as qc
INDEX,_=bi.build();RECIPES=qc.load_recipes()

class CompositionTests(unittest.TestCase):
    def ids(self,q):
        return {x["id"] for x in qc.plan(q,INDEX,RECIPES)["patterns"]}
    def test_intent_split_keeps_multiple_ui_requests(self):
        parts=qc.split_intents("大预览 + 右侧检查器 + 高级参数折叠 + 当前修改谁影响多少条")
        self.assertGreaterEqual(len(parts),4)
    def test_complex_visual_editor_query_returns_multiple_patterns(self):
        ids=self.ids("做成大预览 + 右侧检查器 + 高级参数折叠 + 当前修改谁影响多少条")
        self.assertIn("UIGS.COMPOSITION.PREVIEW_INSPECTOR_SPLIT",ids)
        self.assertIn("UIGS.INSPECTOR.PROGRESSIVE_CONTROL_DISCLOSURE",ids)
        self.assertIn("UIGS.WORKSPACE.SCOPE_TRANSPARENCY",ids)
    def test_recipe_matches_visual_scoped_editor(self):
        plan=qc.plan("大预览右侧检查器，高级参数折叠，并显示当前修改谁和影响多少条",INDEX,RECIPES)
        self.assertTrue(plan["recipes"])
        self.assertEqual(plan["recipes"][0]["id"],"UIGS.RECIPE.VISUAL_SCOPED_EDITOR")
    def test_multi_instance_query_finds_catalog_binding_geometry(self):
        ids=self.ids("工具目录里打开多个独立工具窗口，每个固定不同对象，拖动窗口取消时恢复原位置")
        self.assertIn("UIGS.NAVIGATION.CAPABILITY_CATALOG",ids)
        self.assertIn("UIGS.WORKSPACE.EXPLICIT_TOOL_BINDING",ids)
        self.assertIn("UIGS.WORKSPACE.TRANSIENT_COMMITTED_SURFACE_GEOMETRY",ids)

if __name__=="__main__":unittest.main()
