#!/usr/bin/env python3
"""Render the CPVSS Markdown design doc into a styled standalone HTML page.

This intentionally avoids third-party dependencies so `make html` works on a
fresh machine with only Python available. It supports the Markdown features used
by the design doc: headings, paragraphs, blockquotes, ordered and unordered
lists, pipe tables, fenced code blocks, links, bold text, and inline code.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


DEFAULT_SOURCE = Path("docs/cpvss-subnet-design.md")
DEFAULT_OUTPUT = Path("index.html")
DEFAULT_RELEASE_METADATA = Path("release.json")


def load_release_metadata(path: Path = DEFAULT_RELEASE_METADATA) -> dict[str, str] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(key): str(value) for key, value in data.items()}


def slugify(text: str, seen: dict[str, int]) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = slug or "section"
    count = seen.get(slug, 0)
    seen[slug] = count + 1
    if count:
        return f"{slug}-{count + 1}"
    return slug


def inline(text: str) -> str:
    parts = re.split(r"(`[^`]*`)", text)
    rendered: list[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            rendered.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue

        escaped = html.escape(part)
        escaped = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda m: (
                f'<a href="{html.escape(m.group(2), quote=True)}">'
                f"{m.group(1)}</a>"
            ),
            escaped,
        )
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
        rendered.append(escaped)
    return "".join(rendered)


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    first = lines[index].strip()
    second = lines[index + 1].strip()
    if "|" not in first or "|" not in second:
        return False
    cells = [cell.strip() for cell in second.strip("|").split("|")]
    return all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def is_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    stripped = line.strip()
    if not stripped:
        return True
    if re.match(r"#{2,6}\s+", stripped):
        return True
    if stripped.startswith(">"):
        return True
    if re.match(r"[-*]\s+", stripped):
        return True
    if re.match(r"\d+\.\s+", stripped):
        return True
    if stripped.startswith("```"):
        return True
    if is_table_start(lines, index):
        return True
    return False


def split_table_row(row: str) -> list[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def render_table(lines: list[str], index: int) -> tuple[str, int]:
    headers = split_table_row(lines[index])
    index += 2
    rows: list[list[str]] = []
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped or "|" not in stripped:
            break
        rows.append(split_table_row(stripped))
        index += 1

    head_html = "".join(f"<th>{inline(cell)}</th>" for cell in headers)
    body_rows = []
    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        cells = "".join(f"<td>{inline(cell)}</td>" for cell in padded[: len(headers)])
        body_rows.append(f"<tr>{cells}</tr>")

    table = (
        '<div class="table-wrap"><table><thead><tr>'
        f"{head_html}"
        "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table></div>"
    )
    return table, index


def render_markdown_body(lines: list[str], heading_slugs: dict[int, str]) -> str:
    output: list[str] = []
    i = 0
    in_section = False

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue

        heading_match = re.match(r"(#{2,6})\s+(.+)", stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            if level == 2:
                if in_section:
                    output.append("</div></section>")
                section_id = heading_slugs.get(i, "section")
                output.append(f'<section id="{section_id}"><div class="content">')
                output.append(f"<h2>{inline(text)}</h2>")
                in_section = True
            else:
                output.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue

        if not in_section:
            output.append('<section id="intro"><div class="content">')
            in_section = True

        if is_table_start(lines, i):
            table_html, i = render_table(lines, i)
            output.append(table_html)
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            language_class = ""
            if language:
                language_class = f' class="language-{html.escape(language, quote=True)}"'
            code = html.escape("\n".join(code_lines))
            output.append(f"<pre><code{language_class}>{code}</code></pre>")
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip().lstrip(">").strip())
                i += 1
            output.append(f"<blockquote>{inline(' '.join(quote_lines))}</blockquote>")
            continue

        unordered = re.match(r"[-*]\s+(.+)", stripped)
        if unordered:
            items = []
            while i < len(lines):
                match = re.match(r"[-*]\s+(.+)", lines[i].strip())
                if not match:
                    break
                items.append(f"<li>{inline(match.group(1))}</li>")
                i += 1
            output.append("<ul>" + "".join(items) + "</ul>")
            continue

        ordered = re.match(r"\d+\.\s+(.+)", stripped)
        if ordered:
            items = []
            while i < len(lines):
                match = re.match(r"\d+\.\s+(.+)", lines[i].strip())
                if not match:
                    break
                items.append(f"<li>{inline(match.group(1))}</li>")
                i += 1
            output.append("<ol>" + "".join(items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines) and not is_block_start(lines, i):
            paragraph_lines.append(lines[i].strip())
            i += 1
        output.append(f"<p>{inline(' '.join(paragraph_lines))}</p>")

    if in_section:
        output.append("</div></section>")

    return "\n".join(output)


def parse_document(markdown: str) -> dict[str, object]:
    lines = markdown.splitlines()
    title = "Poseidon Subnet CPVSS Design and Launch Roadmap"
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()

    first_h2 = next((i for i, line in enumerate(lines) if line.startswith("## ")), len(lines))
    meta_lines = lines[1:first_h2]
    metadata: list[tuple[str, str]] = []
    for line in meta_lines:
        clean = line.strip()
        if not clean or ":" not in clean:
            continue
        key, value = clean.split(":", 1)
        metadata.append((key.strip(), value.strip()))

    body_lines = lines[first_h2:]
    seen: dict[str, int] = {}
    nav: list[tuple[str, str]] = []
    heading_slugs: dict[int, str] = {}
    for index, line in enumerate(body_lines):
        if line.startswith("## "):
            text = line[3:].strip()
            slug = slugify(text, seen)
            heading_slugs[index] = slug
            nav.append((text, slug))

    body = render_markdown_body(body_lines, heading_slugs)
    return {"title": title, "metadata": metadata, "nav": nav, "body": body}


def release_banner(release_info: dict[str, str] | None) -> str:
    if not release_info:
        return ""

    release = html.escape(release_info.get("release", "unreleased"))
    commit = html.escape(release_info.get("commit", "unknown"))
    release_date = html.escape(release_info.get("release_date", "unknown"))
    release_page = html.escape(release_info.get("release_page", ""), quote=True)
    page_link = ""
    if release_page:
        page_link = (
            '<span>Snapshot: '
            f'<a href="{release_page}">{release_page}</a>'
            "</span>"
        )

    return (
        '<div class="release-banner">'
        f"<span>Major release: <strong>{release}</strong></span>"
        f"<span>Source commit: <code>{commit}</code></span>"
        f"<span>Release date: {release_date}</span>"
        f"{page_link}"
        "</div>"
    )


def render_page(
    document: dict[str, object],
    source_path: Path,
    release_info: dict[str, str] | None = None,
) -> str:
    title = str(document["title"])
    metadata = document["metadata"]
    nav = document["nav"]
    body = str(document["body"])
    meta_html = "".join(
        f'<span class="pill">{html.escape(key)}: {html.escape(value)}</span>'
        for key, value in metadata  # type: ignore[misc]
    )
    nav_html = "".join(
        f'<a href="#{slug}">{html.escape(text)}</a>' for text, slug in nav  # type: ignore[misc]
    )
    source_href = html.escape(source_path.as_posix(), quote=True)
    release_html = release_banner(release_info)

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <style>
      :root {{
        --ink: #1f2523;
        --muted: #5f6864;
        --line: #d8ded9;
        --paper: #fbfaf6;
        --surface: #ffffff;
        --teal: #1d7c72;
        --teal-soft: #e3f2ee;
        --amber: #b97014;
        --amber-soft: #fbedd9;
        --coral: #bd4b37;
        --green: #446b2f;
        --blue: #426d91;
        --sidebar: #f4f1e9;
        --hero-bg: linear-gradient(90deg, rgba(29, 124, 114, 0.12), rgba(185, 112, 20, 0.08)), var(--surface);
        --th-bg: #eef4ef;
        --quote-bg: var(--ink);
        --quote-text: #f8f4e9;
        --control-bg: rgba(255, 255, 255, 0.86);
        --pill-bg: rgba(255, 255, 255, 0.72);
        --section-alt: rgba(255, 255, 255, 0.56);
        --shadow: 0 18px 45px rgba(37, 42, 38, 0.08);
      }}

      body[data-theme="protocol"] {{
        --ink: #eef4ef;
        --muted: #b9c5bf;
        --line: #34423d;
        --paper: #101816;
        --surface: #17211f;
        --teal: #62d4c1;
        --teal-soft: #183b35;
        --amber: #f0b65d;
        --amber-soft: #342819;
        --coral: #ff8f77;
        --green: #9bcf7c;
        --blue: #88b8e6;
        --sidebar: #0c1210;
        --hero-bg: linear-gradient(90deg, rgba(98, 212, 193, 0.14), rgba(240, 182, 93, 0.1)), var(--surface);
        --th-bg: #1d302c;
        --quote-bg: #0c1210;
        --quote-text: #effaf7;
        --control-bg: rgba(12, 18, 16, 0.88);
        --pill-bg: rgba(12, 18, 16, 0.45);
        --section-alt: rgba(255, 255, 255, 0.03);
        --shadow: 0 18px 45px rgba(0, 0, 0, 0.24);
      }}

      body[data-theme="market"] {{
        --ink: #20242a;
        --muted: #626a76;
        --line: #d7dce4;
        --paper: #f7f8fb;
        --surface: #ffffff;
        --teal: #006d83;
        --teal-soft: #e1f4f7;
        --amber: #996100;
        --amber-soft: #fff1d5;
        --coral: #c44b5d;
        --green: #386d4a;
        --blue: #3b64b4;
        --sidebar: #edf2f8;
        --hero-bg: linear-gradient(90deg, rgba(0, 109, 131, 0.1), rgba(196, 75, 93, 0.08)), var(--surface);
        --th-bg: #e8eef7;
        --quote-bg: #20242a;
        --quote-text: #f8fbff;
        --control-bg: rgba(255, 255, 255, 0.9);
        --pill-bg: rgba(255, 255, 255, 0.76);
        --section-alt: rgba(255, 255, 255, 0.66);
        --shadow: 0 18px 45px rgba(47, 62, 82, 0.11);
      }}

      * {{ box-sizing: border-box; }}
      html {{ scroll-behavior: smooth; }}
      body {{
        margin: 0;
        color: var(--ink);
        background: var(--paper);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        line-height: 1.6;
      }}
      a {{
        color: var(--teal);
        text-decoration-thickness: 1px;
        text-underline-offset: 3px;
      }}
      .page-shell {{
        display: grid;
        grid-template-columns: 280px minmax(0, 1fr);
        min-height: 100vh;
      }}
      .top-actions {{
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 10;
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: flex-end;
        max-width: min(560px, calc(100vw - 32px));
        padding: 8px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--control-bg);
        box-shadow: var(--shadow);
        backdrop-filter: blur(12px);
      }}
      .style-switcher {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
      }}
      button {{
        min-height: 34px;
        border: 1px solid var(--line);
        border-radius: 7px;
        background: var(--surface);
        color: var(--ink);
        font: inherit;
        font-size: 13px;
        font-weight: 750;
        cursor: pointer;
      }}
      .theme-button {{ padding: 5px 10px; }}
      .theme-button[aria-pressed="true"], .pdf-button, .doc-button {{
        border-color: var(--teal);
        background: var(--teal);
        color: #ffffff;
      }}
      .pdf-button, .doc-button {{ padding: 5px 12px; }}
      aside {{
        position: sticky;
        top: 0;
        height: 100vh;
        padding: 32px 24px;
        border-right: 1px solid var(--line);
        background: var(--sidebar);
        overflow: auto;
      }}
      .brand {{ margin-bottom: 28px; }}
      .brand .eyebrow {{
        color: var(--amber);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
      }}
      .brand h1 {{
        margin: 8px 0 12px;
        font-size: 24px;
        line-height: 1.12;
      }}
      .brand p {{
        margin: 0;
        color: var(--muted);
        font-size: 14px;
      }}
      nav {{
        display: grid;
        gap: 6px;
      }}
      nav a {{
        display: block;
        padding: 8px 10px;
        color: var(--ink);
        border-radius: 6px;
        text-decoration: none;
        font-size: 14px;
      }}
      nav a:hover {{
        background: var(--teal-soft);
        color: var(--teal);
      }}
      main {{ min-width: 0; }}
      .hero {{
        padding: 58px clamp(24px, 5vw, 76px) 30px;
        background: var(--hero-bg);
        border-bottom: 1px solid var(--line);
      }}
      .hero-inner {{ max-width: 1100px; }}
      .meta-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 20px;
        padding-right: 300px;
      }}
      .pill {{
        display: inline-flex;
        align-items: center;
        min-height: 30px;
        padding: 4px 10px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--pill-bg);
        color: var(--muted);
        font-size: 13px;
        font-weight: 650;
      }}
      .hero h2 {{
        max-width: 900px;
        margin: 0;
        font-size: clamp(34px, 5vw, 64px);
        line-height: 1.02;
        letter-spacing: 0;
      }}
      .hero p {{
        max-width: 780px;
        margin: 22px 0 0;
        color: var(--muted);
        font-size: 19px;
      }}
      .release-banner {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        max-width: 980px;
        margin-top: 22px;
      }}
      .release-banner span {{
        display: inline-flex;
        align-items: center;
        min-height: 32px;
        padding: 5px 10px;
        border: 1px solid var(--line);
        border-radius: 7px;
        background: var(--surface);
        color: var(--ink);
        font-size: 13px;
        font-weight: 700;
      }}
      section {{
        padding: 48px clamp(24px, 5vw, 76px);
        border-bottom: 1px solid var(--line);
      }}
      section:nth-of-type(even) {{ background: var(--section-alt); }}
      .content {{ max-width: 1120px; }}
      h2, h3, h4, h5, h6 {{
        line-height: 1.18;
        letter-spacing: 0;
      }}
      h2 {{
        margin: 0 0 18px;
        font-size: clamp(28px, 3vw, 42px);
      }}
      h3 {{
        margin: 34px 0 12px;
        font-size: 24px;
      }}
      h4 {{
        margin: 24px 0 8px;
        font-size: 18px;
        color: var(--teal);
      }}
      p {{ max-width: 880px; }}
      blockquote {{
        max-width: 1000px;
        margin: 24px 0;
        padding: 24px 28px;
        border-left: 5px solid var(--teal);
        border-radius: 8px;
        background: var(--quote-bg);
        color: var(--quote-text);
        font-size: clamp(19px, 2vw, 28px);
        line-height: 1.35;
        font-weight: 720;
      }}
      .table-wrap {{
        width: 100%;
        margin: 24px 0;
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
      }}
      table {{
        width: 100%;
        min-width: 820px;
        border-collapse: collapse;
      }}
      th, td {{
        padding: 14px 16px;
        border-bottom: 1px solid var(--line);
        text-align: left;
        vertical-align: top;
      }}
      th {{
        background: var(--th-bg);
        color: var(--ink);
        font-size: 13px;
        text-transform: uppercase;
      }}
      tr:last-child td {{ border-bottom: 0; }}
      ul, ol {{
        max-width: 880px;
        padding-left: 24px;
      }}
      li + li {{ margin-top: 7px; }}
      code {{
        padding: 2px 5px;
        border: 1px solid var(--line);
        border-radius: 5px;
        background: var(--surface);
        font-size: 0.92em;
      }}
      pre {{
        max-width: 880px;
        margin: 18px 0;
        padding: 16px 18px;
        overflow-x: auto;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: var(--surface);
      }}
      pre code {{
        padding: 0;
        border: 0;
        background: transparent;
        font-size: 13px;
        line-height: 1.55;
      }}
      .footer {{
        padding: 36px clamp(24px, 5vw, 76px);
        background: var(--quote-bg);
        color: var(--quote-text);
      }}
      .footer p {{
        margin: 0;
        color: var(--quote-text);
      }}
      @media (max-width: 980px) {{
        .page-shell {{ display: block; }}
        aside {{
          position: static;
          height: auto;
          padding: 24px;
          border-right: 0;
          border-bottom: 1px solid var(--line);
        }}
        nav {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .meta-row {{ padding-right: 0; }}
      }}
      @media (max-width: 560px) {{
        nav {{ grid-template-columns: 1fr; }}
        .hero, section, .footer {{
          padding-left: 18px;
          padding-right: 18px;
        }}
        .hero h2 {{ font-size: 36px; }}
        .hero p {{ font-size: 16px; }}
        th, td {{ padding: 12px; }}
      }}
      @media print {{
        @page {{ margin: 0.55in; }}
        body {{
          background: #ffffff;
          color: #1f2523;
        }}
        .top-actions, aside {{ display: none; }}
        .page-shell {{ display: block; }}
        .hero, section, .footer {{ padding: 24px 0; }}
        blockquote {{ font-size: 18px; }}
        pre {{
          white-space: pre-wrap;
          break-inside: avoid;
        }}
        .table-wrap {{
          overflow: visible;
          break-inside: avoid;
        }}
        table {{
          min-width: 0;
          font-size: 10px;
        }}
        th, td {{ padding: 7px 8px; }}
        h2, h3, h4 {{ break-after: avoid; }}
        tr {{ break-inside: avoid; }}
      }}
    </style>
  </head>
  <body data-theme="executive">
    <div class="top-actions" aria-label="Document actions">
      <div class="style-switcher" role="group" aria-label="Style">
        <button class="theme-button" type="button" data-theme-option="executive" aria-pressed="true">Executive</button>
        <button class="theme-button" type="button" data-theme-option="protocol" aria-pressed="false">Protocol</button>
        <button class="theme-button" type="button" data-theme-option="market" aria-pressed="false">Market</button>
      </div>
      <button class="pdf-button" type="button" id="export-pdf">Export PDF</button>
      <button class="doc-button" type="button" id="export-doc">Export DOCX</button>
    </div>
    <div class="page-shell">
      <aside>
        <div class="brand">
          <div class="eyebrow">Poseidon Subnet</div>
          <h1>{html.escape(title)}</h1>
          <p>Source Markdown: <a href="{source_href}">{source_href}</a></p>
        </div>
        <nav aria-label="Document sections">
          {nav_html}
        </nav>
      </aside>
      <main>
        <header class="hero" id="summary">
          <div class="hero-inner">
            <div class="meta-row">{meta_html}</div>
            <h2>{html.escape(title)}</h2>
            <p>Generated from the Markdown source. Edit the Markdown and run <code>make html</code> to rebuild this page.</p>
            {release_html}
          </div>
        </header>
        {body}
        <footer class="footer">
          <p>Generated from {source_href}. Use the Export PDF or Export DOCX buttons to share this document.</p>
        </footer>
      </main>
    </div>
    <script>
      (() => {{
        const storageKey = "cpvss-theme";
        const buttons = Array.from(document.querySelectorAll("[data-theme-option]"));
        const exportButton = document.getElementById("export-pdf");
        const exportDocButton = document.getElementById("export-doc");
        const getSavedTheme = () => {{
          try {{
            return localStorage.getItem(storageKey);
          }} catch {{
            return null;
          }}
        }};
        const saveTheme = (theme) => {{
          try {{
            localStorage.setItem(storageKey, theme);
          }} catch {{
            /* Theme persistence is optional for local files. */
          }}
        }};
        const setTheme = (theme) => {{
          const allowed = buttons.map((button) => button.dataset.themeOption);
          const nextTheme = allowed.includes(theme) ? theme : "executive";
          document.body.dataset.theme = nextTheme;
          buttons.forEach((button) => {{
            button.setAttribute("aria-pressed", String(button.dataset.themeOption === nextTheme));
          }});
          saveTheme(nextTheme);
        }};
        buttons.forEach((button) => {{
          button.addEventListener("click", () => setTheme(button.dataset.themeOption));
        }});
        exportButton.addEventListener("click", () => window.print());
        const filenameSlug = (value) => {{
          return value
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, "-")
            .replace(/^-+|-+$/g, "") || "poseidon-subnet-design";
        }};
        const xmlEscape = (value) => {{
          return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
        }};
        const normalizeText = (value) => {{
          return String(value || "").replace(/\\s+/g, " ").trim();
        }};
        const paragraph = (text, style) => {{
          const clean = String(text || "");
          if (!clean.trim()) {{
            return "";
          }}
          const styleXml = style ? `<w:pPr><w:pStyle w:val="${{style}}"/></w:pPr>` : "";
          const runs = clean
            .split("\\n")
            .map((part, index) => `${{index ? "<w:br/>" : ""}}<w:t xml:space="preserve">${{xmlEscape(part)}}</w:t>`)
            .join("");
          return `<w:p>${{styleXml}}<w:r>${{runs}}</w:r></w:p>`;
        }};
        const tableXml = (table) => {{
          const rows = Array.from(table.rows).map((row) => {{
            const cells = Array.from(row.cells).map((cell) => {{
              const text = normalizeText(cell.innerText);
              return `<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>${{paragraph(text, cell.tagName === "TH" ? "TableHeader" : "")}}</w:tc>`;
            }}).join("");
            return `<w:tr>${{cells}}</w:tr>`;
          }}).join("");
          return `<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="cfd7d2"/><w:left w:val="single" w:sz="4" w:space="0" w:color="cfd7d2"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="cfd7d2"/><w:right w:val="single" w:sz="4" w:space="0" w:color="cfd7d2"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="cfd7d2"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="cfd7d2"/></w:tblBorders></w:tblPr>${{rows}}</w:tbl>`;
        }};
        const blockXml = (element) => {{
          const tag = element.tagName;
          if (tag === "SCRIPT" || tag === "STYLE") {{
            return "";
          }}
          if (tag === "TABLE") {{
            return tableXml(element);
          }}
          if (tag === "H1") {{
            return paragraph(normalizeText(element.innerText), "Title");
          }}
          if (tag === "H2") {{
            return paragraph(normalizeText(element.innerText), "Heading1");
          }}
          if (tag === "H3") {{
            return paragraph(normalizeText(element.innerText), "Heading2");
          }}
          if (tag === "H4") {{
            return paragraph(normalizeText(element.innerText), "Heading3");
          }}
          if (tag === "P") {{
            return paragraph(normalizeText(element.innerText), "");
          }}
          if (tag === "BLOCKQUOTE") {{
            return paragraph(normalizeText(element.innerText), "Quote");
          }}
          if (tag === "PRE") {{
            return paragraph(element.innerText, "Code");
          }}
          if (tag === "UL" || tag === "OL") {{
            return Array.from(element.children).map((item, index) => {{
              const prefix = tag === "OL" ? `${{index + 1}}. ` : "- ";
              return paragraph(prefix + normalizeText(item.innerText), "");
            }}).join("");
          }}
          return Array.from(element.children).map(blockXml).join("");
        }};
        const documentXml = (main) => {{
          const body = Array.from(main.children).map(blockXml).join("");
          return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
              <w:body>
                ${{body}}
                <w:sectPr>
                  <w:pgSz w:w="12240" w:h="15840"/>
                  <w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" w:header="360" w:footer="360" w:gutter="0"/>
                </w:sectPr>
              </w:body>
            </w:document>`;
        }};
        const docxStyles = () => `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
          <w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:sz w:val="40"/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="Heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="Heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="Heading 3"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="Quote"><w:name w:val="Quote"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="360"/></w:pPr><w:rPr><w:i/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="20"/></w:rPr></w:style>
            <w:style w:type="paragraph" w:styleId="TableHeader"><w:name w:val="Table Header"/><w:basedOn w:val="Normal"/><w:rPr><w:b/></w:rPr></w:style>
          </w:styles>`;
        const crcTable = (() => {{
          const table = [];
          for (let n = 0; n < 256; n += 1) {{
            let c = n;
            for (let k = 0; k < 8; k += 1) {{
              c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
            }}
            table[n] = c >>> 0;
          }}
          return table;
        }})();
        const crc32 = (bytes) => {{
          let crc = 0xffffffff;
          for (const byte of bytes) {{
            crc = crcTable[(crc ^ byte) & 0xff] ^ (crc >>> 8);
          }}
          return (crc ^ 0xffffffff) >>> 0;
        }};
        const dosDateTime = (date) => {{
          const time = (date.getHours() << 11) | (date.getMinutes() << 5) | Math.floor(date.getSeconds() / 2);
          const day = ((date.getFullYear() - 1980) << 9) | ((date.getMonth() + 1) << 5) | date.getDate();
          return {{ time, day }};
        }};
        const u16 = (value) => [value & 0xff, (value >>> 8) & 0xff];
        const u32 = (value) => [value & 0xff, (value >>> 8) & 0xff, (value >>> 16) & 0xff, (value >>> 24) & 0xff];
        const concatParts = (parts) => {{
          const total = parts.reduce((sum, part) => sum + part.length, 0);
          const output = new Uint8Array(total);
          let offset = 0;
          for (const part of parts) {{
            output.set(part, offset);
            offset += part.length;
          }}
          return output;
        }};
        const zipPackage = (files) => {{
          const encoder = new TextEncoder();
          const localParts = [];
          const centralParts = [];
          const now = dosDateTime(new Date());
          let offset = 0;
          for (const file of files) {{
            const nameBytes = encoder.encode(file.name);
            const data = encoder.encode(file.content);
            const crc = crc32(data);
            const localHeader = new Uint8Array([
              ...u32(0x04034b50), ...u16(20), ...u16(0x0800), ...u16(0),
              ...u16(now.time), ...u16(now.day), ...u32(crc),
              ...u32(data.length), ...u32(data.length), ...u16(nameBytes.length), ...u16(0),
            ]);
            localParts.push(localHeader, nameBytes, data);
            const centralHeader = new Uint8Array([
              ...u32(0x02014b50), ...u16(20), ...u16(20), ...u16(0x0800), ...u16(0),
              ...u16(now.time), ...u16(now.day), ...u32(crc),
              ...u32(data.length), ...u32(data.length), ...u16(nameBytes.length), ...u16(0),
              ...u16(0), ...u16(0), ...u16(0), ...u32(0), ...u32(offset),
            ]);
            centralParts.push(centralHeader, nameBytes);
            offset += localHeader.length + nameBytes.length + data.length;
          }}
          const localBytes = concatParts(localParts);
          const centralBytes = concatParts(centralParts);
          const end = new Uint8Array([
            ...u32(0x06054b50), ...u16(0), ...u16(0), ...u16(files.length), ...u16(files.length),
            ...u32(centralBytes.length), ...u32(localBytes.length), ...u16(0),
          ]);
          return concatParts([localBytes, centralBytes, end]);
        }};
        const exportDoc = () => {{
          const main = document.querySelector("main");
          if (!main) {{
            return;
          }}
          const title = document.querySelector(".hero h2")?.textContent?.trim() || document.title;
          const release = document.querySelector(".release-banner strong")?.textContent?.trim();
          const filename = filenameSlug([title, release].filter(Boolean).join("-"));
          const created = new Date().toISOString();
          const files = [
            {{ name: "[Content_Types].xml", content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>` }},
            {{ name: "_rels/.rels", content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>` }},
            {{ name: "word/_rels/document.xml.rels", content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>` }},
            {{ name: "word/document.xml", content: documentXml(main) }},
            {{ name: "word/styles.xml", content: docxStyles() }},
            {{ name: "docProps/core.xml", content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${{xmlEscape(title)}}</dc:title><dc:creator>Poseidon Subnet Design</dc:creator><cp:lastModifiedBy>Poseidon Subnet Design</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">${{created}}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">${{created}}</dcterms:modified></cp:coreProperties>` }},
            {{ name: "docProps/app.xml", content: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Poseidon Subnet HTML Export</Application></Properties>` }},
          ];
          const blob = new Blob([zipPackage(files)], {{ type: "application/vnd.openxmlformats-officedocument.wordprocessingml.document" }});
          const url = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = url;
          link.download = `${{filename}}.docx`;
          document.body.appendChild(link);
          link.click();
          link.remove();
          window.setTimeout(() => URL.revokeObjectURL(url), 0);
        }};
        exportDocButton.addEventListener("click", exportDoc);
        setTheme(getSavedTheme() || "executive");
      }})();
    </script>
  </body>
</html>
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--release", help="Major release name, for example v1.0.0")
    parser.add_argument("--commit", help="Source commit hash for the release")
    parser.add_argument("--release-date", help="Release date in YYYY-MM-DD form")
    parser.add_argument("--release-page", help="Versioned HTML snapshot path")
    parser.add_argument(
        "--metadata-out",
        type=Path,
        help="Write release metadata for future `make html` runs",
    )
    return parser.parse_args(argv[1:])


def release_info_from_args(args: argparse.Namespace) -> dict[str, str] | None:
    if args.release:
        return {
            "release": args.release,
            "commit": args.commit or "unknown",
            "release_date": args.release_date or "unknown",
            "release_page": args.release_page or "",
        }
    return load_release_metadata()


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    source = args.source
    output = args.output

    markdown = source.read_text(encoding="utf-8")
    document = parse_document(markdown)
    release_info = release_info_from_args(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_page(document, source, release_info), encoding="utf-8")
    if args.metadata_out and release_info:
        args.metadata_out.write_text(
            json.dumps(release_info, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(f"Rendered {source} -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
