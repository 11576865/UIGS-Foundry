#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT_JSON=ROOT/"reports"/"generated"/"ui-knowledge-coverage.json"
OUT_MD=ROOT/"reports"/"generated"/"ui-knowledge-coverage.md"

def load(path:Path,default:Any=None)->Any:
    if not path.is_file():return default
    return json.loads(path.read_text(encoding="utf-8"))

def build()->dict[str,Any]:
    patterns=load(ROOT/"domains/interface-grammar/search/index.json",{})
    inventory=load(ROOT/"domains/interface-grammar/inventory/coverage.json",{})
    realizations=load(ROOT/"domains/interface-grammar/realizations/coverage.json",{})
    showcases=load(ROOT/"domains/interface-grammar/showcases/coverage.json",{})
    visual=load(ROOT/"domains/interface-grammar/visual-evidence/coverage.json",{})
    state=load(ROOT/"reports/generated/ui-realization-state.json",{"realizations":[]})
    realization_rows=state.get("realizations",[])
    recipe_count=len(list((ROOT/"domains/interface-grammar/compositions/recipes").glob("*.json")))
    return {
      "schema_version":1,
      "pattern_count":int(patterns.get("pattern_count",0)),
      "composition_recipe_count":recipe_count,
      "source_inventory":{"covered":int(inventory.get("with_ui_inventory",0)),"total":int(inventory.get("sources_total",0)),"declared_empty":inventory.get("declared_empty_ui",[])},
      "concrete_surfaces":{"total":int(inventory.get("total_surfaces",0)),"pattern_linked":int(inventory.get("with_pattern_links",0)),"with_production_visual_evidence":int(visual.get("with_production_visual_evidence",0))},
      "production_realization_pattern_coverage":{"covered":int(realizations.get("with_production_implementation",0)),"total":int(realizations.get("total_patterns",0))},
      "reference_demo_pattern_coverage":{"covered":int(showcases.get("with_reference_demo",0)),"total":int(showcases.get("total_patterns",0))},
      "visual_baseline_pattern_coverage":{"covered":int(showcases.get("with_visual_baseline",0)),"total":int(showcases.get("total_patterns",0))},
      "realization_currentness":{"records":len(realization_rows),"source_content_current":sum(x.get("source_content_current") is True for x in realization_rows),"revision_equals_head":sum(x.get("head_matches_revision") is True for x in realization_rows)}
    }

def markdown(d:dict[str,Any])->str:
    inv=d["source_inventory"];sur=d["concrete_surfaces"];prod=d["production_realization_pattern_coverage"];demo=d["reference_demo_pattern_coverage"];base=d["visual_baseline_pattern_coverage"];cur=d["realization_currentness"]
    return "\n".join([
      "# UI Knowledge Coverage","",
      "| Layer | Coverage |","| --- | ---: |",
      f"| Reusable Patterns | {d['pattern_count']} |",
      f"| Composition Recipes | {d['composition_recipe_count']} |",
      f"| Source-owned project inventories | {inv['covered']}/{inv['total']} |",
      f"| Concrete product surfaces | {sur['total']} |",
      f"| Concrete surfaces linked to Patterns | {sur['pattern_linked']}/{sur['total']} |",
      f"| Pattern production-realization coverage | {prod['covered']}/{prod['total']} |",
      f"| Pattern reference-demo coverage | {demo['covered']}/{demo['total']} |",
      f"| Pattern visual-baseline coverage | {base['covered']}/{base['total']} |",
      f"| Concrete surfaces with production visual evidence | {sur['with_production_visual_evidence']}/{sur['total']} |",
      f"| Realization source content current | {cur['source_content_current']}/{cur['records']} |",
      f"| Realization revision exactly equals repo HEAD | {cur['revision_equals_head']}/{cur['records']} |",
      "","## Interpretation","",
      "- Pattern, concrete Surface, Production Realization, Reference Demo, Visual Baseline and Production Visual Evidence are distinct layers.",
      "- A product can be fully inventoried with zero built-in UI surfaces; this is different from missing inventory.",
      "- Revision != HEAD is not itself implementation staleness. Path-content currentness is the implementation signal.",
      "- The largest current evidence gap is production visual evidence for concrete product surfaces.",""
    ])

def main()->int:
    data=build();OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");OUT_MD.write_text(markdown(data),encoding="utf-8")
    print(f"UI knowledge coverage: patterns={data['pattern_count']}; surfaces={data['concrete_surfaces']['total']}")
    return 0
if __name__=="__main__":raise SystemExit(main())
