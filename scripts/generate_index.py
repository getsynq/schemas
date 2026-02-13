"""Generate index.html for SYNQ JSON Schema documentation site."""

import json
import sys
from pathlib import Path

from jinja2 import Template

TEMPLATE = Template("""\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>SYNQ JSON Schemas</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #333; }
    h1 { border-bottom: 2px solid #eee; padding-bottom: 10px; }
    .schema-list { list-style: none; padding: 0; }
    .schema-list li { padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
    .schema-list a { text-decoration: none; color: #0366d6; font-weight: 500; }
    .schema-list a:hover { text-decoration: underline; }
    .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-left: 8px; }
    .badge-draft { background: #fff3cd; color: #856404; }
    .badge-stable { background: #d4edda; color: #155724; }
    .schema-desc { color: #666; font-size: 14px; margin-top: 4px; }
  </style>
</head>
<body>
  <h1>SYNQ JSON Schemas</h1>
  <p>Public JSON Schema definitions for SYNQ tools and services.</p>
  <h2>Available Schemas</h2>
  <ul class="schema-list">
  {%- for s in schemas %}
    <li>
      <a href="{{ s.html_path }}">{{ s.title }}</a> <span class="badge badge-{{ s.status }}">{{ s.status }}</span>
      <br><a href="{{ s.rel_path }}" style="font-size:13px;color:#666;">{{ s.rel_path }}</a>
      {%- if s.description %}
      <div class="schema-desc">{{ s.description }}</div>
      {%- endif %}
    </li>
  {%- endfor %}
  </ul>
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
    output.write_text(TEMPLATE.render(schemas=schemas))
    print(f"Generated {output} with {len(schemas)} schemas")


if __name__ == "__main__":
    main()
