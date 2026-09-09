"""SVG template: colored Neofetch output with ASCII data cubes."""

import datetime as dt

from generator.utils import esc, format_number

WIDTH, HEIGHT = 920, 520


def _months_since(date_text: str) -> str:
    """Return a compact uptime-like duration from a YYYY-MM-DD start date."""
    try:
        start = dt.date.fromisoformat(date_text)
    except (TypeError, ValueError):
        return "active"

    today = dt.date.today()
    months = max(0, (today.year - start.year) * 12 + today.month - start.month)
    return f"{months // 12:02d}y {months % 12:02d}m"


def _ascii_art(theme: dict) -> str:
    """Render an extruded 3D data gear from ASCII characters."""
    acid = theme["pipeline_teal"]
    coral = theme["spark_orange"]
    blue = theme["lake_green"]
    dim = theme["text_dim"]
    bright = theme["text_bright"]

    lines = [
        ("                    ___[###]___", coral),
        ("                _.-'           '-._", bright),
        ("            _.-'    .-------.      '-._", dim),
        (r"        ___/___    /    (O)  \     ___\___", acid),
        (r"       /  /   \___/      |      \___/   \  \_", bright),
        (r"  ____/__/       |   (O)--+--(O)  |       \__\____", coral),
        (r" [###]          |     \  |  /     |          [###]", acid),
        (r" /   |          |      \(O)/      |          |   \_", bright),
        (r"[    |          |       /|\       |          |    ]", blue),
        ("|    |          |    (O)-+-(O)    |          |    |", acid),
        (r"[    |           \       |       /           |    ]", bright),
        (r" \   |     ___    '------|------'    ___    |   /", dim),
        (r"  [###]___/   \___       |      ___/   \___[###]", coral),
        (r"      \  \       '-._____|___.-'       /  /", bright),
        (r"       \__\______               _______/__/", blue),
        (r"            \    '-------------'       /", dim),
        (r"             \\\\\\\\\\\\\\\\\_", blue),
        (r"              \_____________________\_", bright),
        ("                 '---[#####]---'", coral),
        ("", dim),
        ("                 3D DATA GEAR", acid),
        ("        ingest / process / govern / serve", dim),
        ("", dim),
        ("              nodes: 06 / links: 08", blue),
        ("              pipeline status: ONLINE", acid),
    ]

    rendered = []
    for index, (line, color) in enumerate(lines):
        y = 85 + index * 16.0
        rendered.append(
            f'  <text x="10" y="{y:.1f}" fill="{color}" font-size="10.4" '
            f'font-family="Consolas, Courier New, monospace" xml:space="preserve">{esc(line)}</text>'
        )

    return "\n".join(rendered)


def _system_rows(config: dict, stats: dict, theme: dict) -> str:
    """Render the right-side Neofetch fields."""
    profile = config.get("profile", {})
    username = config.get("username", "youserz")
    social = config.get("social", {})
    uptime = _months_since(profile.get("career_start", "2025-08-01"))
    repo_count = format_number(stats.get("repos", 0))
    pr_count = format_number(stats.get("prs", 0))
    star_count = format_number(stats.get("stars", 0))

    rows = [
        ("OS", "Data Engineering / Lakehouse", "acid"),
        ("Host", profile.get("company", "Zetta / UFLA"), "coral"),
        ("Kernel", "Cloud + Big Data", "blue"),
        ("Uptime", f"{uptime} / since Aug 2025", "acid"),
        ("Role", "Data Engineer Jr", "coral"),
        ("Location", profile.get("location", "Lavras, MG - Brazil"), "blue"),
        ("", "", "gap"),
        ("Code", "Python / SQL / PySpark / C++", "coral"),
        ("Data", "Spark / Xarray / Pandas", "blue"),
        ("Cloud", "AWS / Azure / Databricks", "acid"),
        ("Storage", "Delta Lake / Zarr / Icechunk", "coral"),
        ("Ops", "Docker / Git / Unity Catalog / IAM", "blue"),
        ("", "", "gap"),
        ("Certs", "AWS CCP + Cloud Quest + Partner x3", "acid"),
        ("Security", "Google Cybersecurity", "coral"),
        ("GenAI", "Fundacao Bradesco", "blue"),
        ("Status", "OPEN TO OPPORTUNITIES", "acid"),
        ("GitHub", f"{repo_count} repos / {pr_count} PRs / {star_count} stars", "coral"),
        ("", "", "gap"),
        ("Email", social.get("email", "bernado.felix@estudante.ufla.br"), "blue"),
        ("LinkedIn", f"linkedin.com/in/{social.get('linkedin', 'bernadodiniz')}", "acid"),
        ("Portfolio", f"{username}.github.io/portifolio", "coral"),
    ]

    colors = {
        "acid": theme["pipeline_teal"],
        "coral": theme["spark_orange"],
        "blue": theme["lake_green"],
    }
    x_key, x_value = 430, 535
    y = 92
    parts = []

    for label, value, color_key in rows:
        if color_key == "gap":
            y += 10
            continue
        color = colors[color_key]
        parts.append(
            f'  <text x="{x_key}" y="{y}" fill="{color}" font-size="10.5" font-weight="bold" '
            f'font-family="Consolas, Courier New, monospace">{esc(label + ":")}</text>'
        )
        parts.append(
            f'  <text x="{x_value}" y="{y}" fill="{theme["text_bright"]}" font-size="10.5" '
            f'font-family="Consolas, Courier New, monospace">{esc(value)}</text>'
        )
        y += 18

    return "\n".join(parts)


