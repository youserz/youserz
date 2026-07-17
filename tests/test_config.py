"""Tests for config validation."""

import pytest
from generator.config import validate_config, ConfigError


def test_valid_config():
    config = {
        "username": "testuser",
        "profile": {"name": "Test"},
        "data_layers": [
            {"name": "Layer1", "color": "pipeline_teal", "items": ["A"]},
        ],
    }
    result = validate_config(config)
    assert result["username"] == "testuser"
    assert result["profile"]["name"] == "Test"
    assert "theme" in result


def test_missing_username():
    config = {
        "profile": {"name": "Test"},
        "data_layers": [{"name": "L", "color": "c", "items": []}],
    }
    with pytest.raises(ConfigError, match="username"):
        validate_config(config)


def test_missing_data_layers():
    config = {
        "username": "testuser",
        "profile": {"name": "Test"},
    }
    with pytest.raises(ConfigError, match="data_layers"):
        validate_config(config)


def test_invalid_project_layer_index():
    config = {
        "username": "testuser",
        "profile": {"name": "Test"},
        "data_layers": [
            {"name": "Layer1", "color": "pipeline_teal", "items": []},
        ],
        "projects": [
            {"repo": "a/b", "layer": 5, "description": "x"},
        ],
    }
    with pytest.raises(ConfigError, match="layer"):
        validate_config(config)


def test_theme_hex_validation():
    config = {
        "username": "testuser",
        "profile": {"name": "Test"},
        "data_layers": [
            {"name": "Layer1", "color": "pipeline_teal", "items": []},
        ],
        "theme": {"depth": "not-a-color"},
    }
    with pytest.raises(ConfigError, match="hex color"):
        validate_config(config)


def test_invalid_experience():
    config = {
        "username": "testuser",
        "profile": {"name": "Test"},
        "data_layers": [
            {"name": "Layer1", "color": "pipeline_teal", "items": []},
        ],
        "experience": [
            {"company": "X", "bullets": []},
        ],
    }
    with pytest.raises(ConfigError, match=r"experience\[0\]\.role"):
        validate_config(config)


def test_invalid_certifications():
    config = {
        "username": "testuser",
        "profile": {"name": "Test"},
        "data_layers": [
            {"name": "Layer1", "color": "pipeline_teal", "items": []},
        ],
        "certifications": [
            {"year": "2025"},
        ],
    }
    with pytest.raises(ConfigError, match=r"certifications\[0\]\.name"):
        validate_config(config)
