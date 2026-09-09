"""Tests for SVG generation."""

from generator.svg_builder import SVGBuilder
from generator.config import validate_config


DEMO_CONFIG = {
    "username": "demo",
    "profile": {
        "name": "Demo User",
        "tagline": "Test tagline",
        "philosophy": '"Test philosophy."',
    },
    "data_layers": [
        {"name": "Cloud", "color": "spark_orange", "items": ["AWS", "Azure"]},
        {"name": "Data", "color": "lake_green", "items": ["Spark", "Delta"]},
    ],
    "projects": [
        {"repo": "demo/proj1", "layer": 0, "description": "A test project"},
    ],
    "experience": [
        {"role": "Data Engineer", "company": "TestCo", "period": "2024 – Atual", "bullets": ["ETL pipelines", "Spark jobs"]},
    ],
    "certifications": [
        {"name": "AWS Cloud Practitioner", "year": "2025", "issuer": "AWS"},
    ],
    "stats": {"metrics": ["commits", "stars"]},
    "languages": {"exclude": [], "max_display": 5},
}

DEMO_STATS = {"commits": 100, "stars": 50, "prs": 10, "issues": 5, "repos": 8}
DEMO_LANGS = {"Python": 5000, "Shell": 1000}


def test_render_dataflow_header():
    config = validate_config(DEMO_CONFIG)
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_dataflow_header()
    assert svg.startswith("<svg")
    assert "Demo User" in svg
    assert "</svg>" in svg


def test_render_stats_card():
    config = validate_config(DEMO_CONFIG)
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_stats_card()
    assert svg.startswith("<svg")
    assert "DATA TELEMETRY" in svg
    assert "</svg>" in svg


def test_render_tech_stack():
    config = validate_config(DEMO_CONFIG)
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_tech_stack()
    assert svg.startswith("<svg")
    assert "STACK LAYERS" in svg
    assert "Cloud" in svg
    assert "</svg>" in svg


def test_render_projects_pipeline():
    config = validate_config(DEMO_CONFIG)
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_projects_pipeline()
    assert svg.startswith("<svg")
    assert "FEATURED SYSTEMS" in svg
    assert "</svg>" in svg


def test_render_projects_pipeline_empty():
    config = validate_config({
        "username": "demo",
        "profile": {"name": "Demo"},
        "data_layers": [
            {"name": "A", "color": "pipeline_teal", "items": []},
        ],
    })
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_projects_pipeline()
    assert "No featured projects configured" in svg


def test_render_experience_timeline():
    config = validate_config(DEMO_CONFIG)
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_experience_timeline()
    assert svg.startswith("<svg")
    assert "PROFESSIONAL EXPERIENCE" in svg
    assert "Data Engineer" in svg
    assert "</svg>" in svg


def test_render_experience_timeline_empty():
    config = validate_config({
        "username": "demo",
        "profile": {"name": "Demo"},
        "data_layers": [
            {"name": "A", "color": "pipeline_teal", "items": []},
        ],
    })
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_experience_timeline()
    assert "No experience configured" in svg


def test_render_certifications_grid():
    config = validate_config(DEMO_CONFIG)
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_certifications_grid()
    assert svg.startswith("<svg")
    assert "CERTIFICATIONS" in svg
    assert "AWS Cloud Practitioner" in svg
    assert "</svg>" in svg


def test_render_certifications_grid_empty():
    config = validate_config({
        "username": "demo",
        "profile": {"name": "Demo"},
        "data_layers": [
            {"name": "A", "color": "pipeline_teal", "items": []},
        ],
    })
    builder = SVGBuilder(config, DEMO_STATS, DEMO_LANGS)
    svg = builder.render_certifications_grid()
    assert "No certifications configured" in svg
