"""SVG Builder — orchestrator connecting config, stats, and templates."""

from generator.templates import (
    dataflow_header,
    stats_card,
    tech_stack,
    projects_pipeline,
    experience_timeline,
    certifications_grid,
)


class SVGBuilder:
    """Builds all SVG assets from config and GitHub data.

    Expects a config dict that has already been through validate_config(),
    which resolves theme defaults and applies missing optional fields.
    """

    def __init__(self, config: dict, stats: dict, languages: dict):
        self.config = config
        self.stats = stats
        self.languages = languages
        self.theme = config["theme"]
        self.data_layers = config.get("data_layers", [])
        self.projects = config.get("projects", [])

    def render_dataflow_header(self) -> str:
        return dataflow_header.render(
            config=self.config,
            theme=self.theme,
            data_layers=self.data_layers,
            projects=self.projects,
        )

    def render_stats_card(self) -> str:
        metrics = self.config["stats"]["metrics"]
        return stats_card.render(
            stats=self.stats,
            metrics=metrics,
            theme=self.theme,
        )

    def render_tech_stack(self) -> str:
        lang_config = self.config.get("languages", {})
        return tech_stack.render(
            languages=self.languages,
            data_layers=self.data_layers,
            theme=self.theme,
            exclude=lang_config.get("exclude", []),
            max_display=lang_config.get("max_display", 8),
        )

    def render_projects_pipeline(self) -> str:
        return projects_pipeline.render(
            projects=self.projects,
            data_layers=self.data_layers,
            theme=self.theme,
        )

    def render_experience_timeline(self) -> str:
        return experience_timeline.render(
            experiences=self.config.get("experience", []),
            theme=self.theme,
        )

    def render_certifications_grid(self) -> str:
        return certifications_grid.render(
            certifications=self.config.get("certifications", []),
            theme=self.theme,
        )
