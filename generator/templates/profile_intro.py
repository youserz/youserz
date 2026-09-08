"""SVG template: editorial profile statement matching the portfolio identity."""

from generator.utils import esc

WIDTH, HEIGHT = 850, 176


def _focus_pills(focus: list, theme: dict) -> str:
    """Build centered animated focus labels."""
    labels = focus[:3] or ["DATA ENGINEERING", "CLOUD", "BIG DATA"]
    colors = [theme["pipeline_teal"], theme["spark_orange"], theme["lake_green"]]
    widths = [max(76, len(label) * 7 + 22) for label in labels]
    gap = 13
    start_x = (WIDTH - sum(widths) - gap * (len(labels) - 1)) / 2
    parts = []

    x = start_x
    for index, (label, width) in enumerate(zip(labels, widths)):
        color = colors[index % len(colors)]
        delay = index * 0.16
        parts.append(
            f'  <g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 -5" to="0 0" dur="0.45s" begin="{delay}s" fill="freeze"/>'
            f'    <rect x="{x:.1f}" y="36" width="{width}" height="24" rx="5" fill="{theme["lake_surface"]}" stroke="{color}" stroke-opacity="0.55"/>'
            f'    <circle cx="{x + 12:.1f}" cy="48" r="2.5" fill="{color}">'
            f'<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</circle>'
            f'    <text x="{x + width / 2 + 5:.1f}" y="52" fill="{theme["text_bright"]}" font-size="10" font-family="monospace" text-anchor="middle">{esc(label)}</text>'
            f'  </g>'
        )
        x += width + gap

    return "\n".join(parts)


def _flow_line(theme: dict) -> str:
    """Build a restrained animated data-flow line along the bottom edge."""
    colors = [theme["pipeline_teal"], theme["spark_orange"], theme["lake_green"]]
    particles = []
    for index, color in enumerate(colors):
        particles.append(
            f'  <circle cx="0" cy="153" r="2" fill="{color}">'
            f'    <animate attributeName="cx" from="80" to="770" dur="6.5s" begin="{-index * 2.15}s" repeatCount="indefinite"/>'
            f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.88;1" dur="6.5s" begin="{-index * 2.15}s" repeatCount="indefinite"/>'
            f'  </circle>'
        )
    return "\n".join(particles)


def render(profile: dict, theme: dict) -> str:
    """Render the profile statement SVG."""
    focus = profile.get("focus", ["DATA ENGINEERING", "CLOUD", "BIG DATA"])
    headline = profile.get("headline", "Dados que aguentam o mundo real.")
    summary = profile.get(
        "summary",
        "Do byte bruto à camada analítica — pipelines observáveis, cloud e sistemas de dados que sustentam decisões.",
    )

    pills = _focus_pills(focus, theme)
    particles = _flow_line(theme)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <pattern id="intro-grid" width="42" height="42" patternUnits="userSpaceOnUse">
      <path d="M 42 0 L 0 0 0 42" fill="none" stroke="{theme['grid']}" stroke-width="0.5" opacity="0.16"/>
    </pattern>
    <filter id="intro-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="{theme['depth']}" stroke="{theme['grid']}"/>
  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="11" fill="url(#intro-grid)"/>

  <text x="24" y="23" fill="{theme['text_faint']}" font-size="8" font-family="monospace" letter-spacing="2">PROFILE SIGNAL / 2026</text>
  <g transform="translate(731 18)">
    <circle cx="0" cy="0" r="3" fill="{theme['pipeline_teal']}" filter="url(#intro-glow)">
      <animate attributeName="opacity" values="0.35;1;0.35" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="10" y="3" fill="{theme['text_faint']}" font-size="8" font-family="monospace" letter-spacing="1">AVAILABLE</text>
  </g>

{pills}

  <text x="{WIDTH / 2}" y="96" fill="{theme['text_bright']}" font-size="21" font-weight="600" font-family="sans-serif" text-anchor="middle">{esc(headline)}</text>
  <text x="{WIDTH / 2}" y="121" fill="{theme['text_dim']}" font-size="11" font-family="sans-serif" text-anchor="middle">{esc(summary)}</text>

  <line x1="80" y1="153" x2="770" y2="153" stroke="{theme['grid']}" stroke-width="1" stroke-dasharray="3 8"/>
  <circle cx="80" cy="153" r="3" fill="{theme['depth']}" stroke="{theme['pipeline_teal']}"/>
  <circle cx="770" cy="153" r="3" fill="{theme['depth']}" stroke="{theme['spark_orange']}"/>
{particles}
</svg>'''
