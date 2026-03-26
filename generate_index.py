#!/usr/bin/env python3
"""
KENOMA — index.html Generator
==============================
Scans all HTML files in the same directory, extracts metadata,
auto-categorizes them, and writes a fresh index.html.

Usage:
    python generate_index.py               # scan current directory
    python generate_index.py ./my-folder   # scan a specific folder
    python generate_index.py --watch       # auto-regenerate on file changes

Requirements: Python 3.7+ (stdlib only — no pip installs needed)

Categories (v2 — updated with all project phases):
    nav        Navigator & Index
    bible      Storytelling Bibles
    character  Characters & Narrative
    phase      Phase Design & Systems
    gdd        Game Design Documents
    puzzle     Level Design & Puzzles
    map        Maps & Architecture
    analysis   Research & Analysis
    synthesis  Synthesis, Gaps & Evaluation
    quantum    Quantum Physics Design
    present    Presentations & Pitches
"""

import os
import re
import sys
import json
import argparse
import time
import hashlib
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser


# ─────────────────────────────────────────────────
#  METADATA EXTRACTOR
# ─────────────────────────────────────────────────

class HTMLMetaExtractor(HTMLParser):
    """Parse an HTML file and extract title, description, and body text."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.body_texts = []
        self._in_title = False
        self._in_body = False
        self._in_script = False
        self._in_style = False
        self._in_head = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "head":
            self._in_head = True
        if tag == "body":
            self._in_body = True
        if tag == "script":
            self._in_script = True
        if tag == "style":
            self._in_style = True
        if tag == "meta":
            if attrs_dict.get("name", "").lower() == "description":
                self.description = attrs_dict.get("content", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "head":
            self._in_head = False
        if tag == "script":
            self._in_script = False
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title = text
        if self._in_script or self._in_style or self._in_head:
            return
        if self._in_body and len(text) > 20:
            self.body_texts.append(text)

    def get_summary(self, max_chars=150):
        if self.description:
            return self.description[:max_chars]
        combined = " · ".join(
            t for t in self.body_texts[:6]
            if len(t) > 30 and not t.startswith(("§", "·", "•", "─", "═"))
        )
        if combined:
            return combined[:max_chars] + ("…" if len(combined) > max_chars else "")
        return "No description available"


def extract_metadata(filepath: Path) -> dict:
    """Extract title, summary, and other metadata from an HTML file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        content = ""

    parser = HTMLMetaExtractor()
    try:
        parser.feed(content)
    except Exception:
        pass

    stat = filepath.stat()
    size_kb = round(stat.st_size / 1024, 1)
    modified = datetime.fromtimestamp(stat.st_mtime)

    title = parser.title or filepath.stem.replace("_", " ").replace("-", " ")

    return {
        "filename": filepath.name,
        "filepath": str(filepath),
        "title": title,
        "summary": parser.get_summary(),
        "size_kb": size_kb,
        "size_raw": stat.st_size,
        "modified": modified.strftime("%b %d, %Y"),
        "modified_iso": modified.strftime("%Y-%m-%d"),
        "modified_ts": int(stat.st_mtime),
    }


# ─────────────────────────────────────────────────
#  CATEGORY RULES  (order matters — first match wins)
# ─────────────────────────────────────────────────
#
#  Each entry: (pattern_list, cat_id, label, icon, css_class)
#  Patterns are checked against the lowercased filename.