def render(config: dict, theme: dict, data_layers: list, projects: list, stats: dict | None = None) -> str:
    """Render a GitHub-ready, colored Neofetch profile as one SVG."""
    profile = config.get("profile", {})
    username = config.get("username", "youserz")
    name = profile.get("name", "Bernado Diniz")
    stats = stats or {}
    art = _ascii_art(theme)
    system_rows = _system_rows(config, stats, theme)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <filter id="soft-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="screen-grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{theme['grid']}" stroke-width="0.35" opacity="0.10"/>
    </pattern>
  </defs>

  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" fill="{theme['depth']}" stroke="{theme['grid']}"/>
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="9" fill="url(#screen-grid)"/>

  <!-- Terminal chrome -->
  <rect x="1" y="1" width="{WIDTH - 2}" height="38" rx="9" fill="{theme['lake_surface']}"/>
  <line x1="1" y1="38" x2="{WIDTH - 1}" y2="38" stroke="{theme['grid']}"/>
  <circle cx="19" cy="19" r="4" fill="{theme['spark_orange']}"/>
  <circle cx="34" cy="19" r="4" fill="#e5c45c"/>
  <circle cx="49" cy="19" r="4" fill="{theme['pipeline_teal']}"/>
  <text x="70" y="23" fill="{theme['text_dim']}" font-size="10" font-family="Consolas, Courier New, monospace">bernado@data-stack:~</text>
  <text x="892" y="23" fill="{theme['text_faint']}" font-size="9" font-family="Consolas, Courier New, monospace" text-anchor="end">README.md / neofetch</text>

  <!-- ASCII side -->
  <g filter="url(#soft-glow)">
{art}
  </g>
  <text x="22" y="496" fill="{theme['text_faint']}" font-size="9" font-family="Consolas, Courier New, monospace">[data flows down / decisions flow up]</text>

  <!-- Neofetch side -->
  <text x="430" y="61" fill="{theme['pipeline_teal']}" font-size="13" font-weight="bold" font-family="Consolas, Courier New, monospace">{esc(username)}@data-stack</text>
  <text x="430" y="76" fill="{theme['text_faint']}" font-size="9" font-family="Consolas, Courier New, monospace">-----------------------------------------------</text>
{system_rows}

  <!-- Terminal palette and cursor -->
  <text x="430" y="478" fill="{theme['pipeline_teal']}" font-size="13" font-family="Consolas, Courier New, monospace">[###]</text>
  <text x="472" y="478" fill="{theme['spark_orange']}" font-size="13" font-family="Consolas, Courier New, monospace">[###]</text>
  <text x="514" y="478" fill="{theme['lake_green']}" font-size="13" font-family="Consolas, Courier New, monospace">[###]</text>
  <text x="556" y="478" fill="{theme['text_bright']}" font-size="13" font-family="Consolas, Courier New, monospace">[###]</text>
  <text x="598" y="478" fill="{theme['text_faint']}" font-size="13" font-family="Consolas, Courier New, monospace">[###]</text>
  <text x="430" y="501" fill="{theme['text_dim']}" font-size="9.5" font-family="Consolas, Courier New, monospace">{esc(name)}: dados que aguentam o mundo real.</text>
  <rect x="704" y="490" width="7" height="13" fill="{theme['pipeline_teal']}">
    <animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/>
  </rect>
</svg>'''
