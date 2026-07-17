"""SVG template: HUD Data Dashboard — isometric 3D cubes (left) + futuristic radar (right).

Internal neon palette hardcoded for a premium HUD/cyberpunk aesthetic.
"""

import math
from generator.utils import esc

WIDTH = 850

# ── Neon HUD palette ─────────────────────────────────────────────
NEON = {
    "bg": "#0A1020",
    "surface": "#0D1832",
    "grid": "#162340",
    "divider": "#1c3050",
    "text_bright": "#e0f0ff",
    "text_dim": "#8da9c4",
    "text_faint": "#5a7088",
}

# Layer colors by index (cyan, orange, green, blue)
LAYER_NEON = ["#00E5FF", "#FF7A30", "#29FF87", "#00D4FF"]


def _lighten(hex_color: str, factor: float = 1.6) -> str:
    h = hex_color.lstrip("#")
    r = min(255, int(int(h[0:2], 16) * factor))
    g = min(255, int(int(h[2:4], 16) * factor))
    b = min(255, int(int(h[4:6], 16) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def _darken(hex_color: str, factor: float = 0.45) -> str:
    h = hex_color.lstrip("#")
    r = int(int(h[0:2], 16) * factor)
    g = int(int(h[2:4], 16) * factor)
    b = int(int(h[4:6], 16) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


# ── Cube builder ──────────────────────────────────────────────────

def _build_cube(i, cx, y, w, h, color, title, items):
    """Build a 3D isometric data cube.

    Args:
        i: layer index for animation delay
        cx: horizontal center of the cube
        y: top y of the front face
        w, h: front face dimensions
        color: neon accent color
        title: layer name
        items: list of technology strings
    """
    delay = i * 0.3
    fx1, fy1 = cx - w / 2, y
    fx2, fy2 = cx + w / 2, y + h

    top_color = _lighten(color, 1.5)
    right_color = _darken(color, 0.4)
    shadow_color = _darken(color, 0.15)

    # ── Top face (small parallelogram above front face) ──
    top_h = 8
    tx1, ty1 = fx1 + 6, fy1
    tx2, ty2 = fx2 - 2, fy1
    tx3, ty3 = fx2 + 4, fy1 - top_h
    tx4, ty4 = fx1 + 8, fy1 - top_h

    # ── Right face (thin strip on the right) ──
    rx1, ry1 = fx2, fy1
    rx2, ry2 = fx2 + 6, fy1 - top_h
    rx3, ry3 = fx2 + 6, fy2 - top_h
    rx4, ry4 = fx2, fy2

    parts = []
    parts.append(
        f'  <g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{delay}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" dur="0.5s" begin="{delay}s" fill="freeze"/>'
    )

    # Shadow below cube
    parts.append(
        f'    <rect x="{fx1 + 2}" y="{fy2 + 2}" width="{w - 4}" height="6" rx="2" '
        f'fill="{shadow_color}" opacity="0.18" filter="url(#shadow-blur)"/>'
    )

    # Right face (draw first, behind front)
    parts.append(
        f'    <path d="M {rx1:.1f} {ry1:.1f} L {rx2:.1f} {ry2:.1f} L {rx3:.1f} {ry3:.1f} L {rx4:.1f} {ry4:.1f} Z" '
        f'fill="{right_color}" opacity="0.7"/>'
    )

    # Top face
    parts.append(
        f'    <path d="M {tx1:.1f} {ty1:.1f} L {tx2:.1f} {ty2:.1f} L {tx3:.1f} {ty3:.1f} L {tx4:.1f} {ty4:.1f} Z" '
        f'fill="{top_color}" opacity="0.85"/>'
    )

    # Top edge highlight glow
    parts.append(
        f'    <line x1="{fx1 + 6}" y1="{fy1}" x2="{fx2 - 6}" y2="{fy1}" '
        f'stroke="{color}" stroke-width="1.2" opacity="0.9" filter="url(#edge-glow)"/>'
    )

    # Front face
    parts.append(
        f'    <rect x="{fx1:.1f}" y="{fy1:.1f}" width="{w}" height="{h}" rx="5" ry="5" '
        f'fill="{NEON["surface"]}" stroke="{color}" stroke-width="1" opacity="0.92"/>'
    )

    # Front face inner dark fill
    parts.append(
        f'    <rect x="{fx1 + 2:.1f}" y="{fy1 + 2:.1f}" width="{w - 4}" height="{h - 4}" rx="4" ry="4" '
        f'fill="{NEON["bg"]}" opacity="0.55"/>'
    )

    # Title centered at top of front face
    parts.append(
        f'    <text x="{cx}" y="{fy1 + 22}" text-anchor="middle" fill="{color}" '
        f'font-size="12" font-weight="bold" font-family="monospace" filter="url(#text-glow)">{esc(title)}</text>'
    )

    # Capsules grid
    capsule_w = 90
    capsule_h = 16
    cap_gap_x = 5
    cap_gap_y = 3
    caps_per_row = 3
    cap_start_y = fy1 + 32
    inner_pad = 10

    total_row_w = caps_per_row * capsule_w + (caps_per_row - 1) * cap_gap_x
    cap_start_x = cx - total_row_w / 2

    for j, item in enumerate(items):
        row = j // caps_per_row
        col = j % caps_per_row
        bx = cap_start_x + col * (capsule_w + cap_gap_x)
        by = cap_start_y + row * (capsule_h + cap_gap_y)

        cap_delay = delay + j * 0.06
        parts.append(
            f'    <rect x="{bx:.1f}" y="{by:.1f}" width="{capsule_w}" height="{capsule_h}" rx="6" ry="6" '
            f'fill="{color}" opacity="0.10" stroke="{color}" stroke-width="0.5" stroke-opacity="0.3">'
            f'      <animate attributeName="opacity" values="0.10;0.18;0.10" dur="3s" begin="{cap_delay}s" repeatCount="indefinite"/>'
            f'    </rect>'
        )
        parts.append(
            f'    <text x="{bx + capsule_w / 2:.1f}" y="{by + 11:.1f}" text-anchor="middle" '
            f'fill="{NEON["text_dim"]}" font-size="7.5" font-family="monospace">{esc(item)}</text>'
        )

    # Scan line
    parts.append(
        f'    <rect x="{fx1:.1f}" y="{fy1:.1f}" width="{w}" height="1.5" fill="{color}" opacity="0.12">'
        f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {h}" '
        f'dur="3.5s" begin="{delay + 0.3}s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    parts.append('  </g>')
    return "\n".join(parts)


# ── Connection between cubes ──────────────────────────────────────

def _build_connection(cx, y_top, y_bot, color, i):
    """Vertical line + pulsing node between two stacked cubes."""
    delay = i * 0.4
    mid_y = (y_top + y_bot) / 2
    return (
        f'  <g>'
        f'    <line x1="{cx}" y1="{y_top}" x2="{cx}" y2="{y_bot}" '
        f'stroke="{color}" stroke-width="0.8" stroke-dasharray="3,4" opacity="0.35"/>'
        f'    <circle cx="{cx}" cy="{mid_y}" r="4" fill="{NEON["bg"]}" stroke="{color}" stroke-width="1" opacity="0.8">'
        f'      <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" begin="{delay}s" repeatCount="indefinite"/>'
        f'    </circle>'
        f'    <circle cx="{cx}" cy="{mid_y}" r="1.5" fill="{color}" opacity="0.9"/>'
        f'  </g>'
    )


# ── HUD Radar chart ───────────────────────────────────────────────

def _build_radar(cx, cy, radius, layers, colors):
    """Build a futuristic HUD radar chart.

    Args:
        cx, cy: radar center
        radius: outer radius
        layers: list of layer dicts with name
        colors: list of neon hex colors
    """
    n = len(layers)
    angle_step = 360 / n
    parts = []

    # ── Concentric rings ──
    for r in [radius * 0.33, radius * 0.66, radius]:
        parts.append(
            f'    <circle cx="{cx}" cy="{cy}" r="{r:.0f}" '
            f'fill="none" stroke="{NEON["grid"]}" stroke-width="0.6" '
            f'stroke-dasharray="3,6" opacity="0.25"/>'
        )

    # ── Radial divider lines ──
    for i in range(n):
        deg = i * angle_step - 90
        rad = math.radians(deg)
        ex = cx + radius * math.cos(rad)
        ey = cy + radius * math.sin(rad)
        parts.append(
            f'    <line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="{NEON["grid"]}" stroke-width="0.5" opacity="0.3"/>'
        )

    # ── Sector fills (translucent) ──
    for i in range(n):
        color = colors[i]
        deg_start = i * angle_step - 90
        deg_end = (i + 1) * angle_step - 90
        rad_s = math.radians(deg_start)
        rad_e = math.radians(deg_end)
        x1 = cx + radius * math.cos(rad_s)
        y1 = cy + radius * math.sin(rad_s)
        x2 = cx + radius * math.cos(rad_e)
        y2 = cy + radius * math.sin(rad_e)
        large = 1 if angle_step > 180 else 0
        parts.append(
            f'    <path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {radius} {radius} 0 {large} 1 {x2:.1f} {y2:.1f} Z" '
            f'fill="{color}" fill-opacity="0.06"/>'
        )

    # ── Rotating sweep needle ──
    sweep_color = colors[0]
    sweep_deg_start = 345
    sweep_deg_end = 360
    rad_s = math.radians(sweep_deg_start - 90)
    rad_e = math.radians(sweep_deg_end - 90)
    x1 = cx + radius * math.cos(rad_s)
    y1 = cy + radius * math.sin(rad_s)
    x2 = cx + radius * math.cos(rad_e)
    y2 = cy + radius * math.sin(rad_e)
    parts.append(
        f'    <g>'
        f'      <path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {radius} {radius} 0 0 1 {x2:.1f} {y2:.1f} Z" '
        f'fill="{sweep_color}" fill-opacity="0.06"/>'
        f'      <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - radius:.0f}" '
        f'stroke="{sweep_color}" stroke-width="1.2" opacity="0.7"/>'
        f'      <circle cx="{cx}" cy="{cy - radius:.0f}" r="2.5" fill="{sweep_color}" opacity="0.8">'
        f'        <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" repeatCount="indefinite"/>'
        f'      </circle>'
        f'      <animateTransform attributeName="transform" type="rotate" '
        f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="10s" repeatCount="indefinite"/>'
        f'    </g>'
    )

    # ── Labels with icon + title + score ──
    label_r = radius + 18
    for i in range(n):
        deg = i * angle_step - 90
        rad = math.radians(deg)
        lx = cx + label_r * math.cos(rad)
        ly = cy + label_r * math.sin(rad)
        color = colors[i]
        name = layers[i]["name"]
        score = len(layers[i].get("items", []))

        # Text anchor: always centered on its position
        anchor = "middle"

        # Indicator dot
        parts.append(
            f'    <circle cx="{lx:.1f}" cy="{ly - 10:.1f}" r="3" fill="{color}" opacity="0.6">'
            f'      <animate attributeName="opacity" values="0.4;1;0.4" dur="2.5s" begin="{i * 0.5}s" repeatCount="indefinite"/>'
            f'    </circle>'
        )
        # Label name
        parts.append(
            f'    <text x="{lx:.1f}" y="{ly:.1f}" fill="{color}" font-size="9" font-family="monospace" '
            f'text-anchor="{anchor}" dominant-baseline="middle">{esc(name)}</text>'
        )
        # Score below
        parts.append(
            f'    <text x="{lx:.1f}" y="{ly + 13:.1f}" fill="{NEON["text_faint"]}" font-size="8" '
            f'font-family="monospace" text-anchor="{anchor}" dominant-baseline="middle">({score})</text>'
        )

    # ── Orbiting particles ──
    for p in range(6):
        angle = p * 60
        rad = math.radians(angle - 90)
        orbit_r = radius * 0.55
        px = cx + orbit_r * math.cos(rad)
        py = cy + orbit_r * math.sin(rad)
        parts.append(
            f'    <circle cx="{px:.1f}" cy="{py:.1f}" r="1.2" fill="{colors[p % n]}" opacity="0.5">'
            f'      <animate attributeName="opacity" values="0.2;0.8;0.2" dur="2s" begin="{p * 0.4}s" repeatCount="indefinite"/>'
            f'    </circle>'
        )

    return "\n".join(parts)


# ── HUD micro-details ─────────────────────────────────────────────

def _build_hud_elements(width, height):
    """Corner brackets, grid dots, fake coords, scan line."""
    parts = []

    # Corner brackets
    bl = 12
    brk = NEON["divider"]
    parts.append(
        f'  <g opacity="0.4">'
        f'    <polyline points="6,{bl + 6} 6,6 {bl + 6},6" fill="none" stroke="{brk}" stroke-width="1"/>'
        f'    <polyline points="{width - bl - 6},6 {width - 6},6 {width - 6},{bl + 6}" fill="none" stroke="{brk}" stroke-width="1"/>'
        f'    <polyline points="6,{height - bl - 6} 6,{height - 6} {bl + 6},{height - 6}" fill="none" stroke="{brk}" stroke-width="1"/>'
        f'    <polyline points="{width - bl - 6},{height - 6} {width - 6},{height - 6} {width - 6},{height - bl - 6}" fill="none" stroke="{brk}" stroke-width="1"/>'
        f'  </g>'
    )

    # Fake coordinate text
    parts.append(
        f'  <text x="{width - 20}" y="16" fill="{NEON["text_faint"]}" font-size="7" font-family="monospace" '
        f'text-anchor="end" opacity="0.3">SYS::DATA_LK_v2.4</text>'
    )

    # Scan line
    parts.append(
        f'  <rect x="6" y="6" width="{width - 12}" height="1" fill="{NEON["text_bright"]}" opacity="0.03">'
        f'<animateTransform attributeName="transform" type="translate" from="0 0" to="0 {height - 12}" '
        f'dur="8s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    return "\n".join(parts)


def _build_grid():
    """Faint background grid dots."""
    lines = []
    for x in range(40, WIDTH, 60):
        for y in range(40, 600, 40):
            lines.append(
                f'  <circle cx="{x}" cy="{y}" r="0.6" fill="{NEON["grid"]}" opacity="0.12"/>'
            )
    return "\n".join(lines)


# ── Main render ───────────────────────────────────────────────────

def render(languages: dict, data_layers: list, theme: dict, exclude: list, max_display: int) -> str:
    """Render the HUD Data Dashboard SVG."""

    n_layers = len(data_layers)
    layer_colors = [LAYER_NEON[i % len(LAYER_NEON)] for i in range(n_layers)]

    # ── Left: Stacked cubes ──
    cube_w = 320
    cube_h = 95
    cube_cx = 220
    start_y = 72
    gap = 24

    cubes = []
    connections = []

    for i, layer in enumerate(data_layers):
        color = layer_colors[i]
        cy = start_y + i * (cube_h + gap)

        cubes.append(
            _build_cube(i, cube_cx, cy, cube_w, cube_h,
                        color, layer["name"], layer.get("items", []))
        )

        # Connection to next
        if i < n_layers - 1:
            next_top = cy + cube_h
            next_bot = start_y + (i + 1) * (cube_h + gap)
            connections.append(
                _build_connection(cube_cx, next_top, next_bot, color, i)
            )

    cubes_str = "\n".join(cubes)
    connections_str = "\n".join(connections)

    # ── Right: Radar ──
    radar_cx = 645
    radar_cy = 265
    radar_radius = 105

    radar = _build_radar(radar_cx, radar_cy, radar_radius, data_layers, layer_colors)

    # ── Dynamic height ──
    left_h = start_y + n_layers * (cube_h + gap) - gap + 40
    radar_h = radar_cy + radar_radius + 60
    height = max(500, left_h, radar_h)

    # ── HUD elements ──
    hud = _build_hud_elements(WIDTH, height)
    grid = _build_grid()

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}">
  <defs>
    <filter id="shadow-blur" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <filter id="edge-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="text-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="radar-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" ry="12"
        fill="{NEON['bg']}" stroke="{NEON['divider']}" stroke-width="1"/>

  <!-- Background grid -->
{grid}

  <!-- HUD micro elements -->
{hud}

  <!-- Left title -->
  <text x="30" y="40" fill="{NEON['text_faint']}" font-size="10" font-family="monospace" letter-spacing="2.5">STACK LAYERS</text>

  <!-- Vertical divider -->
  <line x1="425" y1="24" x2="425" y2="{height - 24}" stroke="{NEON['divider']}" stroke-width="0.8" opacity="0.5"/>

  <!-- Right title -->
  <text x="460" y="40" fill="{NEON['text_faint']}" font-size="10" font-family="monospace" letter-spacing="2.5">CORE COMPETENCIES</text>

  <!-- Connections (behind cubes) -->
{connections_str}

  <!-- Cubes -->
{cubes_str}

  <!-- Radar -->
  <g filter="url(#radar-glow)">
{radar}
  </g>
</svg>'''
