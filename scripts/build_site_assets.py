#!/usr/bin/env python3
"""Build deterministic SEO/GEO metadata and agent-facing CRD assets."""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONFIG = json.loads((ROOT / "site" / "pages.json").read_text(encoding="utf-8"))
SITE = CONFIG["site"]
PAGES = CONFIG["pages"]


def relative_prefix(file_name: str) -> str:
    return "../" if "/" in file_name else ""


def breadcrumb(page: dict[str, str]) -> list[dict[str, object]]:
    items: list[dict[str, object]] = [
        {"@type": "ListItem", "position": 1, "name": "CRD", "item": SITE["url"]}
    ]
    if page["file"] != "index.html":
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": page["title"].split(" | ")[0].split(" — ")[0],
                "item": page["url"],
            }
        )
    return items


def structured_data(page: dict[str, str]) -> dict[str, object]:
    page_id = f'{page["url"]}#webpage'
    graph: list[dict[str, object]] = [
        {
            "@type": "WebSite",
            "@id": f'{SITE["url"]}#website',
            "url": SITE["url"],
            "name": SITE["name"],
            "alternateName": SITE["alternateName"],
            "inLanguage": "en",
            "publisher": {"@id": f'{SITE["authorUrl"]}#person'},
        },
        {
            "@type": "Person",
            "@id": f'{SITE["authorUrl"]}#person',
            "name": SITE["author"],
            "url": SITE["authorUrl"],
            "sameAs": SITE["sameAs"],
        },
    ]
    page_node: dict[str, object] = {
        "@type": page["type"],
        "@id": page_id,
        "url": page["url"],
        "name": page["title"],
        "headline": page["title"],
        "description": page["description"],
        "inLanguage": "en",
        "isPartOf": {"@id": f'{SITE["url"]}#website'},
        "author": {"@id": f'{SITE["authorUrl"]}#person'},
        "creator": {"@id": f'{SITE["authorUrl"]}#person'},
        "dateModified": SITE["modified"],
        "license": SITE["license"],
        "image": SITE["image"],
    }
    if page["type"] == "TechArticle":
        page_node["proficiencyLevel"] = "Beginner to advanced"
        page_node["version"] = SITE["specificationVersion"]
    graph.append(page_node)
    if page["file"] != "index.html":
        graph.append(
            {
                "@type": "BreadcrumbList",
                "@id": f'{page["url"]}#breadcrumb',
                "itemListElement": breadcrumb(page),
            }
        )
    return {"@context": "https://schema.org", "@graph": graph}


def metadata_block(page: dict[str, str]) -> str:
    prefix = relative_prefix(page["file"])
    og_type = "article" if page["type"] == "TechArticle" else "website"
    markdown = ""
    if page.get("markdown"):
        markdown = (
            f'    <link rel="alternate" type="text/markdown" '
            f'href="{prefix}{html.escape(page["markdown"])}" title="Markdown version" />\n'
        )
    data = json.dumps(structured_data(page), ensure_ascii=False, indent=2)
    return f'''    <!-- site-meta:start -->
    <title>{html.escape(page["title"])}</title>
    <meta name="description" content="{html.escape(page["description"], quote=True)}" />
    <link rel="canonical" href="{page["url"]}" />
{markdown}    <meta property="og:type" content="{og_type}" />
    <meta property="og:site_name" content="{SITE["name"]}" />
    <meta property="og:title" content="{html.escape(page["title"], quote=True)}" />
    <meta property="og:description" content="{html.escape(page["description"], quote=True)}" />
    <meta property="og:url" content="{page["url"]}" />
    <meta property="og:image" content="{SITE["image"]}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(page["title"], quote=True)}" />
    <meta name="twitter:description" content="{html.escape(page["description"], quote=True)}" />
    <meta name="twitter:image" content="{SITE["image"]}" />
    <script id="site-structured-data" type="application/ld+json">
{data}
    </script>
    <!-- site-meta:end -->'''


def clean_existing_metadata(text: str) -> str:
    text = re.sub(r"\s*<!-- site-meta:start -->.*?<!-- site-meta:end -->", "", text, flags=re.S)
    patterns = [
        r"\s*<title>.*?</title>",
        r'\s*<meta\s+name="description"[^>]*?/?>',
        r'\s*<link\s+rel="canonical"[^>]*?/?>',
        r'\s*<link\s+rel="alternate"\s+type="text/markdown"[^>]*?/?>',
        r'\s*<meta\s+property="og:[^"]+"[^>]*?/?>',
        r'\s*<meta\s+name="twitter:[^"]+"[^>]*?/?>',
        r'\s*<script\s+id="site-structured-data".*?</script>',
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.S | re.I)
    return text


