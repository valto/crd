#!/usr/bin/env python3
"""Validate CRD site SEO, GEO, links, and generated endpoint consistency."""

from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CONFIG = json.loads((ROOT / "site" / "pages.json").read_text(encoding="utf-8"))
SITE = CONFIG["site"]
PAGES = CONFIG["pages"]
ERRORS: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.h1 = 0
        self.ids: list[str] = []
        self.links: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.link_tags: list[dict[str, str]] = []
        self.json_ld: list[str] = []
        self.in_json_ld = False
        self.json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.link_tags.append(values)
        elif tag in {"a", "img", "script", "source", "object"}:
            key = {"a": "href", "img": "src", "script": "src", "source": "src", "object": "data"}[tag]
            if values.get(key):
                self.links.append(values[key])
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "script" and values.get("type") == "application/ld+json":
            self.in_json_ld = True
            self.json_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            self.json_ld.append("".join(self.json_parts).strip())

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data
        if self.in_json_ld:
            self.json_parts.append(data)


def fail(message: str) -> None:
    ERRORS.append(message)


def local_target(page_path: Path, target: str) -> Path | None:
    if not target or target.startswith(("#", "mailto:", "data:", "javascript:")):
        return None
    parsed = urlsplit(target)
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc != "valto.github.io" or not parsed.path.startswith("/crd/"):
            return None
        relative = parsed.path.removeprefix("/crd/") or "index.html"
        return DOCS / relative
    clean = target.split("#", 1)[0].split("?", 1)[0]
    if clean.startswith("/crd/"):
        return DOCS / (clean.removeprefix("/crd/") or "index.html")
    return (page_path.parent / clean).resolve() if clean else None


def validate_page(page: dict[str, str], titles: set[str], descriptions: set[str], canonicals: set[str]) -> None:
    path = DOCS / page["file"]
    if not path.exists():
        fail(f"{page['file']}: missing")
        return
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    descriptions_found = [m.get("content", "") for m in parser.meta if m.get("name") == "description"]
    canonicals_found = [l.get("href", "") for l in parser.link_tags if l.get("rel") == "canonical"]
    og_required = {"og:title", "og:description", "og:url", "og:image"}
    og_found = {m.get("property") for m in parser.meta if m.get("property", "").startswith("og:")}
    twitter_required = {"twitter:card", "twitter:title", "twitter:description", "twitter:image"}
    twitter_found = {m.get("name") for m in parser.meta if m.get("name", "").startswith("twitter:")}
    if parser.h1 != 1:
        fail(f"{page['file']}: expected one H1, found {parser.h1}")
    if parser.title.strip() != page["title"]:
        fail(f"{page['file']}: title mismatch")
    if parser.title in titles:
        fail(f"{page['file']}: duplicate title")
    titles.add(parser.title)
    if descriptions_found != [page["description"]]:
        fail(f"{page['file']}: description mismatch")
    if page["description"] in descriptions:
        fail(f"{page['file']}: duplicate description")
    descriptions.add(page["description"])
    if canonicals_found != [page["url"]]:
        fail(f"{page['file']}: canonical mismatch")
    if page["url"] in canonicals:
        fail(f"{page['file']}: duplicate canonical")
    canonicals.add(page["url"])
    if not og_required.issubset(og_found):
        fail(f"{page['file']}: incomplete Open Graph metadata")
    if not twitter_required.issubset(twitter_found):
        fail(f"{page['file']}: incomplete Twitter metadata")
    if len(parser.json_ld) != 1:
        fail(f"{page['file']}: expected one JSON-LD block")
    else:
        try:
            json.loads(parser.json_ld[0])
        except json.JSONDecodeError as error:
            fail(f"{page['file']}: invalid JSON-LD: {error}")
    duplicate_ids = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
    if duplicate_ids:
        fail(f"{page['file']}: duplicate IDs: {', '.join(duplicate_ids)}")
    for target in parser.links:
        resolved = local_target(path, target)
        if resolved and not resolved.exists():
            fail(f"{page['file']}: broken local target {target}")


def validate_generated_assets() -> None:
    required = [
        "llms.txt",
        "llms-full.txt",
        "index.md",
        "specification.md",
        "template.md",
        "agent-transformation.md",
        "working-with-crds.md",
        "mle.md",
        "glossary.md",
        "crd-vs-prd.md",
        "agent-prompt.md",
        "agent-prompt.txt",
        "schema/crd.schema.json",
        "skills/crd-author/SKILL.md",
        "assets/crd-social-card.png",
    ]
    for relative in required:
        if not (DOCS / relative).exists():
            fail(f"missing generated/public asset: {relative}")
    pairs = {
        "crd-specification.md": "specification.md",
        "crd-template.md": "template.md",
        "agent-transformation-instructions.md": "agent-transformation.md",
        "working-with-crds.md": "working-with-crds.md",
        "minimum-logical-element.md": "mle.md",
        "schema/crd.schema.json": "schema/crd.schema.json",
        "skills/crd-author/SKILL.md": "skills/crd-author/SKILL.md",
        "crd-vs-prd.md": "crd-vs-prd.md",
        "glossary.md": "glossary.md",
        "agent-prompt.md": "agent-prompt.md",
    }
    for source, published in pairs.items():
        if (ROOT / source).read_bytes() != (DOCS / published).read_bytes():
            fail(f"stale generated copy: {published}")
    prompt_source = (DOCS / "agent-prompt.txt").read_text(encoding="utf-8").strip()
    prompt_page = (DOCS / "agent-prompt.html").read_text(encoding="utf-8")
    prompt_match = re.search(r'<textarea id="crd-agent-prompt"[^>]*>(.*?)</textarea>', prompt_page, flags=re.S)
    if not prompt_match or html.unescape(prompt_match.group(1)).strip() != prompt_source:
        fail("agent-prompt.html: embedded prompt differs from agent-prompt.txt")
    try:
        json.loads((DOCS / "schema" / "crd.schema.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"published JSON Schema invalid: {error}")


def validate_glossary_parity() -> None:
    glossary_md = (ROOT / "glossary.md").read_text(encoding="utf-8")
    terms = re.findall(r"^## (.+)$", glossary_md, flags=re.M)
    glossary_html = (DOCS / "glossary.html").read_text(encoding="utf-8")
    for term in terms:
        if f"<h2>{html.escape(term)}</h2>" not in glossary_html:
            fail(f"docs/glossary.html: missing rendered term {term!r} present in glossary.md")


def validate_sitemap() -> None:
    expected = {page["url"] for page in PAGES}
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
    actual = set(re.findall(r"<loc>(.*?)</loc>", sitemap))
    if actual != expected:
        fail(f"sitemap mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")


def validate_404() -> None:
    text = (DOCS / "404.html").read_text(encoding="utf-8")
    if not re.search(r'<meta\s+name="robots"\s+content="noindex,follow"', text):
        fail("404.html: missing noindex,follow")


def main() -> int:
    titles: set[str] = set()
    descriptions: set[str] = set()
    canonicals: set[str] = set()
    for page in PAGES:
        validate_page(page, titles, descriptions, canonicals)
    validate_generated_assets()
    validate_glossary_parity()
    validate_sitemap()
    validate_404()
    if ERRORS:
        for error in ERRORS:
            print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print(f"validated {len(PAGES)} indexable pages and generated assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
