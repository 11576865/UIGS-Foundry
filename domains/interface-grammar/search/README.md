# Interface Grammar Search

This directory is the deterministic retrieval layer for UIGS patterns.

The committed `index.json` is generated from semantic Pattern files. It exposes:

- stable Pattern ID;
- Chinese/English names;
- natural-language aliases;
- intent and use conditions;
- platform realizations;
- validation contracts;
- visual-showcase availability.

Use:

```bash
python tools/query_ui_patterns.py "右边停住左边滚"
python tools/query_ui_patterns.py "大预览 右侧 参数检查器" --json
```

The current resolver is lexical/structural rather than an embedding service. Exact aliases and explicit terminology receive high weight; Chinese character bigrams and token overlap provide fuzzy fallback.

Retrieval does not promote maturity. Experimental patterns remain Experimental even when they are the best match.
