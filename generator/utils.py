"""Utility functions, color maps, math helpers, and SVG icon paths for datastack-profile."""

import re
import math
import hashlib
from xml.sax.saxutils import escape as xml_escape

HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

# Default Data Lake / Pipeline theme palette
DEFAULT_THEME = {
    "depth": "#0b1120",
    "lake_surface": "#111d2e",
    "grid": "#1e3a5f",
    "pipeline_teal": "#00c8a0",
    "spark_orange": "#ff6b35",
    "lake_green": "#2ecc71",
    "text_bright": "#e6f1ff",
    "text_dim": "#8da9c4",
    "text_faint": "#4a6582",
}


def resolve_theme(user_theme: dict) -> dict:
    """Merge user theme overrides with defaults, returning a complete theme dict."""
    return {**DEFAULT_THEME, **(user_theme or {})}


def resolve_layer_colors(data_layers: list, theme: dict) -> list:
    """Return a list of hex color strings, one per data layer, resolved from the theme."""
    fallback = theme.get("pipeline_teal", "#00c8a0")
    return [
        theme.get(layer.get("color", "pipeline_teal"), fallback)
        for layer in data_layers
    ]


# GitHub Linguist colors for popular languages
LANGUAGE_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Java": "#b07219",
    "C#": "#178600",
    "C++": "#f34b7d",
    "C": "#555555",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Ruby": "#701516",
    "PHP": "#4F5D95",
    "Swift": "#F05138",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "Scala": "#c22d40",
    "R": "#198CE7",
    "Lua": "#000080",
    "Shell": "#89e051",
    "PowerShell": "#012456",
    "Haskell": "#5e5086",
    "Elixir": "#6e4a7e",
    "Clojure": "#db5855",
    "Erlang": "#B83998",
    "Julia": "#a270ba",
    "Vim Script": "#199f4b",
    "Objective-C": "#438eff",
    "Perl": "#0298c3",
    "MATLAB": "#e16737",
    "Groovy": "#4298b8",
    "Vue": "#41b883",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "SCSS": "#c6538c",
    "Dockerfile": "#384d54",
    "Makefile": "#427819",
    "HCL": "#844FBA",
    "Nix": "#7e7eff",
    "Zig": "#ec915c",
    "Svelte": "#ff3e00",
    "Astro": "#ff5a03",
    "SQL": "#336791",
    "Jupyter Notebook": "#DA5B0B",
}

# SVG icon paths (16x16 viewBox) — monoline terminal style
COMMIT_ICON = (
    '<path d="M1.5 8a6.5 6.5 0 1 1 13 0 6.5 6.5 0 0 1-13 0z" '
    'fill="none" stroke="currentColor" stroke-width="1.2"/>'
    '<path d="M8 5v6M5 8h6" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>'
)

STAR_ICON = (
    '<path d="M8 1.5l1.8 4.1 4.4.4-3.3 2.9 1 4.3L8 11l-3.7 2.2 1-4.3-3.3-2.9 4.4-.4z" '
    'fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>'
)

PR_ICON = (
    '<path d="M5 2v12M5 4a3 3 0 1 0 0 6 3 3 0 0 0 0-6z" '
    'fill="none" stroke="currentColor" stroke-width="1.2"/>'
    '<path d="M11 8a3 3 0 1 0 0 6 3 3 0 0 0 0-6z" '
    'fill="none" stroke="currentColor" stroke-width="1.2"/>'
    '<path d="M8 5h3M8 11h3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>'
)

ISSUE_ICON = (
    '<circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.2"/>'
    '<circle cx="8" cy="8" r="2" fill="currentColor"/>'
)

REPO_ICON = (
    '<path d="M4 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z" '
    'fill="none" stroke="currentColor" stroke-width="1.2"/>'
    '<path d="M4 7h8M4 11h5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>'
)

METRIC_ICONS = {
    "commits": COMMIT_ICON,
    "stars": STAR_ICON,
    "prs": PR_ICON,
    "issues": ISSUE_ICON,
    "repos": REPO_ICON,
}

METRIC_LABELS = {
    "commits": "Commits",
    "stars": "Stars",
    "prs": "PRs",
    "issues": "Issues",
    "repos": "Repos",
}

METRIC_COLORS = {
    "commits": "pipeline_teal",
    "stars": "spark_orange",
    "prs": "lake_green",
    "issues": "pipeline_teal",
    "repos": "lake_green",
}


