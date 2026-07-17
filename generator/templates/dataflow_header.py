"""SVG template: DataFlow Header -- animated pipeline banner with 3D cube (850x300)."""

import math
from generator.utils import deterministic_random, esc

WIDTH, HEIGHT = 850, 355


def _build_cube(theme):
    """Build a 3D isometric Data Engineering cube with animations.

    Returns an SVG group containing:
    - Glow halo behind the cube (pulsing radial gradient)
    - 3 visible faces (top, left, right) with data elements
    - Continuous Y-axis rotation, vertical float, glow pulse
    """
    # Cube center in local coords
    CX, CY = 100, 105

    # -- Top face gradient: cyan to bright teal --
    # -- Left face gradient: blue to purple --
    # -- Right face gradient: teal to cyan --

    return f'''  <!-- Data Engineering Cube -->

  <!-- Glow halo behind cube -->
  <circle cx="{CX}" cy="{CY}" r="68" fill="url(#cube-glow)" opacity="0.12">
    <animate attributeName="opacity" values="0.08;0.22;0.08" dur="3.5s" repeatCount="indefinite"/>
    <animate attributeName="r" values="66;72;66" dur="3.5s" repeatCount="indefinite"/>
  </circle>

  <!-- Float + Rotate wrapper -->
  <g>
    <!-- Subtle vertical float -->
    <animateTransform attributeName="transform" type="translate"
      values="0,0; 0,-5; 0,0; 0,-5; 0,0" dur="4s" repeatCount="indefinite"/>

    <!-- Continuous Y-axis rotation -->
    <g>
      <animateTransform attributeName="transform" type="rotate"
        from="0 {CX} {CY}" to="360 {CX} {CY}" dur="10s" repeatCount="indefinite"/>

      <!-- Left face (blue-purple gradient) -->
      <polygon points="40,65 100,95 100,155 40,125"
        fill="url(#cube-left)" stroke="#60d0ff" stroke-width="1.2" stroke-linejoin="round" opacity="0.92"/>

      <!-- Left face: data layers (horizontal storage lines) -->
      <line x1="47" y1="82" x2="93" y2="105" stroke="#60d0ff" stroke-width="0.6" opacity="0.5"/>
      <line x1="44" y1="102" x2="90" y2="125" stroke="#60d0ff" stroke-width="0.6" opacity="0.5"/>
      <line x1="42" y1="122" x2="88" y2="145" stroke="#60d0ff" stroke-width="0.6" opacity="0.5"/>

      <!-- Left face: node dots on layers -->
      <circle cx="55" cy="86" r="1.5" fill="#a0f0ff" opacity="0.7">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" begin="0.3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="70" cy="112" r="1.5" fill="#a0f0ff" opacity="0.7">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" begin="1s" repeatCount="indefinite"/>
      </circle>
      <circle cx="60" cy="132" r="1.5" fill="#a0f0ff" opacity="0.7">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" begin="1.7s" repeatCount="indefinite"/>
      </circle>

      <!-- Right face (teal-cyan gradient) -->
      <polygon points="100,95 160,65 160,125 100,155"
        fill="url(#cube-right)" stroke="#60d0ff" stroke-width="1.2" stroke-linejoin="round" opacity="0.92"/>

      <!-- Right face: pipeline nodes with connections -->
      <line x1="115" y1="90" x2="140" y2="100" stroke="#60d0ff" stroke-width="0.6" opacity="0.5"/>
      <line x1="140" y1="100" x2="130" y2="115" stroke="#60d0ff" stroke-width="0.6" opacity="0.5"/>
      <line x1="130" y1="115" x2="150" y2="135" stroke="#60d0ff" stroke-width="0.6" opacity="0.5"/>

      <circle cx="115" cy="90" r="2" fill="#a0f0ff" opacity="0.8">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" begin="0s" repeatCount="indefinite"/>
      </circle>
      <circle cx="140" cy="100" r="2" fill="#a0f0ff" opacity="0.8">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" begin="0.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="130" cy="115" r="2" fill="#a0f0ff" opacity="0.8">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" begin="1s" repeatCount="indefinite"/>
      </circle>
      <circle cx="150" cy="135" r="2" fill="#a0f0ff" opacity="0.8">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" begin="1.5s" repeatCount="indefinite"/>
      </circle>

      <!-- Top face (cyan gradient, lightest) -->
      <polygon points="100,35 160,65 100,95 40,65"
        fill="url(#cube-top)" stroke="#60d0ff" stroke-width="1.2" stroke-linejoin="round" opacity="0.95"/>

      <!-- Top face: data grid (2x2 dotted pattern) -->
      <line x1="70" y1="50" x2="130" y2="80" stroke="#a0f0ff" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.4"/>
      <line x1="60" y1="65" x2="130" y2="50" stroke="#a0f0ff" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.4"/>

      <!-- Top face: central data node -->
      <circle cx="100" cy="65" r="3" fill="#ffffff" opacity="0.6">
        <animate attributeName="opacity" values="0.3;0.9;0.3" dur="2.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="100" cy="65" r="6" fill="none" stroke="#a0f0ff" stroke-width="0.5" opacity="0.3">
        <animate attributeName="opacity" values="0.1;0.4;0.1" dur="2.5s" repeatCount="indefinite"/>
        <animate attributeName="r" values="5;8;5" dur="2.5s" repeatCount="indefinite"/>
      </circle>

    </g>
  </g>'''


