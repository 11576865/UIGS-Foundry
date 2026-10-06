#!/usr/bin/env python3
from __future__ import annotations
import json, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_ui_search_index as b
import query_ui_patterns as q

INDEX,_=b.build()

class QueryTests(unittest.TestCase):
    def top(self,text):
        results=q.query(text,INDEX,3)
        self.assertTrue(results)
        return results[0]["id"]

    def test_exact_sticky_alias(self):
        self.assertEqual(self.top("右边停住左边滚"),"UIGS.WORKSPACE.STICKY_SUPPORTING_PANE")

    def test_preview_inspector_language(self):
        self.assertEqual(self.top("大预览 右侧 参数检查器"),"UIGS.COMPOSITION.PREVIEW_INSPECTOR_SPLIT")

    def test_scope_language(self):
        self.assertEqual(self.top("当前修改谁，会影响多少条"),"UIGS.WORKSPACE.SCOPE_TRANSPARENCY")

    def test_progressive_advanced_controls(self):
        self.assertEqual(self.top("高级参数折叠"),"UIGS.INSPECTOR.PROGRESSIVE_CONTROL_DISCLOSURE")

    def test_quarantined_pattern_hidden_by_default(self):
        index={"patterns":[{
            "id":"UIGS.TEST.QUARANTINED",
            "status":"canonical",
            "effective_authority":"quarantined",
            "name":{"zh":"隔离测试","en":"Quarantine Test"},
            "aliases":["隔离测试"],
            "intent":"test",
            "search_terms":["隔离测试"],
            "realizations":{},
            "validation":[],
        }]}
        self.assertEqual(q.query("隔离测试",index,3),[])
        results=q.query("隔离测试",index,3,include_quarantined=True)
        self.assertEqual(results[0]["id"],"UIGS.TEST.QUARANTINED")

if __name__=="__main__":
    unittest.main()