def get_language_color(lang: str) -> str:
    """Return the GitHub linguist hex color for a language."""
    return LANGUAGE_COLORS.get(lang, "#8b949e")


def calculate_language_percentages(
    languages: dict, exclude: list, max_display: int
) -> list:
    """Calculate language percentages from byte counts.

    Args:
        languages: dict mapping language name to byte count
        exclude: list of language names to exclude
        max_display: maximum number of languages to show

    Returns:
        list of dicts with keys: name, bytes, percentage, color
    """
    filtered = {k: v for k, v in languages.items() if k not in exclude}
    total = sum(filtered.values())
    if total == 0:
        return []

    sorted_langs = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    top = sorted_langs[:max_display]

    return [
        {
            "name": name,
            "bytes": count,
            "percentage": round((count / total) * 100, 1),
            "color": get_language_color(name),
        }
        for name, count in top
    ]


def format_number(n: int) -> str:
    """Format a number for display. 1234 -> '1.2k', 1000000 -> '1.0M'."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)


def wrap_text(text: str, max_chars: int) -> list:
    """Split text into lines that fit within max_chars width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if current and len(current) + 1 + len(word) > max_chars:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}" if current else word
    if current:
        lines.append(current)
    return lines


def deterministic_random(seed_str: str, count: int, min_val: float, max_val: float) -> list:
    """Generate deterministic pseudo-random values from a seed string."""
    values = []
    for i in range(count):
        h = hashlib.md5(f"{seed_str}_{i}".encode()).hexdigest()
        normalized = int(h[:8], 16) / 0xFFFFFFFF
        values.append(min_val + normalized * (max_val - min_val))
    return values


def esc(text: str) -> str:
    """Escape text for safe embedding in SVG/XML."""
    return xml_escape(str(text), entities={'"': "&quot;", "'": "&apos;"})


def svg_arc_path(cx, cy, r, start_deg, end_deg):
    """Generate SVG path 'd' attribute for a filled arc sector (pie slice)."""
    start_rad = math.radians(start_deg - 90)
    end_rad = math.radians(end_deg - 90)
    x1 = cx + r * math.cos(start_rad)
    y1 = cy + r * math.sin(start_rad)
    x2 = cx + r * math.cos(end_rad)
    y2 = cy + r * math.sin(end_rad)
    large_arc = 1 if (end_deg - start_deg) > 180 else 0
    return f"M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z"


# ── Isometric helpers for tech-stack blocks ──

ISO_X = math.cos(math.radians(30))   # ≈ 0.866
ISO_Y = math.sin(math.radians(30))   # ≈ 0.5


def iso_top_face(cx: float, cy: float, w: float, d: float) -> str:
    """Return SVG path 'd' for an isometric top face (rhomboid).

    cx,cy is the center point projected on screen.
    w = width along x-axis, d = depth along y-axis.
    """
    # Top face corners
    x0 = cx
    y0 = cy - d * ISO_Y
    x1 = cx + w * ISO_X
    y1 = cy - d * ISO_Y + w * ISO_Y
    x2 = cx
    y2 = cy + w * ISO_Y
    x3 = cx - w * ISO_X
    y3 = cy - d * ISO_Y - w * ISO_Y
    return f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} L {x3:.1f} {y3:.1f} Z"


def iso_front_face(cx: float, cy: float, w: float, h: float) -> str:
    """Return SVG path 'd' for an isometric front face (parallelogram).

    cx,cy is the projected center.
    w = width, h = height (vertical).
    """
    x0 = cx - w * ISO_X
    y0 = cy
    x1 = cx + w * ISO_X
    y1 = cy + w * ISO_Y * 2  # adjust for iso slope
    x2 = cx + w * ISO_X
    y2 = cy + h + w * ISO_Y * 2
    x3 = cx - w * ISO_X
    y3 = cy + h
    return f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} L {x3:.1f} {y3:.1f} Z"


def iso_right_face(cx: float, cy: float, d: float, h: float) -> str:
    """Return SVG path 'd' for an isometric right-side face.

    cx,cy is the projected center.
    d = depth, h = height (vertical).
    """
    x0 = cx
    y0 = cy
    x1 = cx + d * ISO_X
    y1 = cy + d * ISO_Y
    x2 = cx + d * ISO_X
    y2 = cy + h + d * ISO_Y
    x3 = cx
    y3 = cy + h
    return f"M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} L {x3:.1f} {y3:.1f} Z"
