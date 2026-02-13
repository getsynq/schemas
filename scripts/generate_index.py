"""Generate index.html for SYNQ JSON Schema documentation site."""

import json
import sys
from pathlib import Path

from jinja2 import Template

TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SYNQ - JSON Schemas</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      -webkit-font-smoothing: antialiased;
      color: #261F3B;
      background: #f8fafc;
      min-height: 100vh;
    }
    .header {
      background: #261F3B;
      color: #fff;
      padding: 3rem 1.5rem 2.5rem;
    }
    .header-inner {
      max-width: 800px;
      margin: 0 auto;
    }
    .logo { margin-bottom: 1.25rem; }
    .header h1 {
      font-size: 1.75rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .header p {
      margin-top: 0.5rem;
      color: #a89bbe;
      font-size: 1rem;
    }
    .header a {
      color: #d4cbea;
      text-decoration: underline;
      text-underline-offset: 2px;
    }
    .header a:hover { color: #fff; }
    .content {
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem 1.5rem 4rem;
    }
    .section-label {
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94a3b8;
      margin-bottom: 0.75rem;
    }
    .schema-card {
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin-bottom: 0.5rem;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .schema-card:hover {
      border-color: #94a3b8;
      box-shadow: 0 1px 3px rgba(38, 31, 59, 0.06);
    }
    .schema-card-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .schema-card-title {
      font-size: 1rem;
      font-weight: 600;
      color: #261F3B;
      text-decoration: none;
    }
    .schema-card-title:hover { text-decoration: underline; }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 9999px;
      font-size: 0.6875rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .badge-stable { background: #ecfdf5; color: #065f46; }
    .badge-draft { background: #fefce8; color: #854d0e; }
    .schema-path {
      display: inline-block;
      margin-top: 0.25rem;
      font-size: 0.8125rem;
      font-family: "SF Mono", SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
      color: #64748b;
      text-decoration: none;
    }
    .schema-path:hover { color: #261F3B; }
    .schema-desc {
      margin-top: 0.375rem;
      font-size: 0.875rem;
      color: #475569;
      line-height: 1.5;
    }
    .schema-group + .schema-group { margin-top: 2rem; }
  </style>
</head>
<body>
  <div class="header">
    <div class="header-inner">
      <div class="logo"><img src="synq-logo.svg" width="92" height="24" alt="SYNQ"></div>
      <h1>JSON Schemas</h1>
      <p>Public JSON Schema definitions for SYNQ tools and services.</p>
      <p>See <a href="https://docs.synq.io/">docs.synq.io</a> for full documentation.</p>
    </div>
  </div>
  <div class="content">
  {%- for group in groups %}
    <div class="schema-group">
      <div class="section-label">{{ group.label }}</div>
      {%- for s in group.schemas %}
      <div class="schema-card">
        <div class="schema-card-header">
          <a class="schema-card-title" href="{{ s.html_path }}">{{ s.title }}</a>
          <span class="badge badge-{{ s.status }}">{{ s.status }}</span>
        </div>
        <a class="schema-path" href="{{ s.rel_path }}">{{ s.rel_path }}</a>
        {%- if s.description %}
        <div class="schema-desc">{{ s.description }}</div>
        {%- endif %}
      </div>
      {%- endfor %}
    </div>
  {%- endfor %}
  </div>
</body>
</html>
""")


def collect_schemas(root: Path) -> list[dict]:
    schemas = []
    for path in sorted(root.rglob("*.schema.json")):
        if ".github" in path.parts:
            continue
        rel = path.relative_to(root)
        with open(path) as f:
            data = json.load(f)
        base = path.name.removesuffix(".schema.json")
        html_path = str(rel.parent / f"{base}.html")
        schemas.append(
            {
                "rel_path": str(rel),
                "html_path": html_path,
                "title": data.get("title", base).removeprefix("SYNQ "),
                "status": data.get("x-status", "stable"),
                "description": data.get("description", ""),
            }
        )
    # Stable first, then draft; alphabetically by title within each group
    schemas.sort(key=lambda s: (s["status"] != "stable", s["title"]))
    return schemas


def main() -> None:
    root = Path.cwd()
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.html")
    schemas = collect_schemas(root)
    groups = []
    stable = [s for s in schemas if s["status"] == "stable"]
    draft = [s for s in schemas if s["status"] == "draft"]
    if stable:
        groups.append({"label": "Stable", "schemas": stable})
    if draft:
        groups.append({"label": "Draft", "schemas": draft})
    output.write_text(TEMPLATE.render(groups=groups))
    print(f"Generated {output} with {len(schemas)} schemas")


if __name__ == "__main__":
    main()