CATEGORY_RULES = [

    # ── Navigation / Index ──────────────────────────────────────
    (["_navigator", "navigator_"],
     "nav", "Navigator & Index", "🧭", "tag-nav"),

    # ── Storytelling Bibles ──────────────────────────────────────
    (["storytelling_bible", "story_bible", "_bible"],
     "bible", "Storytelling Bibles", "📖", "tag-bible"),

    # ── Characters & Narrative ──────────────────────────────────
    (["complete_narrative", "vanguard_expansion",
      "_character", "character_", "_narrative"],
     "character", "Characters & Narrative", "🎭", "tag-character"),

    # ── Phase Design & Systems ───────────────────────────────────
    (["phase_design", "game_loop", "_systems", "systems_"],
     "phase", "Phase Design & Systems", "⚙️", "tag-phase"),

    # ── Game Design Documents ────────────────────────────────────
    (["gdd_v5", "gdd_v4", "gdd_v3", "gdd_v2", "gdd_enh",
      "gdd.html", "gdd_", "_gdd", "production_gdd"],
     "gdd", "Game Design Documents", "📋", "tag-gdd"),

    # ── Level Design & Puzzles ───────────────────────────────────
    (["interference_puzzle", "interference_puzzles",
      "calibration_channel", "level_design", "_puzzle", "puzzle_"],
     "puzzle", "Level Design & Puzzles", "🧩", "tag-puzzle"),

    # ── Maps & Architecture ──────────────────────────────────────
    (["_maps", "map_", "maps.html"],
     "map", "Maps & Architecture", "🗺️", "tag-map"),

    # ── Synthesis, Gaps & Evaluation ────────────────────────────
    (["final_synthesis", "gap_analysis", "_evaluation",
      "evaluation_", "_synthesis", "synthesis_"],
     "synthesis", "Synthesis & Evaluation", "🔎", "tag-synthesis"),

    # ── Quantum Physics Design ───────────────────────────────────
    (["_quantum", "quantum_"],
     "quantum", "Quantum Physics Design", "⚛️", "tag-quantum"),

    # ── Research & Analysis ──────────────────────────────────────
    (["deep_analysis", "comparative_analysis", "ts_analysis",
      "ts_deep", "uniqueness", "_analysis", "analysis_"],
     "analysis", "Research & Analysis", "🔬", "tag-analysis"),

    # ── Presentations & Pitches ──────────────────────────────────
    (["product_presentation", "team_presentation",
      "investor_presentation", "_presentation", "presentation_"],
     "present", "Presentations & Pitches", "📊", "tag-present"),
]

# Preferred display order for groups
CATEGORY_ORDER = [
    "nav", "bible", "character", "phase",
    "gdd", "puzzle", "map",
    "synthesis", "quantum", "analysis",
    "present", "other",
]

VERSION_PATTERN = re.compile(r"[_\-]v(\d+)", re.IGNORECASE)

KEY_DOCS = {
    # Story heart
    "kenoma_storytelling_bible_v8",
    "kenoma_complete_narrative",
    "kenoma_phase_design",
    # Character
    "kenoma_vanguard_expansion",
    "kenoma_vanguard_interference_puzzles",
    # Systems
    "kenoma_game_loop_systems",
    # World & puzzles
    "kenoma_calibration_channel",
    "kenoma_ts_deep_analysis",
    "kenoma_maps",
    # Synthesis
    "kenoma_final_synthesis",
    "kenoma_gap_analysis",
    "kenoma_evaluation",
    # Navigation
    "kenoma_navigator",
    # Quantum
    "kenoma_quantum",
}


def categorize(filename: str) -> tuple:
    """Return (cat_id, label, icon, css_class)."""
    lower = filename.lower()
    for patterns, cat_id, label, icon, color in CATEGORY_RULES:
        if any(p in lower for p in patterns):
            return cat_id, label, icon, color
    return "other", "Other Files", "📄", "tag-other"


def detect_version(filename: str) -> str:
    lower = filename.lower()
    m = VERSION_PATTERN.search(lower)
    if m:
        return f"v{m.group(1)}"
    if "enhanced" in lower:
        return "v2"
    if "revised" in lower:
        return "v2"
    return "—"


def is_key_doc(filename: str) -> bool:
    stem = Path(filename).stem.lower()
    return stem in KEY_DOCS


# ─────────────────────────────────────────────────
#  HTML BUILDER
# ─────────────────────────────────────────────────

