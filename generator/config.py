"""Config validation and defaults for the DataStack Profile generator."""

from generator.utils import resolve_theme, HEX_COLOR_RE


class ConfigError(ValueError):
    """Raised when config.yml has invalid or missing data."""


def validate_config(config: dict) -> dict:
    """Validate and apply defaults to a parsed config dict.

    Args:
        config: raw dict from yaml.safe_load()

    Returns:
        config dict with defaults applied for optional fields

    Raises:
        ConfigError: if required fields are missing or values are invalid
    """
    if not isinstance(config, dict):
        raise ConfigError("Config must be a YAML mapping (dict).")

    # username — required
    username = config.get("username")
    if not username or not isinstance(username, str) or not username.strip():
        raise ConfigError("'username' is required and must be a non-empty string.")

    # profile.name — required
    profile = config.get("profile", {})
    if not isinstance(profile, dict):
        raise ConfigError("'profile' must be a mapping.")
    if not profile.get("name"):
        raise ConfigError("'profile.name' is required.")

    # data_layers — required, must be a list
    data_layers = config.get("data_layers", [])
    if not isinstance(data_layers, list) or not data_layers:
        raise ConfigError("'data_layers' must be a non-empty list.")
    for i, layer in enumerate(data_layers):
        if not isinstance(layer, dict):
            raise ConfigError(f"data_layers[{i}] must be a mapping.")
        if not layer.get("name"):
            raise ConfigError(f"data_layers[{i}].name is required.")
        if not layer.get("color"):
            raise ConfigError(f"data_layers[{i}].color is required.")
        if not isinstance(layer.get("items", []), list):
            raise ConfigError(f"data_layers[{i}].items must be a list.")

    # projects — optional, validate entries if present
    projects = config.get("projects", [])
    if not isinstance(projects, list):
        raise ConfigError("'projects' must be a list.")
    for i, proj in enumerate(projects):
        if not isinstance(proj, dict):
            raise ConfigError(f"projects[{i}] must be a mapping.")
        if not proj.get("repo"):
            raise ConfigError(f"projects[{i}].repo is required.")
        layer_idx = proj.get("layer", 0)
        if not isinstance(layer_idx, int) or layer_idx < 0 or layer_idx >= len(data_layers):
            raise ConfigError(
                f"projects[{i}].layer must be an integer from 0 to {len(data_layers) - 1}."
            )

    # theme — optional, validate hex codes
    user_theme = config.get("theme", {})
    if not isinstance(user_theme, dict):
        raise ConfigError("'theme' must be a mapping.")
    for key, value in user_theme.items():
        if not isinstance(value, str) or not HEX_COLOR_RE.match(value):
            raise ConfigError(
                f"theme.{key} must be a valid hex color (e.g. #00c8a0), got '{value}'."
            )

    # Apply theme defaults
    config["theme"] = resolve_theme(user_theme)

    # experience — optional, validate entries if present
    experience = config.get("experience", [])
    if not isinstance(experience, list):
        raise ConfigError("'experience' must be a list.")
    for i, exp in enumerate(experience):
        if not isinstance(exp, dict):
            raise ConfigError(f"experience[{i}] must be a mapping.")
        if not exp.get("role"):
            raise ConfigError(f"experience[{i}].role is required.")
        if not exp.get("company"):
            raise ConfigError(f"experience[{i}].company is required.")
        if not isinstance(exp.get("bullets", []), list):
            raise ConfigError(f"experience[{i}].bullets must be a list.")

    # certifications — optional, validate entries if present
    certifications = config.get("certifications", [])
    if not isinstance(certifications, list):
        raise ConfigError("'certifications' must be a list.")
    for i, cert in enumerate(certifications):
        if not isinstance(cert, dict):
            raise ConfigError(f"certifications[{i}] must be a mapping.")
        if not cert.get("name"):
            raise ConfigError(f"certifications[{i}].name is required.")

    # Apply other defaults
    config["profile"].setdefault("tagline", "")
    config["profile"].setdefault("philosophy", "")
    config.setdefault("social", {})
    config.setdefault("projects", [])
    config.setdefault("experience", [])
    config.setdefault("certifications", [])
    config.setdefault("stats", {}).setdefault(
        "metrics", ["commits", "stars", "prs", "issues", "repos"]
    )
    lang_cfg = config.setdefault("languages", {})
    lang_cfg.setdefault("exclude", [])
    lang_cfg.setdefault("max_display", 8)

    return config