def visible_metadata(page: dict[str, str]) -> str:
    source = ""
    if page.get("source"):
        source_url = f'https://github.com/valto/crd/blob/main/{page["source"]}'
        source = f' · <a href="{source_url}">Canonical source</a>'
    return f'''<!-- document-meta:start -->
      <aside class="document-meta shell" aria-label="Document provenance">
        <p><strong>{html.escape(page["classification"])}</strong> · Specification {SITE["specificationVersion"]} · Package {SITE["packageVersion"]} · Updated {SITE["modified"]} · {SITE["author"]}{source}</p>
      </aside>
<!-- document-meta:end -->'''


def breadcrumb_html(page: dict[str, str]) -> str:
    if page["file"] == "index.html":
        return ""
    prefix = relative_prefix(page["file"])
    label = html.escape(page["title"].split(" | ")[0].split(" — ")[0])
    return f'''<!-- breadcrumbs:start -->
    <nav class="breadcrumbs shell" aria-label="Breadcrumb">
      <a href="{prefix}index.html">CRD</a><span aria-hidden="true">/</span><span aria-current="page">{label}</span>
    </nav>
<!-- breadcrumbs:end -->'''


def update_html(page: dict[str, str]) -> None:
    path = DOCS / page["file"]
    text = clean_existing_metadata(path.read_text(encoding="utf-8"))
    def normalize_brand_image(match: re.Match[str]) -> str:
        source = re.search(r'src="([^"]+)"', match.group(0))
        if not source:
            raise ValueError(f"{page['file']}: brand image missing src")
        return f'<img class="brand-mark" src="{source.group(1)}" alt="" width="29" height="29" />'

    text = re.sub(r'<img class="brand-mark"[^>]*>', normalize_brand_image, text)
    if page["file"] == "agent-prompt.html":
        prompt = (DOCS / "agent-prompt.txt").read_text(encoding="utf-8").strip()
        text, count = re.subn(
            r'(<textarea id="crd-agent-prompt"[^>]*>).*?(</textarea>)',
            lambda match: match.group(1) + html.escape(prompt) + match.group(2),
            text,
            count=1,
            flags=re.S,
        )
        if count != 1:
            raise ValueError("agent-prompt.html: prompt textarea not found")
    text = re.sub(r"\s*<!-- breadcrumbs:start -->.*?<!-- breadcrumbs:end -->", "", text, flags=re.S)
    text = re.sub(r"\s*<!-- document-meta:start -->.*?<!-- document-meta:end -->", "", text, flags=re.S)
    viewport = re.search(r'<meta\s+name="viewport"[^>]*?/?>', text, flags=re.I)
    if not viewport:
        raise ValueError(f"{page['file']}: missing viewport meta")
    text = text[: viewport.end()] + "\n" + metadata_block(page) + text[viewport.end() :]
    crumbs = breadcrumb_html(page)
    if crumbs:
        text = text.replace("<main", f"{crumbs}\n    <main", 1)
    provenance = visible_metadata(page)
    text = text.replace("</main>", f"{provenance}\n    </main>", 1)
    path.write_text(text, encoding="utf-8")


def copy_file(source: str, destination: str) -> None:
    target = DOCS / destination
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / source, target)