def _build_particles(username, theme):
    """Build small square particles flowing through horizontal pipes."""
    particles = []
    pipe_y_positions = [55, 100, 145]
    pipe_colors = [
        theme.get("pipeline_teal", "#00c8a0"),
        theme.get("spark_orange", "#ff6b35"),
        theme.get("lake_green", "#2ecc71"),
    ]

    for pipe_idx, py in enumerate(pipe_y_positions):
        color = pipe_colors[pipe_idx % len(pipe_colors)]
        for i in range(5):
            delay = i * 1.2 + pipe_idx * 0.4
            duration = 6 + pipe_idx
            particles.append(
                f'    <rect x="0" y="{py - 2}" width="4" height="4" rx="1" fill="{color}" opacity="0.7">\n'
                f'      <animateTransform attributeName="transform" type="translate" '
                f'from="-10 0" to="{WIDTH + 10} 0" dur="{duration}s" begin="{delay}s" repeatCount="indefinite"/>\n'
                f'      <animate attributeName="opacity" values="0;0.8;0.8;0" keyTimes="0;0.1;0.9;1" '
                f'dur="{duration}s" begin="{delay}s" repeatCount="indefinite"/>\n'
                f'    </rect>'
            )
    return "\n".join(particles)


def _build_pipes(theme):
    """Build horizontal pipeline tubes with gradients."""
    pipe_y_positions = [55, 100, 145]
    colors = [
        theme.get("pipeline_teal", "#00c8a0"),
        theme.get("spark_orange", "#ff6b35"),
        theme.get("lake_green", "#2ecc71"),
    ]
    pipes = []
    for idx, py in enumerate(pipe_y_positions):
        color = colors[idx % len(colors)]
        pipes.append(
            f'    <rect x="20" y="{py - 6}" width="{WIDTH - 40}" height="12" rx="6" '
            f'fill="none" stroke="{color}" stroke-width="1" opacity="0.25"/>'
        )
        pipes.append(
            f'    <line x1="20" y1="{py}" x2="{WIDTH - 20}" y2="{py}" '
            f'stroke="{color}" stroke-width="0.5" stroke-dasharray="4,8" opacity="0.15"/>'
        )
    return "\n".join(pipes)


def _build_grid_background(theme):
    """Build faint technical grid lines."""
    lines = []
    for x in range(40, WIDTH, 60):
        lines.append(
            f'    <line x1="{x}" y1="10" x2="{x}" y2="{HEIGHT - 10}" '
            f'stroke="{theme["grid"]}" stroke-width="0.5" stroke-dasharray="2,6" opacity="0.08"/>'
        )
    for y in range(40, HEIGHT, 40):
        lines.append(
            f'    <line x1="10" y1="{y}" x2="{WIDTH - 10}" y2="{y}" '
            f'stroke="{theme["grid"]}" stroke-width="0.5" stroke-dasharray="2,6" opacity="0.08"/>'
        )
    return "\n".join(lines)


def _build_starfield(username, theme):
    """Build background data dust particles."""
    stars = []
    sx = deterministic_random(f"{username}_header_sx", 30, 10, WIDTH - 10)
    sy = deterministic_random(f"{username}_header_sy", 30, 10, HEIGHT - 10)
    sr = deterministic_random(f"{username}_header_sr", 30, 0.5, 1.5)
    so = deterministic_random(f"{username}_header_so", 30, 0.05, 0.25)
    sd = deterministic_random(f"{username}_header_sd", 30, 3.0, 7.0)

    accent_colors = {
        0: theme.get("pipeline_teal", "#00c8a0"),
        5: theme.get("spark_orange", "#ff6b35"),
        10: theme.get("lake_green", "#2ecc71"),
    }

    for i in range(30):
        fill = accent_colors.get(i % 15, theme.get("text_faint", "#4a6582"))
        stars.append(
            f'    <circle cx="{sx[i]:.1f}" cy="{sy[i]:.1f}" r="{sr[i]:.2f}" '
            f'fill="{fill}" opacity="{so[i]:.2f}">\n'
            f'      <animate attributeName="opacity" values="{so[i]:.2f};{min(so[i]*3,0.7):.2f};{so[i]:.2f}" '
            f'dur="{sd[i]:.1f}s" repeatCount="indefinite"/>\n'
            f'    </circle>'
        )
    return "\n".join(stars)


