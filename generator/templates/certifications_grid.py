"""SVG template: Certifications Grid — animated certification badges (850xN)."""

from generator.utils import esc

WIDTH = 850


def _build_cert_card(index, x, y, w, h, color, cert, theme):
    """Build a single certification card."""
    delay = index * 0.25
    name = cert.get("name", "")
    year = cert.get("year", "")
    issuer = cert.get("issuer", "")

    parts = []

    # Card container with entry animation
    parts.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 12" to="0 0" dur="0.5s" begin="{delay}s" fill="freeze"/>'
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

    # Checkmark badge (top center)
    cx = x + w / 2
    badge_y = y + 18
    parts.append(
        f'    <circle cx="{cx}" cy="{badge_y}" r="10" fill="{color}" opacity="0.12">'
        f'      <animate attributeName="opacity" values="0.12;0.25;0.12" dur="3s" '
        f'begin="{delay}s" repeatCount="indefinite"/>'
        f'    </circle>'
    )
    parts.append(
        f'    <path d="M {cx - 4} {badge_y} L {cx - 1} {badge_y + 3} L {cx + 4} {badge_y - 3}" '
        f'fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>'
    )

    # Certification name
    parts.append(
        f'    <text x="{cx}" y="{y + 45}" text-anchor="middle" fill="{theme["text_bright"]}" '
        f'font-size="10" font-weight="bold" font-family="monospace">{esc(name)}</text>'
    )

    # Issuer + year
    if issuer and year:
        info_text = f"{issuer}  |  {year}"
    elif year:
        info_text = year
    else:
        info_text = issuer
    if info_text:
        parts.append(
            f'    <text x="{cx}" y="{y + 60}" text-anchor="middle" fill="{theme["text_faint"]}" '
            f'font-size="9" font-family="monospace">{esc(info_text)}</text>'
        )

    # Scan line inside card
    parts.append(
        f'    <rect x="{x}" y="{y}" width="{w}" height="1.5" fill="{color}" opacity="0.1">'
        f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {h}" '
        f'dur="3s" begin="{delay + 0.3}s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append('  </g>')
    return "\n".join(parts)


def render(certifications: list, theme: dict) -> str:
    """Render the certifications grid SVG."""
    if not certifications:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="120" viewBox="0 0 {WIDTH} 120">
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="119" rx="12" ry="12"
        fill="{theme['depth']}" stroke="{theme['grid']}" stroke-width="1"/>
  <text x="{WIDTH / 2}" y="60" fill="{theme['text_faint']}" font-size="12"
        font-family="monospace" text-anchor="middle" dominant-baseline="middle">No certifications configured</text>
</svg>'''

    cols = 3
    card_w = 250
    card_h = 75
    gap_x = 25
    gap_y = 20
    start_x = (WIDTH - (cols * card_w + (cols - 1) * gap_x)) / 2
    start_y = 55

    cert_colors = [
        theme.get("pipeline_teal", "#00c8a0"),
        theme.get("spark_orange", "#ff6b35"),
        theme.get("lake_green", "#2ecc71"),
    ]

    cards = []
    for i, cert in enumerate(certifications):
        col = i % cols
        row = i // cols
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        color = cert_colors[i % len(cert_colors)]
        cards.append(_build_cert_card(i, x, y, card_w, card_h, color, cert, theme))

    cards_str = "\n".join(cards)
    rows = (len(certifications) + cols - 1) // cols
    total_height = start_y + rows * (card_h + gap_y) - gap_y + 30
    height = max(140, total_height)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <!-- Background -->
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" ry="12"
        fill="{theme['depth']}" stroke="{theme['grid']}" stroke-width="1"/>

  <!-- Title -->
  <text x="30" y="38" fill="{theme['text_faint']}" font-size="11" font-family="monospace" letter-spacing="3">CERTIFICATIONS &amp; ACCREDITATIONS</text>

  <!-- Certification cards -->
{cards_str}
</svg>'''
