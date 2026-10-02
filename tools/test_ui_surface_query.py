#!/usr/bin/env python3
from __future__ import annotations
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));import query_ui_surfaces as q
INDEX={"surfaces":[
 {"id":"ASS.TOOL.FONTS","name":"字体管理","kind":"tool","group":"RESOURCES","intent":"导入字体","implementation_effect":"管理字体资源","patterns":[],"project":"ASS","repository":"o/a","platform":"android","source_refs":[],"visual_evidence":[]},
 {"id":"MKV.STAGE.OUTPUT_HUB","name":"检查与封装","kind":"supporting-pane","group":"OUTPUT","intent":"检查输出并封装","implementation_effect":"自适应输出区","patterns":[],"project":"MKV","repository":"o/m","platform":"web","source_refs":[],"visual_evidence":[]},
 {"id":"HSR.WORKSPACE.LAYOUT","name":"字幕样式工作台","kind":"workspace","group":"LAYOUT","intent":"字幕样式","implementation_effect":"预览加检查器","patterns":[],"project":"HSR","repository":"o/h","platform":"web","source_refs":[],"visual_evidence":[]}
]}
class QueryTests(unittest.TestCase):
    def top(self,text):return q.query(text,INDEX,3)[0]["id"]
    def test_fonts(self):self.assertEqual(self.top("字体管理"),"ASS.TOOL.FONTS")
    def test_output_hub(self):self.assertEqual(self.top("检查与封装"),"MKV.STAGE.OUTPUT_HUB")
    def test_layout(self):self.assertEqual(self.top("字幕样式工作台"),"HSR.WORKSPACE.LAYOUT")
if __name__=="__main__":unittest.main()