def _build_name_tagline(name, tagline, theme):
    """Build centered name and tagline with terminal cursor effect."""
    name_text = (
        f'    <text x="{WIDTH / 2}" y="175" text-anchor="middle" '
        f'fill="{theme["text_bright"]}" font-size="24" font-weight="bold" '
        f'font-family="monospace">{esc(name)}'
        f'<animate attributeName="opacity" values="1;1;0;1" keyTimes="0;0.7;0.75;1" '
        f'dur="1.5s" repeatCount="indefinite"/></text>'
    )

    tagline_text = (
        f'    <text x="{WIDTH / 2}" y="198" text-anchor="middle" '
        f'fill="{theme["text_dim"]}" font-size="14" '
        f'font-family="monospace">{esc(tagline)}</text>'
    )

    cursor = (
        f'    <rect x="{WIDTH / 2 + len(tagline) * 4.5}" y="186" width="8" height="14" '
        f'fill="{theme["pipeline_teal"]}" opacity="0">\n'
        f'      <animate attributeName="opacity" values="0;1;0" dur="1s" repeatCount="indefinite"/>\n'
        f'    </rect>'
    )

    return f"{name_text}\n{tagline_text}\n{cursor}"


def _build_sub_tagline(sub_tagline, theme):
    """Build a secondary tagline below the main one."""
    return (
        f'    <text x="{WIDTH / 2}" y="222" text-anchor="middle" '
        f'fill="{theme["text_faint"]}" font-size="11" '
        f'font-family="monospace" font-style="italic">{esc(sub_tagline)}</text>'
    )


def _build_bio(bio_text, theme):
    """Build bio paragraph below the sub-tagline, wrapped to 2 lines if needed."""
    if not bio_text:
        return ""
    max_line = 95
    words = bio_text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}" if current else word
        if len(test) > max_line:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)

    parts = []
    for i, line in enumerate(lines[:3]):
        parts.append(
            f'    <text x="{WIDTH / 2}" y="{245 + i * 14}" text-anchor="middle" '
            f'fill="{theme["text_faint"]}" font-size="10" font-family="sans-serif" opacity="0.6">{esc(line)}</text>'
        )
    return "\n".join(parts)


def render(config: dict, theme: dict, data_layers: list, projects: list) -> str:
    """Render the dataflow header SVG with 3D Data Engineering cube."""
    username = config.get("username", "user")
    profile = config.get("profile", {})
    name = profile.get("name", username)
    tagline = profile.get("tagline", "")
    philosophy = profile.get("philosophy", "")
    bio = profile.get("bio", "")

    cube = _build_cube(theme)
    particles = _build_particles(username, theme)
    pipes = _build_pipes(theme)
    grid = _build_grid_background(theme)
    stars = _build_starfield(username, theme)
    name_tagline = _build_name_tagline(name, tagline, theme)
    sub_tagline = _build_sub_tagline(philosophy, theme)
    bio_text = _build_bio(bio, theme)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <!-- Pipe glow gradient -->
    <linearGradient id="pipe-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{theme['pipeline_teal']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{theme['pipeline_teal']}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{theme['pipeline_teal']}" stop-opacity="0"/>
    </linearGradient>

    <!-- Cube glow radial gradient -->
    <radialGradient id="cube-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{theme['pipeline_teal']}" stop-opacity="0.5"/>
      <stop offset="40%" stop-color="#6b4fa0" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="{theme['pipeline_teal']}" stop-opacity="0"/>
    </radialGradient>

    <!-- Cube top face gradient (cyan, lightest) -->
    <linearGradient id="cube-top" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#00a8cc" stop-opacity="0.18"/>
    </linearGradient>

    <!-- Cube left face gradient (blue to purple) -->
    <linearGradient id="cube-left" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a1a6e" stop-opacity="0.55"/>
      <stop offset="50%" stop-color="#3b3b8c" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#6b4fa0" stop-opacity="0.35"/>
    </linearGradient>

    <!-- Cube right face gradient (teal to cyan) -->
    <linearGradient id="cube-right" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#006ca0" stop-opacity="0.45"/>
      <stop offset="50%" stop-color="#0088cc" stop-opacity="0.40"/>
      <stop offset="100%" stop-color="#00a0d0" stop-opacity="0.30"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" rx="12" ry="12" fill="{theme['depth']}"/>

  <!-- Grid -->
{grid}

  <!-- Pipes -->
{pipes}

  <!-- Background particles -->
{stars}

  <!-- Flowing data particles -->
{particles}

  <!-- Data Engineering Cube (center, above name) -->
  <g transform="translate(325, 12) scale(1.05)">
{cube}
  </g>

  <!-- Name & tagline -->
{name_tagline}

  <!-- Sub-tagline -->
{sub_tagline}

  <!-- Bio -->
{bio_text}
</svg>'''