def build_agent_assets() -> None:
    copies = {
        "README.md": "index.md",
        "crd-specification.md": "specification.md",
        "crd-template.md": "template.md",
        "agent-transformation-instructions.md": "agent-transformation.md",
        "working-with-crds.md": "working-with-crds.md",
        "minimum-logical-element.md": "mle.md",
        "capability-inventory.md": "inventory.md",
        "source-context-template.md": "source-context.md",
        "crd-vs-prd.md": "crd-vs-prd.md",
        "glossary.md": "glossary.md",
        "agent-prompt.md": "agent-prompt.md",
        "schema/crd.schema.json": "schema/crd.schema.json",
        "skills/crd-author/SKILL.md": "skills/crd-author/SKILL.md",
    }
    for source, destination in copies.items():
        copy_file(source, destination)
    for path in sorted((ROOT / "examples").glob("*")):
        if path.suffix in {".md", ".json"}:
            copy_file(str(path.relative_to(ROOT)), f"examples/{path.name}")
    prompt = (ROOT / "agent-prompt.md").read_text(encoding="utf-8")
    match = re.search(r"```text\n(.*?)\n```", prompt, flags=re.S)
    if not match:
        raise ValueError("agent-prompt.md: missing text code block")
    (DOCS / "agent-prompt.txt").write_text(match.group(1).strip() + "\n", encoding="utf-8")

    llms_sections: dict[str, list[dict[str, str]]] = {
        "Start here": [],
        "Normative and practical guidance": [],
        "Templates and machine-readable resources": [],
        "Examples": [],
    }
    for page in PAGES:
        item = {
            "title": page["title"].split(" | ")[0],
            "url": SITE["url"] + page["markdown"] if page.get("markdown") else page["url"],
            "description": page["description"],
        }
        if page["file"] in {"index.html", "learn.html", "why-crd.html", "crd-vs-prd.html"}:
            llms_sections["Start here"].append(item)
        elif page["file"].startswith("examples/"):
            llms_sections["Examples"].append(item)
        elif page["classification"] in {"Template", "Agent resource", "Controlled vocabulary"}:
            llms_sections["Templates and machine-readable resources"].append(item)
        else:
            llms_sections["Normative and practical guidance"].append(item)

    lines = [
        f'# {SITE["name"]} ({SITE["alternateName"]})',
        "",
        "> Capability Documentation is an open, technology-agnostic framework. A Capability Requirements Document specifies one complete Capability MLE for people, agents, applications, and developers.",
        "",
        f'- Specification status: {SITE["specificationVersion"]}',
        f'- Package release: {SITE["packageVersion"]}',
        f'- Creator and steward: [{SITE["author"]}]({SITE["authorUrl"]})',
        f'- License: [CC BY 4.0]({SITE["license"]})',
        '- Canonical repository: [github.com/valto/crd](https://github.com/valto/crd)',
    ]
    for section, items in llms_sections.items():
        if not items:
            continue
        lines.extend(["", f"## {section}", ""])
        for item in items:
            lines.append(f'- [{item["title"]}]({item["url"]}): {item["description"]}')
    lines.extend(
        [
            "",
            "## Direct machine-readable resources",
            "",
            f'- [CRD JSON Schema]({SITE["url"]}schema/crd.schema.json): Validation schema for structured CRDs.',
            f'- [CRD Author skill]({SITE["url"]}skills/crd-author/SKILL.md): Define and Extract workflows for capable agents.',
            f'- [Agent prompt]({SITE["url"]}agent-prompt.txt): Plain-text agent onboarding prompt.',
        ]
    )
    (DOCS / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    full_sources = [
        ("Framework overview", DOCS / "index.md"),
        ("CRD specification", DOCS / "specification.md"),
        ("CRD template", DOCS / "template.md"),
        ("Agent transformation", DOCS / "agent-transformation.md"),
        ("Working with CRDs", DOCS / "working-with-crds.md"),
        ("Minimum Logical Element", DOCS / "mle.md"),
        ("Glossary", DOCS / "glossary.md"),
        ("CRD versus PRD", DOCS / "crd-vs-prd.md"),
        ("Agent prompt", DOCS / "agent-prompt.md"),
    ]
    full = [
        f'# {SITE["name"]} ({SITE["alternateName"]}) — full context',
        "",
        f'Generated {SITE["modified"]} from canonical repository sources. Specification status: {SITE["specificationVersion"]}. Package release: {SITE["packageVersion"]}.',
    ]
    for label, path in full_sources:
        full.extend(["", "---", "", f"# Source: {label}", f"URL: {SITE['url']}{path.relative_to(DOCS)}", "", path.read_text(encoding="utf-8").strip()])
    (DOCS / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")


def build_sitemap() -> None:
    rows = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in PAGES:
        rows.extend(
            [
                "  <url>",
                f'    <loc>{page["url"]}</loc>',
                f'    <lastmod>{SITE["modified"]}</lastmod>',
                f'    <priority>{page["priority"]}</priority>',
                "  </url>",
            ]
        )
    rows.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    build_agent_assets()
    for page in PAGES:
        update_html(page)
    build_sitemap()
    print(f"built {len(PAGES)} pages and agent assets")


if __name__ == "__main__":
    main()
