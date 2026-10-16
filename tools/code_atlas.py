#!/usr/bin/env python3
"""Read-only, source-anchored Python code map for UIGS.

No AI-inferred edges: nodes and relationships come from Python AST.
Unresolved/dynamic calls are counted, not silently invented as edges.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

THIS = Path(__file__).resolve()
WEB = THIS.parent / "code_atlas_web" / "index.html"
IGNORE = {".git", ".venv", "venv", "node_modules", "__pycache__", "build", "dist"}
MAX_FILE_BYTES = 1_000_000


def revision_for(root: Path) -> str | None:
    try:
        v = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, timeout=3).decode().strip()
        if not re.fullmatch(r"[0-9a-f]{40}", v):
            return None
        # A dirty checkout cannot truthfully claim line anchors at HEAD.
        dirty = subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], stderr=subprocess.DEVNULL, timeout=3).strip()
        return None if dirty else v
    except (OSError, subprocess.SubprocessError):
        return None


def python_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.py") if p.is_file() and not set(p.relative_to(root).parts).intersection(IGNORE) and p.stat().st_size <= MAX_FILE_BYTES)


def source_url(repo: str | None, sha: str | None, rel: str, line: int = 0) -> str | None:
    if not repo or not sha or not re.fullmatch(r"[0-9a-f]{40}", sha):
        return None
    return f"https://github.com/{repo}/blob/{sha}/{quote(rel, safe='/')}" + (f"#L{line}" if line else "")


def index(root: Path, repo: str | None = None, revision: str | None = None) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")
    revision = revision or revision_for(root)
    nodes: list[dict] = []
    edges: list[dict] = []
    parsed: list[tuple[str, ast.Module]] = []
    symbol_index: dict[tuple[str, str], str] = {}
    module_aliases: dict[str, str] = {}
    errors: list[dict] = []
    unresolved = Counter()

    files = python_files(root)
    for path in files:
        rel = path.relative_to(root).as_posix()
        module = rel[:-3].replace("/", ".")
        if module.endswith(".__init__"):
            module = module[:-9]
        module_aliases[module] = rel
        module_aliases[module.rsplit(".", 1)[-1]] = rel  # resolution checked for ambiguity below
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=rel)
        except (SyntaxError, UnicodeError) as ex:
            errors.append({"path": rel, "error": str(ex)})
            continue
        parsed.append((rel, tree))
        nodes.append({"id": f"file:{rel}", "kind": "file", "label": path.name, "path": rel, "line": 1, "url": source_url(repo, revision, rel, 1)})

        def defs(body: list[ast.stmt], prefix: str = "") -> None:
            for stmt in body:
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    qual = prefix + stmt.name
                    ident = f"fn:{rel}:{qual}"
                    symbol_index[(rel, qual)] = ident
                    nodes.append({"id": ident, "kind": "function", "label": qual + "()", "path": rel, "line": stmt.lineno, "url": source_url(repo, revision, rel, stmt.lineno)})
                    edges.append({"from": f"file:{rel}", "to": ident, "kind": "declares", "evidence": "ast_definition", "path": rel, "line": stmt.lineno})
                elif isinstance(stmt, ast.ClassDef):
                    defs(stmt.body, prefix + stmt.name + ".")
        defs(tree.body)

    # Never resolve an ambiguous module tail to an arbitrary repository file.
    tails: dict[str, list[str]] = {}
    for rel, _ in parsed:
        tails.setdefault(Path(rel).stem, []).append(rel)
    for tail, paths in tails.items():
        if len(paths) > 1:
            module_aliases.pop(tail, None)

    for rel, tree in parsed:
        aliases: dict[str, tuple[str, str | None]] = {}
        for stmt in tree.body:
            if isinstance(stmt, ast.Import):
                for item in stmt.names:
                    target = module_aliases.get(item.name) or module_aliases.get(item.name.rsplit(".", 1)[-1])
                    if target:
                        aliases[item.asname or item.name.split(".")[0]] = (target, None)
                        edges.append({"from": f"file:{rel}", "to": f"file:{target}", "kind": "imports", "evidence": "ast_import", "path": rel, "line": stmt.lineno})
            elif isinstance(stmt, ast.ImportFrom) and stmt.level == 0 and stmt.module:
                target = module_aliases.get(stmt.module) or module_aliases.get(stmt.module.rsplit(".", 1)[-1])
                if target:
                    edges.append({"from": f"file:{rel}", "to": f"file:{target}", "kind": "imports", "evidence": "ast_import", "path": rel, "line": stmt.lineno})
                    for item in stmt.names:
                        aliases[item.asname or item.name] = (target, item.name)

        def visit_function(fn: ast.FunctionDef | ast.AsyncFunctionDef, qual: str) -> None:
            src = symbol_index.get((rel, qual))
            if not src:
                return
            # Static calls are valid only for an unshadowed syntactic reference.
            parameters = {a.arg for a in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs}
            if fn.args.vararg:
                parameters.add(fn.args.vararg.arg)
            if fn.args.kwarg:
                parameters.add(fn.args.kwarg.arg)
            locally_bound = set(parameters)
            def walk_body():
                pending = list(fn.body)
                while pending:
                    item = pending.pop()
                    yield item
                    # Calls in a nested function have a different caller identity.
                    if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                        pending.extend(ast.iter_child_nodes(item))

            for item in walk_body():
                if isinstance(item, (ast.Assign, ast.AnnAssign, ast.NamedExpr, ast.For, ast.AsyncFor)):
                    targets = item.targets if isinstance(item, ast.Assign) else [item.target]
                    for t in targets:
                        locally_bound.update(x.id for x in ast.walk(t) if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store))
            for item in walk_body():
                if not isinstance(item, ast.Call):
                    continue
                target = None
                f = item.func
                if isinstance(f, ast.Name):
                    if f.id not in locally_bound:
                        target = symbol_index.get((rel, f.id))
                        if not target and f.id in aliases:
                            imported_rel, symbol = aliases[f.id]
                            if symbol:
                                target = symbol_index.get((imported_rel, symbol))
                elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                    if f.value.id not in locally_bound and f.value.id in aliases:
                        imported_rel, symbol = aliases[f.value.id]
                        if symbol is None:
                            target = symbol_index.get((imported_rel, f.attr))
                    elif f.value.id in {"self", "cls"} and "." in qual:
                        owner = qual.rsplit(".", 1)[0]
                        target = symbol_index.get((rel, owner + "." + f.attr))
                if target:
                    edges.append({"from": src, "to": target, "kind": "calls", "evidence": "ast_direct_call", "path": rel, "line": item.lineno})
                else:
                    unresolved[rel] += 1

        for stmt in tree.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit_function(stmt, stmt.name)
            elif isinstance(stmt, ast.ClassDef):
                for child in stmt.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        visit_function(child, stmt.name + "." + child.name)

    # Deduplicate repeated calls; preserve the first source line as inspectable evidence.
    unique: dict[tuple[str, str, str], dict] = {}
    for edge in edges:
        key = (edge["from"], edge["to"], edge["kind"])
        unique.setdefault(key, edge)
    return {
        "schema_version": 1,
        "generator": "tools/code_atlas.py:python_ast_v1",
        "repository": repo,
        "revision": revision,
        "limitations": ["Only Python sources are parsed", "Dynamic/reflection calls are not resolved", "Static edges are not runtime proof", "Names shadowed through complex closures may remain unresolved"],
        "nodes": sorted(nodes, key=lambda n: n["id"]),
        "edges": sorted(unique.values(), key=lambda e: (e["from"], e["to"], e["kind"])),
        "parse_errors": errors,
        "unresolved_call_sites": dict(unresolved),
        "stats": {"python_files": len(files), "parsed_files": len(parsed), "nodes": len(nodes), "edges": len(unique), "unresolved_calls": sum(unresolved.values())},
    }


def serve(root: Path, repo: str | None, host: str, port: int) -> None:
    graph = index(root, repo)
    html = WEB.read_bytes()
    payload = json.dumps(graph, ensure_ascii=False).encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path in {"/", "/index.html"}:
                body, ctype = html, "text/html; charset=utf-8"
            elif self.path == "/api/graph":
                body, ctype = payload, "application/json; charset=utf-8"
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

    with ThreadingHTTPServer((host, port), Handler) as server:
        print(f"Code Atlas: http://{host}:{server.server_port} — {len(graph['nodes'])} nodes", flush=True)
        server.serve_forever()


def main() -> None:
    p = argparse.ArgumentParser(description="UIGS read-only Code Atlas")
    p.add_argument("--root", type=Path, default=THIS.parents[1])
    p.add_argument("--repo", default="11576865/UIGS-Foundry")
    p.add_argument("--revision", help="Commit SHA for source anchors (autodetect from git by default)")
    p.add_argument("--output", type=Path, help="Write JSON to this path instead of stdout")
    p.add_argument("--serve", action="store_true", help="Open local read-only HTTP service")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    if args.serve:
        serve(args.root, args.repo, args.host, args.port)
    else:
        report = index(args.root, args.repo, args.revision)
        content = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
            print(f"{args.output}: {report['stats']}")
        else:
            print(content, end="")


if __name__ == "__main__":
    main()