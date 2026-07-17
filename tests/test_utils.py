"""Tests for utility functions."""

from generator.utils import (
    resolve_theme,
    resolve_layer_colors,
    format_number,
    calculate_language_percentages,
    get_language_color,
    esc,
    HEX_COLOR_RE,
)


def test_resolve_theme_defaults():
    theme = resolve_theme({})
    assert theme["depth"] == "#0b1120"
    assert theme["pipeline_teal"] == "#00c8a0"


def test_resolve_theme_override():
    theme = resolve_theme({"depth": "#000000"})
    assert theme["depth"] == "#000000"
    assert theme["lake_surface"] == "#111d2e"


def test_resolve_layer_colors():
    layers = [
        {"name": "A", "color": "spark_orange"},
        {"name": "B", "color": "lake_green"},
    ]
    theme = resolve_theme({})
    colors = resolve_layer_colors(layers, theme)
    assert colors[0] == "#ff6b35"
    assert colors[1] == "#2ecc71"


def test_format_number():
    assert format_number(999) == "999"
    assert format_number(1500) == "1.5k"
    assert format_number(1_500_000) == "1.5M"


def test_calculate_language_percentages():
    langs = {"Python": 500, "JavaScript": 300, "HTML": 200}
    result = calculate_language_percentages(langs, exclude=["HTML"], max_display=2)
    assert len(result) == 2
    assert result[0]["name"] == "Python"
    assert result[0]["percentage"] == 62.5


def test_get_language_color():
    assert get_language_color("Python") == "#3572A5"
    assert get_language_color("UnknownLang") == "#8b949e"


def test_esc():
    assert esc("<script>") == "&lt;script&gt;"
    assert esc('"test"') == "&quot;test&quot;"


def test_hex_color_regex():
    assert HEX_COLOR_RE.match("#ff6b35")
    assert not HEX_COLOR_RE.match("ff6b35")
    assert not HEX_COLOR_RE.match("#fff")
