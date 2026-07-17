"""SVG template: Experience Timeline — animated vertical pipeline of professional roles (850xN)."""

from generator.utils import esc

WIDTH = 850


def _build_timeline_node(y, color, theme, delay):
    """Build a pulsing timeline node."""
    cx = 60
    return (
        f'  <g>'
        f'    <circle cx="{cx}" cy="{y}" r="6" fill="{color}" opacity="0.2">'
        f'      <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" '
        f'begin="{delay}s" repeatCount="indefinite"/>'
        f'    </circle>'
        f'    <circle cx="{cx}" cy="{y}" r="3" fill="{color}" opacity="0.9"/>'
        f'    <circle cx="{cx}" cy="{y}" r="1.5" fill="{theme["text_bright"]}" opacity="0.8"/>'
        f'  </g>'
    )


def _build_timeline_connector(y1, y2, color):
    """Build a dashed line connecting two timeline nodes with pulse."""
    return (
        f'  <line x1="60" y1="{y1}" x2="60" y2="{y2}" '
        f'stroke="{color}" stroke-width="1" stroke-dasharray="4,4" opacity="0.3">'
        f'    <animate attributeName="opacity" values="0.2;0.4;0.2" dur="4s" repeatCount="indefinite"/>'
        f'  </line>'
    )


def _build_experience_card(index, x, y, w, h, color, exp, theme):
    """Build a single experience card with entry animation."""
    delay = index * 0.35
    bullets = exp.get("bullets", [])

    parts = []

    # Card container with entry animation
    parts.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="15 0" to="0 0" dur="0.5s" begin="{delay}s" fill="freeze"/>'
    )

    # Card background
    parts.append(
        f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" ry="8" '
        f'fill="{theme["lake_surface"]}" stroke="{color}" stroke-width="0.8" opacity="0.85"/>'
    )

    # Inner fill
    parts.append(
        f'    <rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="7" ry="7" '
        f'fill="{theme["depth"]}" opacity="0.4"/>'
    )

    # Role title
    parts.append(
        f'    <text x="{x + 14}" y="{y + 22}" fill="{color}" '
        f'font-size="13" font-weight="bold" font-family="monospace">{esc(exp["role"])}</text>'
    )

    # Company + period
    company_text = f"{exp.get('company', '')}  |  {exp.get('period', '')}"
    parts.append(
        f'    <text x="{x + 14}" y="{y + 40}" fill="{theme["text_dim"]}" '
        f'font-size="10" font-family="monospace">{esc(company_text)}</text>'
    )

    # Bullets
    for i, bullet in enumerate(bullets[:3]):
        by = y + 58 + i * 16
        parts.append(
            f'    <circle cx="{x + 18}" cy="{by - 3}" r="1.5" fill="{color}" opacity="0.6"/>'
        )
        parts.append(
            f'    <text x="{x + 26}" y="{by}" fill="{theme["text_dim"]}" '
            f'font-size="9" font-family="sans-serif">{esc(bullet)}</text>'
        )

    # Scan line inside card
    parts.append(
        f'    <rect x="{x}" y="{y}" width="{w}" height="1.5" fill="{color}" opacity="0.12">'
        f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {h}" '
        f'dur="4s" begin="{delay + 0.4}s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append('  </g>')
    return "\n".join(parts)


def render(experiences: list, theme: dict) -> str:
    """Render the experience timeline SVG."""
    if not experiences:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="120" viewBox="0 0 {WIDTH} 120">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="119" rx="12" ry="12"
        fill="{theme['depth']}" stroke="{theme['grid']}" stroke-width="1"/>
  <text x="{WIDTH / 2}" y="60" fill="{theme['text_faint']}" font-size="12"
        font-family="monospace" text-anchor="middle" dominant-baseline="middle">No experience configured</text>
</svg>'''

    # Layout constants
    card_w = 720
    card_h = 95
    start_y = 55
    gap_y = 25
    card_x = 95

    timeline_colors = [
        theme.get("pipeline_teal", "#00c8a0"),
        theme.get("spark_orange", "#ff6b35"),
        theme.get("lake_green", "#2ecc71"),
    ]

    cards = []
    nodes = []
    connectors = []

    for i, exp in enumerate(experiences):
        color = timeline_colors[i % len(timeline_colors)]
        cy = start_y + i * (card_h + gap_y) + card_h / 2

        # Node
        nodes.append(_build_timeline_node(cy, color, theme, i * 0.3))

        # Connector to next node
        if i < len(experiences) - 1:
            next_y = start_y + (i + 1) * (card_h + gap_y) + card_h / 2
            connectors.append(_build_timeline_connector(cy, next_y, color))

        # Card
        card_y = start_y + i * (card_h + gap_y)
        cards.append(
            _build_experience_card(i, card_x, card_y, card_w, card_h, color, exp, theme)
        )

    cards_str = "\n".join(cards)
    nodes_str = "\n".join(nodes)
    connectors_str = "\n".join(connectors)

    total_height = start_y + len(experiences) * (card_h + gap_y) - gap_y + 30
    height = max(140, total_height)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <!-- Background -->
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" ry="12"
        fill="{theme['depth']}" stroke="{theme['grid']}" stroke-width="1"/>

  <!-- Title -->
  <text x="30" y="38" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">PROFESSIONAL EXPERIENCE</text>

  <!-- Timeline connectors (draw first, behind) -->
{connectors_str}

  <!-- Experience cards -->
{cards_str}

  <!-- Timeline nodes -->
{nodes_str}
</svg>'''