def build_file_row(meta: dict) -> str:
    cat_id, cat_label, icon, color = categorize(meta["filename"])
    version = detect_version(meta["filename"])
    key = is_key_doc(meta["filename"])
    key_tag = '<span class="fr-tag tag-key">✦ Core</span>' if key else ""
    # Short category label for the tag pill (first word)
    short = cat_label.split()[0]
    tags_html = f'<span class="fr-tag {color}">{short}</span>{key_tag}'
    size_str = f"{meta['size_kb']} KB"

    return f"""      <a class="file-row" href="{meta['filename']}"
         data-tags="{cat_id}"
         data-version="{version}"
         data-size="{meta['size_raw']}"
         data-date="{meta['modified_iso']}"
         data-name="{meta['filename'].lower()}"
         target="_blank" rel="noopener">
        <div class="fr-name">
          <span class="fr-icon">{icon}</span>
          <div class="fr-text">
            <div class="fr-filename">{meta['filename']}</div>
            <div class="fr-summary">{meta['summary']}</div>
          </div>
        </div>
        <div class="fr-version">{version}</div>
        <div class="fr-date">{meta['modified']}</div>
        <div class="fr-size">{size_str}</div>
        <div class="fr-meta">{tags_html}</div>
      </a>"""


def build_groups(files: list) -> str:
    from collections import defaultdict
    groups = defaultdict(list)
    group_info = {}

    for meta in files:
        cat_id, cat_label, icon, _ = categorize(meta["filename"])
        groups[cat_id].append(meta)
        group_info[cat_id] = (cat_label, icon)

    html_parts = []
    for cat_id in CATEGORY_ORDER:
        if cat_id not in groups:
            continue
        label, icon = group_info[cat_id]
        rows = "\n".join(build_file_row(m) for m in groups[cat_id])
        html_parts.append(
            f'      <div class="group-hd" data-group="{cat_id}">'
            f'{icon} {label}</div>\n{rows}'
        )

    return "\n\n".join(html_parts)


def build_sidebar_items(files: list) -> str:
    from collections import Counter
    counts = Counter()
    for meta in files:
        cat_id, _, _, _ = categorize(meta["filename"])
        counts[cat_id] += 1

    # Sidebar entries: (cat_id, icon, display_label)
    cats = [
        ("all",       "📁",  "All Files",              len(files)),
        ("nav",       "🧭",  "Navigator",              counts.get("nav", 0)),
        ("bible",     "📖",  "Story Bible",            counts.get("bible", 0)),
        ("character", "🎭",  "Characters",             counts.get("character", 0)),
        ("phase",     "⚙️",  "Phase & Systems",        counts.get("phase", 0)),
        ("gdd",       "📋",  "GDD",                    counts.get("gdd", 0)),
        ("puzzle",    "🧩",  "Puzzles",                counts.get("puzzle", 0)),
        ("map",       "🗺️", "Maps",                   counts.get("map", 0)),
        ("synthesis", "🔎",  "Synthesis",              counts.get("synthesis", 0)),
        ("quantum",   "⚛️",  "Quantum",                counts.get("quantum", 0)),
        ("analysis",  "🔬",  "Research",               counts.get("analysis", 0)),
        ("present",   "📊",  "Presentations",          counts.get("present", 0)),
        ("other",     "📄",  "Other",                  counts.get("other", 0)),
    ]

    items = []
    for cat_id, icon, label, count in cats:
        if count == 0 and cat_id != "all":
            continue
        active = ' class="sb-item active"' if cat_id == "all" else ' class="sb-item"'
        items.append(
            f'        <div{active} onclick="filterTag(\'{cat_id}\',this)">'
            f'<span class="sb-icon">{icon}</span> {label}'
            f'<span class="sb-count">{count}</span></div>'
        )
    return "\n".join(items)


def format_total_size(files: list) -> str:
    total = sum(m["size_raw"] for m in files)
    if total > 1_000_000:
        return f"{total/1_000_000:.1f} MB"
    return f"{total/1024:.0f} KB"


# ─────────────────────────────────────────────────
#  MAIN GENERATOR
# ─────────────────────────────────────────────────

