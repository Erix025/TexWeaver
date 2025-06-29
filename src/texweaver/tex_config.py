import importlib.resources as pkg_resources
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml


class TexConfig:
    """LaTeX template configuration manager."""

    def __init__(
        self, template_name: str = "default", config_file: Optional[str] = None
    ):
        """
        Initialize the TeX configuration.

        Args:
            template_name: Name of the built-in template to use
            config_file: Path to custom configuration file
        """
        self.config: Dict[str, Any] = {}
        self.template_name = template_name

        if config_file is not None:
            self.load_from_file(config_file)
        else:
            self.load_template(template_name)

    def load_from_file(self, config_file: str) -> None:
        """Load configuration from a file."""
        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def load_template(self, template_name: str) -> None:
        """Load a built-in template."""
        try:
            # Use the new traversable API for accessing subdirectories
            templates_path = pkg_resources.files("texweaver") / "templates"
            template_file = templates_path / f"{template_name}.yaml"

            if template_file.exists():
                with template_file.open(encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
            else:
                # Fallback to default template
                default_file = templates_path / "default.yaml"
                with default_file.open(encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)

        except Exception as e:
            # Ultimate fallback - create a minimal config
            print(f"Warning: Could not load template '{template_name}': {e}")
            self.config = self._create_minimal_config()

    def _create_minimal_config(self) -> Dict[str, Any]:
        """Create a minimal fallback configuration."""
        return {
            "name": "Minimal Fallback",
            "description": "Fallback configuration",
            "formatting": {
                "text": "{content}",
                "bold": "\\textbf{{{content}}}",
                "italic": "\\textit{{{content}}}",
                "paragraph": "{content}\n",
                "heading1": "\\section{{{content}}}\n",
                "heading2": "\\subsection{{{content}}}\n",
                "heading3": "\\subsubsection{{{content}}}\n",
            },
            "math": {
                "inline_formula": "${content}$",
                "block_formula": "\\begin{{equation}}\n{content}\n\\end{{equation}}\n",
            },
            "lists": {
                "ordered_list": "\\begin{{enumerate}}\n{items}\n\\end{{enumerate}}\n",
                "unordered_list": "\\begin{{itemize}}\n{items}\n\\end{{itemize}}\n",
                "list_item": "  \\item {content}",
            },
            "code": {
                "inline_code": "\\texttt{{{content}}}",
                "code_block": "\\begin{{verbatim}}\n{code}\n\\end{{verbatim}}\n",
            },
            "media": {"image": "\\includegraphics{{{src}}}"},
        }

    @classmethod
    def list_available_templates(cls) -> List[str]:
        """List all available built-in templates."""
        templates = []
        try:
            templates_path = pkg_resources.files("texweaver") / "templates"
            if templates_path.exists():
                for template_file in templates_path.iterdir():
                    if template_file.suffix == ".yaml":
                        templates.append(template_file.stem)
        except Exception:
            # Fallback list if directory reading fails
            templates = ["default", "academic", "book", "presentation"]
        return sorted(templates)

    def get_template_info(self) -> Dict[str, str]:
        """Get template metadata."""
        return {
            "name": self.config.get("name", "Unknown"),
            "description": self.config.get("description", "No description"),
            "author": self.config.get("author", "Unknown"),
            "version": self.config.get("version", "1.0"),
        }

    def apply(self, category: str, key: str, **kwargs) -> str:
        """
        Apply a template rule.

        Args:
            category: Template category (e.g., 'formatting', 'math', 'lists')
            key: Specific template key within the category
            **kwargs: Variables to substitute in the template

        Returns:
            Formatted LaTeX string
        """
        # Try category.key first
        if category in self.config and key in self.config[category]:
            template = self.config[category][key]
            return template.format(**kwargs)

        # Try direct key lookup for backward compatibility
        if key in self.config:
            template = self.config[key]
            return template.format(**kwargs)

        # Fallback
        if "content" in kwargs:
            return kwargs["content"]
        else:
            return ""

    def apply_simple(self, key: str, **kwargs) -> str:
        """
        Apply a template rule using simple key lookup (backward compatibility).

        Args:
            key: Template key
            **kwargs: Variables to substitute in the template

        Returns:
            Formatted LaTeX string
        """
        # Search through all categories
        for category_name, category_content in self.config.items():
            if isinstance(category_content, dict) and key in category_content:
                template = category_content[key]
                return template.format(**kwargs)

        # Direct lookup
        if key in self.config:
            template = self.config[key]
            return template.format(**kwargs)

        # Fallback
        if "content" in kwargs:
            return kwargs["content"]
        else:
            return ""


# Create default configuration instance (delayed initialization)
_default_config = None


def get_default_config():
    """Get the default configuration instance."""
    global _default_config
    if _default_config is None:
        _default_config = TexConfig("default")
    return _default_config


# For backward compatibility
DefaultConfig = get_default_config()
