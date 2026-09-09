"""SVG template: Neofetch-inspired profile header for a data engineer."""

import datetime as dt

from generator.utils import esc

WIDTH, HEIGHT = 850, 360


def _months_since(date_text: str) -> str:
    """Return a compact uptime-like duration from a YYYY-MM-DD start date."""
    try:
        start = dt.date.fromisoformat(date_text)
    except (TypeError, ValueError):
        return "active"

    today = dt.date.today()
    months = max(0, (today.year - start.year) * 12 + today.month - start.month)
    return f"{months // 12:02d}y {months % 12:02d}m"


def _cube(cx: float, top_y: float, size: float, color: str, label: str, delay: float, theme: dict) -> str:
    """Build one floating isometric cube with a readable system label."""
    depth = size * 0.22
    height = size * 0.72
    left = cx - size / 2
    right = cx + size / 2
    bottom = top_y + height
    front_y = top_y + depth
    dark = theme["depth"]
    surface = theme["lake_surface"]
    bright = theme["text_bright"]

    return f'''  <g opacity="0" filter="url(#cube-glow)">
    <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{delay}s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,-7; 0,0" dur="4.5s" begin="{delay}s" repeatCount="indefinite"/>
    <polygon points="{left:.1f},{top_y:.1f} {cx:.1f},{top_y - depth:.1f} {right:.1f},{top_y:.1f} {cx:.1f},{front_y:.1f}" fill="{color}" fill-opacity="0.42" stroke="{color}" stroke-width="1"/>
    <polygon points="{left:.1f},{top_y:.1f} {cx:.1f},{front_y:.1f} {cx:.1f},{bottom + depth:.1f} {left:.1f},{bottom:.1f}" fill="{surface}" stroke="{color}" stroke-opacity="0.8" stroke-width="1"/>
    <polygon points="{cx:.1f},{front_y:.1f} {right:.1f},{top_y:.1f} {right:.1f},{bottom:.1f} {cx:.1f},{bottom + depth:.1f}" fill="{dark}" stroke="{color}" stroke-opacity="0.72" stroke-width="1"/>
    <path d="M {left + 10:.1f} {top_y + 8:.1f} L {cx - 5:.1f} {front_y - 1:.1f} M {left + 7:.1f} {top_y + 20:.1f} L {cx - 5:.1f} {front_y + 11:.1f}" stroke="{bright}" stroke-opacity="0.3" stroke-width="0.7"/>
    <circle cx="{cx + 12:.1f}" cy="{top_y + 9:.1f}" r="2.2" fill="{bright}">
      <animate attributeName="opacity" values="0.25;1;0.25" dur="2.2s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>
    <text x="{cx:.1f}" y="{bottom - 15:.1f}" fill="{bright}" font-size="9" font-weight="bold" font-family="monospace" text-anchor="middle">{esc(label)}</text>
  </g>'''


def _stack(data_layers: list, theme: dict) -> str:
    """Build the left-side floating data stack and its connectors."""
    colors = [theme["pipeline_teal"], theme["spark_orange"], theme["lake_green"]]
    labels = ["INGEST", "TRANSFORM", "LAKEHOUSE", "SERVE"]
    placements = [(112, 78, 76), (205, 139, 84), (105, 220, 92), (245, 227, 66)]
    parts = []

    for index, (cx, y, size) in enumerate(placements):
        color = colors[index % len(colors)]
        label = labels[index]
        parts.append(_cube(cx, y, size, color, label, index * 0.18, theme))

    # Dashed data routes stay behind the cubes.
    routes = [(132, 131, 180, 137, colors[0]), (177, 204, 151, 219, colors[1]), (192, 266, 238, 256, colors[2])]
    for x1, y1, x2, y2, color in routes:
        parts.insert(0, f'  <path d="M {x1} {y1} C {x1 + 25} {y1 + 14}, {x2 - 25} {y2 - 14}, {x2} {y2}" fill="none" stroke="{color}" stroke-width="0.8" stroke-dasharray="3 6" opacity="0.5"/>')

    for index, color in enumerate(colors):
        parts.insert(1, f'''  <circle cx="0" cy="0" r="2.2" fill="{color}">
    <animateMotion path="M 62 {127 + index * 65} C 98 {145 + index * 64}, 157 {153 + index * 54}, 229 {170 + index * 43}" dur="5.5s" begin="{-index * 1.8}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.86;1" dur="5.5s" begin="{-index * 1.8}s" repeatCount="indefinite"/>
  </circle>''')

    return "\n".join(parts)


