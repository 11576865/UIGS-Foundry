# Cross-project UI Surface Inventory

Sources with inventory: 3/5
Concrete surfaces: 46
Pattern-linked surfaces: 19
Surfaces with production visual evidence: 0

| Project | Repository | Source HEAD | Status | Surfaces |
| --- | --- | --- | --- | ---: |
| ASS-Workbench-Android | 11576865/ASS-Workbench-Android | 818a26d202 | available | 23 |
| Character-Voice-Service | 11576865/Character-Voice-Service | 747e7998cb | ui-inventory-missing | 0 |
| HSR-Voice-Archive-Builder | 11576865/HSR-Voice-Archive-Builder | 62df3afe48 | available | 11 |
| MKV-Fast-Muxer | 11576865/MKV-Fast-Muxer | f2a29c0b3e | available | 12 |
| Quick-Automatic-Hardsub-Encoder | 11576865/Quick-Automatic-Hardsub-Encoder | d62dd49637 | ui-inventory-missing | 0 |

## Boundary

- Concrete UI inventory is authoritative in each source repository; Foundry stores a derived cross-project index.
- A surface may link zero or more reusable UIGS Patterns. Absence of a Pattern link does not make the concrete UI nonexistent.
- Source references describe implementation location; production screenshots/recordings are a separate visual-evidence field.
- Missing visual evidence remains explicit and is never substituted with Foundry reference-demo screenshots.