def generate_index(scan_dir: Path, output_path: Path):
    """Scan directory and write index.html."""

    html_files = sorted(
        [f for f in scan_dir.glob("*.html") if f.name.lower() != "index.html"],
        key=lambda f: f.name.lower()
    )

    if not html_files:
        print(f"⚠  No HTML files found in {scan_dir}")
        return

    print(f"📂 Scanning {scan_dir}")
    print(f"📄 Found {len(html_files)} HTML file(s)…")

    files_meta = []
    for f in html_files:
        meta = extract_metadata(f)
        files_meta.append(meta)
        cat_id, _, _, _ = categorize(f.name)
        key_mark = " ✦" if is_key_doc(f.name) else ""
        print(f"   ✓  {f.name}  ({meta['size_kb']} KB)  [{cat_id}]{key_mark}")

    # Default sort: newest first
    files_meta.sort(key=lambda m: m["modified_iso"], reverse=True)

    groups_html    = build_groups(files_meta)
    sidebar_html   = build_sidebar_items(files_meta)
    total_size     = format_total_size(files_meta)
    file_count     = len(files_meta)
    generated_at   = datetime.now().strftime("%b %d, %Y · %H:%M")

    manifest_json = json.dumps(
        [{"filename": m["filename"],
          "tags": categorize(m["filename"])[0],
          "name": m["filename"].lower(),
          "summary": m["summary"].lower()}
         for m in files_meta],
        indent=2
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KENOMA — Project Files</title>
<!-- Generated by generate_index.py on {generated_at} -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{height:100%;font-family:'Inter',system-ui,sans-serif;font-size:13px;}}
body{{background:#1a1a1a;display:flex;align-items:center;justify-content:center;padding:24px;min-height:100vh;}}

.window{{width:100%;max-width:1140px;background:#252526;border-radius:10px;
  box-shadow:0 32px 80px rgba(0,0,0,.7),0 0 0 1px rgba(255,255,255,.06);
  overflow:hidden;display:flex;flex-direction:column;max-height:calc(100vh - 48px);}}

/* Title bar */
.titlebar{{height:40px;background:#2d2d2e;display:flex;align-items:center;
  padding:0 14px;gap:8px;border-bottom:1px solid #1a1a1a;flex-shrink:0;user-select:none;}}
.tb-dots{{display:flex;gap:7px;align-items:center;}}
.dot{{width:12px;height:12px;border-radius:50%;cursor:default;}}
.dot-r{{background:#ff5f57;}}.dot-y{{background:#febc2e;}}.dot-g{{background:#28c840;}}
.tb-title{{flex:1;text-align:center;font-size:12.5px;font-weight:500;color:#7a7a7a;letter-spacing:.2px;}}
.tb-spacer{{width:54px;}}

/* Toolbar */
.toolbar{{height:44px;background:#2d2d2e;display:flex;align-items:center;
  padding:0 14px;gap:6px;border-bottom:1px solid #1a1a1a;flex-shrink:0;}}
.tb-btn{{height:26px;padding:0 10px;background:transparent;border:1px solid transparent;
  border-radius:5px;color:#7a7a7a;font-family:'Inter',sans-serif;font-size:12px;cursor:pointer;
  display:flex;align-items:center;gap:5px;transition:all .12s;white-space:nowrap;}}
.tb-btn:hover{{background:rgba(255,255,255,.07);color:#ccc;border-color:rgba(255,255,255,.1);}}
.tb-btn.active{{background:rgba(255,255,255,.1);color:#ddd;border-color:rgba(255,255,255,.12);}}
.tb-sep{{width:1px;height:22px;background:#3a3a3a;margin:0 2px;}}
.breadcrumb{{flex:1;height:26px;background:#1e1e1e;border:1px solid #3a3a3a;border-radius:5px;
  display:flex;align-items:center;padding:0 10px;gap:6px;overflow:hidden;}}
.bc-seg{{font-family:'JetBrains Mono',monospace;font-size:11px;color:#555;
  display:flex;align-items:center;gap:6px;white-space:nowrap;}}
.bc-seg.cur{{color:#c0b890;}}
.bc-arrow{{color:#363636;font-size:10px;}}
.search-wrap{{position:relative;display:flex;align-items:center;}}
.search-icon{{position:absolute;left:9px;color:#555;font-size:12px;pointer-events:none;z-index:1;}}
.search-box{{height:26px;padding:0 10px 0 28px;background:#1e1e1e;border:1px solid #3a3a3a;
  border-radius:5px;color:#ccc;font-family:'Inter',sans-serif;font-size:12px;
  outline:none;width:200px;transition:border-color .15s;}}
.search-box:focus{{border-color:#666;}}

/* Layout */
.layout{{display:flex;flex:1;overflow:hidden;}}

/* Sidebar */
.sidebar{{width:178px;flex-shrink:0;background:#252526;border-right:1px solid #1a1a1a;
  padding:10px 0;overflow-y:auto;}}
.sb-section-lbl{{font-size:10.5px;font-weight:600;color:#484848;letter-spacing:1px;
  text-transform:uppercase;padding:8px 14px 3px;display:block;}}
.sb-item{{display:flex;align-items:center;gap:8px;padding:5px 14px;color:#7a7a7a;
  font-size:12.5px;cursor:pointer;transition:background .1s,color .1s;}}
.sb-item:hover{{background:rgba(255,255,255,.05);color:#aaa;}}
.sb-item.active{{background:rgba(255,255,255,.08);color:#ddd;}}
.sb-icon{{font-size:14px;opacity:.7;flex-shrink:0;}}
.sb-count{{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:10px;color:#3e3e3e;}}
.sb-sep{{height:1px;background:#1e1e1e;margin:6px 10px;}}

/* Main */
.main{{flex:1;overflow-y:auto;display:flex;flex-direction:column;}}

/* Column header */
.col-hdr{{display:grid;grid-template-columns:2fr 80px 110px 80px 1fr;
  gap:0;padding:7px 16px;border-bottom:1px solid #1e1e1e;
  position:sticky;top:0;background:#252526;z-index:5;flex-shrink:0;}}
.ch-col{{font-size:11px;font-weight:600;color:#484848;letter-spacing:.5px;
  text-transform:uppercase;cursor:pointer;padding:2px 8px;border-radius:3px;
  display:flex;align-items:center;gap:4px;transition:color .1s;user-select:none;}}
.ch-col:hover{{color:#777;}}
.ch-col.sorted{{color:#b8a870;}}

/* Group header */
.group-hd{{padding:10px 16px 4px;font-size:10.5px;font-weight:600;color:#3e3e3e;
  letter-spacing:1px;text-transform:uppercase;border-top:1px solid #1c1c1c;
  display:flex;align-items:center;gap:8px;}}
.group-hd:first-child{{border-top:none;}}
.group-hd::after{{content:'';flex:1;height:1px;background:#222;}}

/* File row */
.file-row{{display:grid;grid-template-columns:2fr 80px 110px 80px 1fr;
  gap:0;padding:0 8px;align-items:center;cursor:pointer;border-radius:5px;
  margin:0 8px;min-height:42px;transition:background .1s;
  text-decoration:none;color:inherit;}}
.file-row:hover{{background:rgba(255,255,255,.058);}}
.file-row:active{{background:rgba(255,255,255,.09);}}
.file-row.hidden{{display:none !important;}}
.fr-name{{display:flex;align-items:center;gap:10px;padding:8px;overflow:hidden;}}
.fr-icon{{font-size:18px;flex-shrink:0;opacity:.82;}}
.fr-text{{overflow:hidden;}}
.fr-filename{{font-size:13px;font-weight:500;color:#d0d0d0;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis;margin-bottom:1px;}}
.fr-summary{{font-size:11px;color:#4e4e4e;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;line-height:1.3;}}
.file-row:hover .fr-summary{{color:#686868;}}
.fr-version,.fr-date,.fr-size{{padding:8px;}}
.fr-version{{font-family:'JetBrains Mono',monospace;font-size:11px;color:#404040;text-align:center;}}
.fr-date{{font-size:12px;color:#505050;white-space:nowrap;}}
.fr-size{{font-family:'JetBrains Mono',monospace;font-size:11px;color:#404040;text-align:right;}}
.fr-meta{{padding:8px;display:flex;align-items:center;gap:4px;flex-wrap:wrap;}}
.fr-tag{{display:inline-flex;align-items:center;font-size:9.5px;
  font-family:'JetBrains Mono',monospace;letter-spacing:.5px;
  text-transform:uppercase;padding:2px 6px;border-radius:3px;}}

/* ── Tag colors — one per category ── */
.tag-nav       {{background:rgba(100,180,220,.12);color:#50a8d8;}}
.tag-bible     {{background:rgba(200,140,24,.12); color:#a8780e;}}
.tag-character {{background:rgba(160,72,160,.12); color:#a048a0;}}
.tag-phase     {{background:rgba(80,160,80,.12);  color:#40a040;}}
.tag-gdd       {{background:rgba(80,140,80,.12);  color:#50a050;}}
.tag-puzzle    {{background:rgba(80,160,120,.12); color:#40a070;}}
.tag-map       {{background:rgba(176,72,72,.12);  color:#a04848;}}
.tag-synthesis {{background:rgba(220,140,40,.12); color:#c07820;}}
.tag-quantum   {{background:rgba(60,100,200,.12); color:#4070c0;}}
.tag-analysis  {{background:rgba(72,112,176,.12); color:#4870a8;}}
.tag-present   {{background:rgba(120,80,176,.12); color:#8050a8;}}
.tag-other     {{background:rgba(100,100,100,.12);color:#686868;}}
.tag-key       {{background:rgba(200,168,24,.2);  color:#c8a020;}}

/* Empty state */
.empty{{flex:1;display:flex;flex-direction:column;align-items:center;
  justify-content:center;color:#303030;gap:10px;padding:40px;}}
.empty-icon{{font-size:42px;opacity:.3;}}
.empty-msg{{font-size:14px;}}

/* Status bar */
.statusbar{{padding:6px 16px;border-top:1px solid #1a1a1a;display:flex;
  gap:16px;align-items:center;background:#2d2d2e;flex-shrink:0;}}
.sb-stat{{font-size:11.5px;color:#484848;display:flex;align-items:center;gap:5px;}}
.sb-stat span{{color:#666;}}
.sb-right{{margin-left:auto;font-size:10.5px;color:#303030;font-family:'JetBrains Mono',monospace;}}

::-webkit-scrollbar{{width:7px;height:7px;}}
::-webkit-scrollbar-track{{background:#1a1a1a;}}
::-webkit-scrollbar-thumb{{background:#333;border-radius:4px;}}
::-webkit-scrollbar-thumb:hover{{background:#444;}}
</style>
</head>
<body>

<div class="window">

  <div class="titlebar">
    <div class="tb-dots">
      <div class="dot dot-r" title="Close"></div>
      <div class="dot dot-y" title="Minimize"></div>
      <div class="dot dot-g" title="Maximize"></div>
    </div>
    <div class="tb-title">KENOMA — Project Files · {file_count} documents</div>
    <div class="tb-spacer"></div>
  </div>

  <div class="toolbar">
    <button class="tb-btn" onclick="history.back()" title="Back">‹</button>
    <button class="tb-btn" onclick="history.forward()" title="Forward">›</button>
    <div class="tb-sep"></div>
    <div class="breadcrumb">
      <div class="bc-seg">🏠 Home</div>
      <div class="bc-arrow">›</div>
      <div class="bc-seg">Projects</div>
      <div class="bc-arrow">›</div>
      <div class="bc-seg cur">KENOMA · بایگانی دو راستی</div>
    </div>
    <div class="tb-sep"></div>
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input class="search-box" type="text" id="searchInput"
             placeholder="Search files… (press /)" oninput="filterFiles(this.value)"
             autocomplete="off" spellcheck="false">
    </div>
    <div class="tb-sep"></div>
    <button class="tb-btn active" id="btn-list" onclick="setView('list')">☰ List</button>
    <button class="tb-btn" id="btn-grid" onclick="setView('grid')">⊞ Grid</button>
  </div>

  <div class="layout">

    <div class="sidebar">
      <span class="sb-section-lbl">Filter by type</span>
{sidebar_html}
      <div class="sb-sep"></div>
      <span class="sb-section-lbl">Sort</span>
      <div class="sb-item" onclick="sortFiles('name')"><span class="sb-icon">🔤</span> Name</div>
      <div class="sb-item" onclick="sortFiles('date')"><span class="sb-icon">📅</span> Date Modified</div>
      <div class="sb-item" onclick="sortFiles('size')"><span class="sb-icon">📦</span> File Size</div>
      <div class="sb-item" onclick="sortFiles('version')"><span class="sb-icon">🔢</span> Version</div>
    </div>

    <div class="main" id="mainArea">
      <div class="col-hdr" id="colHdr">
        <div class="ch-col sorted" data-key="name" onclick="sortFiles('name')">Name ↕</div>
        <div class="ch-col" data-key="version" onclick="sortFiles('version')">Version</div>
        <div class="ch-col" data-key="date" onclick="sortFiles('date')">Modified</div>
        <div class="ch-col" data-key="size" onclick="sortFiles('size')">Size</div>
        <div class="ch-col">Tags</div>
      </div>

{groups_html}

      <div class="empty" id="emptyState" style="display:none">
        <div class="empty-icon">🔍</div>
        <div class="empty-msg">No files match your search</div>
      </div>
    </div>

  </div>

  <div class="statusbar">
    <div class="sb-stat">📄 <span id="visCount">{file_count}</span>&nbsp;files</div>
    <div class="sb-stat">💾 <span>{total_size}</span></div>
    <div class="sb-stat">📅 <span>Generated {generated_at}</span></div>
    <div class="sb-right">generate_index.py · KENOMA project</div>
  </div>

</div>

<script>
// ── Manifest ──
const MANIFEST = {manifest_json};

// ── State ──
let currentTag = 'all';
let currentSearch = '';

const rows = () => [...document.querySelectorAll('.file-row')];
const groups = () => [...document.querySelectorAll('.group-hd')];

function updateVisible() {{
  const q = currentSearch.toLowerCase();
  let count = 0;
  rows().forEach(r => {{
    const tagMatch = currentTag === 'all' || r.dataset.tags === currentTag;
    const qMatch = !q ||
      r.dataset.name.includes(q) ||
      r.querySelector('.fr-summary').textContent.toLowerCase().includes(q);
    const show = tagMatch && qMatch;
    r.classList.toggle('hidden', !show);
    if (show) count++;
  }});
  groups().forEach(g => {{
    let el = g.nextElementSibling;
    let has = false;
    while (el && !el.classList.contains('group-hd')) {{
      if (el.classList.contains('file-row') && !el.classList.contains('hidden')) has = true;
      el = el.nextElementSibling;
    }}
    g.style.display = has ? '' : 'none';
  }});
  document.getElementById('visCount').textContent = count;
  document.getElementById('emptyState').style.display = count === 0 ? 'flex' : 'none';
}}

function filterTag(tag, el) {{
  document.querySelectorAll('.sb-item').forEach(i => i.classList.remove('active'));
  el.classList.add('active');
  currentTag = tag;
  updateVisible();
}}

function filterFiles(q) {{
  currentSearch = q;
  updateVisible();
}}

let sortDirs = {{}};
function sortFiles(key) {{
  sortDirs[key] = !sortDirs[key];
  const asc = sortDirs[key];
  document.querySelectorAll('.ch-col').forEach(c => c.classList.remove('sorted'));
  const hdr = document.querySelector(`[data-key="${{key}}"]`);
  if (hdr) hdr.classList.add('sorted');
  const grps = groups();
  grps.forEach(g => {{
    const rowEls = [];
    let el = g.nextElementSibling;
    while (el && !el.classList.contains('group-hd')) {{
      if (el.classList.contains('file-row')) rowEls.push(el);
      el = el.nextElementSibling;
    }}
    rowEls.sort((a, b) => {{
      let va, vb;
      if (key === 'name')    {{ va = a.dataset.name;    vb = b.dataset.name; }}
      if (key === 'size')    {{ va = +a.dataset.size;   vb = +b.dataset.size; }}
      if (key === 'date')    {{ va = a.dataset.date;    vb = b.dataset.date; }}
      if (key === 'version') {{ va = parseInt(a.dataset.version)||0; vb = parseInt(b.dataset.version)||0; }}
      return asc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
    }});
    let ins = g;
    rowEls.forEach(r => {{ ins.insertAdjacentElement('afterend', r); ins = r; }});
  }});
}}

let currentView = 'list';
function setView(v) {{
  currentView = v;
  document.getElementById('btn-list').classList.toggle('active', v === 'list');
  document.getElementById('btn-grid').classList.toggle('active', v === 'grid');
  const ma = document.getElementById('mainArea');
  const hdr = document.getElementById('colHdr');
  if (v === 'grid') {{
    hdr.style.display = 'none';
    ma.style.cssText = 'flex:1;overflow-y:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:2px;padding:10px;align-content:start;';
    groups().forEach(g => g.style.gridColumn = '1/-1');
    rows().forEach(r => {{
      r.style.cssText = 'display:flex;flex-direction:column;padding:12px 14px;min-height:86px;border-radius:6px;';
      r.querySelectorAll('.fr-version,.fr-date,.fr-size').forEach(e => e.style.display='none');
    }});
  }} else {{
    hdr.style.display = '';
    ma.style.cssText = 'flex:1;overflow-y:auto;display:flex;flex-direction:column;';
    groups().forEach(g => g.style.gridColumn = '');
    rows().forEach(r => {{
      r.style.cssText = '';
      r.querySelectorAll('.fr-version,.fr-date,.fr-size').forEach(e => e.style.display='');
    }});
  }}
}}

// Keyboard shortcuts
document.addEventListener('keydown', e => {{
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
    e.preventDefault();
    document.getElementById('searchInput').focus();
  }}
  if (e.key === 'Escape') {{
    document.getElementById('searchInput').value = '';
    filterFiles('');
    document.getElementById('searchInput').blur();
  }}
}});
</script>
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")
    print(f"\n✅  Written → {output_path}")
    print(f"   {file_count} files · {total_size} total")


# ─────────────────────────────────────────────────
#  WATCH MODE
# ─────────────────────────────────────────────────

def get_dir_hash(scan_dir: Path) -> str:
    files = sorted(scan_dir.glob("*.html"))
    parts = []
    for f in files:
        if f.name.lower() == "index.html":
            continue
        stat = f.stat()
        parts.append(f"{f.name}:{stat.st_size}:{stat.st_mtime:.0f}")
    return hashlib.md5("\n".join(parts).encode()).hexdigest()


def watch_mode(scan_dir: Path, output_path: Path):
    print(f"👁  Watch mode — monitoring {scan_dir}")
    print(f"    Press Ctrl+C to stop\n")
    last_hash = None
    while True:
        try:
            current_hash = get_dir_hash(scan_dir)
            if current_hash != last_hash:
                print(f"🔄  Change detected · {datetime.now().strftime('%H:%M:%S')}")
                generate_index(scan_dir, output_path)
                last_hash = current_hash
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n⛔  Watch mode stopped.")
            break


# ─────────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Scan HTML files and generate index.html",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_index.py                   Scan current directory
  python generate_index.py ./docs            Scan ./docs folder
  python generate_index.py --watch           Auto-regenerate on changes
  python generate_index.py ./docs --watch    Watch a specific folder
  python generate_index.py -o custom.html    Custom output path
        """
    )
    parser.add_argument(
        "directory", nargs="?", default=".",
        help="Directory to scan (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output path for index.html (default: <directory>/index.html)"
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Watch for file changes and auto-regenerate"
    )

    args = parser.parse_args()
    scan_dir = Path(args.directory).resolve()

    if not scan_dir.is_dir():
        print(f"❌  Not a directory: {scan_dir}")
        sys.exit(1)

    output_path = (
        Path(args.output).resolve() if args.output
        else scan_dir / "index.html"
    )

    if args.watch:
        generate_index(scan_dir, output_path)
        watch_mode(scan_dir, output_path)
    else:
        generate_index(scan_dir, output_path)


if __name__ == "__main__":
    main()