def _terminal_lines(profile: dict, theme: dict) -> str:
    """Build the Neofetch-style right-side system specification."""
    name = profile.get("name", "Bernado Diniz")
    tagline = profile.get("tagline", "Data Engineer")
    company = profile.get("company", "Zetta / UFLA")
    location = profile.get("location", "Lavras, MG - Brazil")
    uptime = _months_since(profile.get("career_start", "2025-08-01"))
    focus = " · ".join(profile.get("focus", ["DATA ENGINEERING", "CLOUD", "BIG DATA"]))
    rows = [
        ("OS", "DATA ENGINEERING / PORTFOLIO"),
        ("Host", company.upper()),
        ("Kernel", "CLOUD · LAKEHOUSE · BIG DATA"),
        ("Uptime", f"{uptime} / building pipelines"),
        ("Role", tagline.upper()),
        ("Location", location.upper()),
        ("Focus", focus),
        ("Languages", "PYTHON · SQL · PYSPARK · C++"),
        ("Systems", "AWS · AZURE · DATABRICKS · SPARK"),
        ("Storage", "DELTA LAKE · ZARR · ICECHUNK"),
        ("Status", "OPEN TO OPPORTUNITIES"),
    ]
    parts = []
    x_label = 420
    x_value = 510
    for index, (label, value) in enumerate(rows):
        y = 82 + index * 21
        color = theme["pipeline_teal"] if label in {"Role", "Status"} else theme["spark_orange"]
        parts.append(
            f'  <text x="{x_label}" y="{y}" fill="{color}" font-size="10" font-family="monospace">{esc(label + ":")}</text>'
            f'<text x="{x_value}" y="{y}" fill="{theme["text_bright"]}" font-size="10" font-family="monospace">{esc(value)}</text>'
        )
    return "\n".join(parts)


def render(config: dict, theme: dict, data_layers: list, projects: list) -> str:
    """Render a terminal-like profile header with animated 3D data cubes."""
    profile = config.get("profile", {})
    name = profile.get("name", "Bernado Diniz")
    tagline = profile.get("tagline", "Data Engineer")
    stack = _stack(data_layers, theme)
    terminal = _terminal_lines(profile, theme)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <filter id="cube-glow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="2.4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="terminal-grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 32 0 L 0 0 0 32" fill="none" stroke="{theme['grid']}" stroke-width="0.5" opacity="0.15"/>
    </pattern>
  </defs>

  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{theme['depth']}" stroke="{theme['grid']}" stroke-width="1"/>
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="11" fill="url(#terminal-grid)"/>

  <!-- Terminal bar -->
  <rect x="1" y="1" width="{WIDTH - 2}" height="35" rx="11" fill="{theme['lake_surface']}"/>
  <path d="M 1 36 H {WIDTH - 1}" stroke="{theme['grid']}"/>
  <circle cx="20" cy="18" r="4" fill="{theme['spark_orange']}"/>
  <circle cx="34" cy="18" r="4" fill="#e5c45c"/>
  <circle cx="48" cy="18" r="4" fill="{theme['pipeline_teal']}"/>
  <text x="70" y="22" fill="{theme['text_dim']}" font-size="10" font-family="monospace">bernado@data-stack:~</text>
  <text x="815" y="22" fill="{theme['text_faint']}" font-size="9" font-family="monospace" text-anchor="end">neofetch --profile</text>

  <!-- Left visual: floating data cubes -->
  <text x="28" y="58" fill="{theme['text_faint']}" font-size="9" font-family="monospace" letter-spacing="1.5">DATA SYSTEM / 3D PIPELINE</text>
{stack}
  <text x="28" y="327" fill="{theme['text_faint']}" font-size="9" font-family="monospace">[●] pipeline online / no manual retries</text>

  <!-- Divider -->
  <line x1="380" y1="52" x2="380" y2="329" stroke="{theme['grid']}" stroke-dasharray="2 7"/>

  <!-- Right visual: system specification -->
  <text x="408" y="58" fill="{theme['text_faint']}" font-size="9" font-family="monospace" letter-spacing="1.5">{esc(name.upper())} / SYSTEM INFO</text>
{terminal}
  <line x1="420" y1="318" x2="815" y2="318" stroke="{theme['grid']}" stroke-dasharray="3 6"/>
  <text x="420" y="333" fill="{theme['text_faint']}" font-size="8" font-family="monospace">{esc(tagline.upper())} · DATA SYSTEMS THAT HOLD UP</text>
</svg>'''
