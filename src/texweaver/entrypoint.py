import argparse

from . import TexParser
from .tex_config import TexConfig


def main():
    """Main entry point for the TexWeaver CLI."""
    parser = argparse.ArgumentParser(
        description="TexWeaver - Convert Markdown to LaTeX using customizable templates"
    )

    # Make input and output files optional when using list or info commands
    parser.add_argument("input_file", nargs="?", help="Path to input Markdown file")
    parser.add_argument("output_file", nargs="?", help="Path to output LaTeX file")

    parser.add_argument(
        "-t",
        "--template",
        default="default",
        help="Template to use (default: 'default'). Use --list-templates to see available options.",
    )

    parser.add_argument(
        "-c", "--config", help="Path to custom configuration file (overrides template)"
    )

    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List all available templates and exit",
    )

    parser.add_argument(
        "--template-info", help="Show information about a specific template"
    )

    args = parser.parse_args()

    # Handle list templates request
    if args.list_templates:
        list_templates()
        return

    # Handle template info request
    if args.template_info:
        show_template_info(args.template_info)
        return

    # Check required arguments for conversion
    if not args.input_file:
        parser.error("input_file is required for conversion")

    # Generate default output file name if not provided
    output_file = args.output_file
    if not output_file:
        if args.input_file.endswith(".md"):
            output_file = args.input_file[:-3] + ".tex"
        else:
            output_file = args.input_file + ".tex"

    # Process the input file and generate the output file
    process_file(args.input_file, output_file, args.template, args.config)


def list_templates():
    """List all available templates."""
    templates = TexConfig.list_available_templates()
    print("Available templates:")
    print("===================")

    for template_name in templates:
        try:
            config = TexConfig(template_name)
            info = config.get_template_info()
            print(f"  {template_name:15} - {info['description']}")
        except Exception:
            print(f"  {template_name:15} - (Error loading template)")

    print("\nUsage: texweaver -t <template_name> input.md output.tex")


def show_template_info(template_name):
    """Show detailed information about a specific template."""
    try:
        config = TexConfig(template_name)
        info = config.get_template_info()

        print(f"Template: {template_name}")
        print("=" * (len(template_name) + 10))
        print(f"Name:        {info['name']}")
        print(f"Description: {info['description']}")
        print(f"Author:      {info['author']}")
        print(f"Version:     {info['version']}")

    except Exception as e:
        print(f"Error loading template '{template_name}': {e}")
        print("Use --list-templates to see available templates.")


def process_file(input_file, output_file, template_name="default", config_file=None):
    """Process the input file and generate the output file."""
    try:
        # Create configuration
        if config_file:
            config = TexConfig(config_file=config_file)
        else:
            config = TexConfig(template_name)

        # Parse markdown
        parser = TexParser()
        with open(input_file, "r", encoding="utf-8") as f:
            src = f.read()
            parser.parse(src)

        # Generate LaTeX
        doc = parser.doc
        latex_content = doc.to_latex(config)

        # Write output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(latex_content)

        print(
            f"Successfully converted '{input_file}' to '{output_file}' using template '{template_name}'"
        )

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error processing file: {e}")


if __name__ == "__main__":
    main()
