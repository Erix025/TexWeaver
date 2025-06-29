import json

from .tex_config import TexConfig


def preprocess_text(text):
    # replace underscores with \_
    text = text.replace("_", r"\_")
    return text


class Document:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def to_latex(self, config: TexConfig):
        """Generate a complete LaTeX document."""
        # Get document structure from template
        preamble = config.apply("document", "preamble", content="")
        begin_document = config.apply("document", "begin_document", content="")
        end_document = config.apply("document", "end_document", content="")

        # If no document structure is defined, use fallback
        if not preamble:
            preamble = self._get_default_preamble()
        if not begin_document:
            begin_document = "\\begin{document}\n"
        if not end_document:
            end_document = "\\end{document}"

        # Check if this is a presentation template
        is_presentation = "beamer" in preamble.lower()

        if is_presentation:
            # For presentations, wrap content in frames
            content = self._generate_presentation_content(config)
        else:
            # Generate regular content
            content = "\n".join([c.to_latex(config) for c in self.components])

        # Combine everything
        return f"{preamble}\n{begin_document}\n{content}\n{end_document}"

    def _generate_presentation_content(self, config: TexConfig):
        """Generate content for Beamer presentations with proper frame structure."""
        if not self.components:
            return ""

        result = []
        current_frame_content = []
        frame_started = False

        for component in self.components:
            if isinstance(component, SlideBreak):
                # End current frame and start new one
                if frame_started:
                    result.append("\\end{frame}\n")

                # Check if next slide will have code blocks
                next_slide_components = self._get_next_slide_components(component)
                has_code = any(
                    isinstance(comp, CodeBlock) for comp in next_slide_components
                )

                if has_code:
                    result.append("\\begin{frame}[fragile]")
                else:
                    result.append("\\begin{frame}")
                frame_started = True
                current_frame_content = []
            else:
                if not frame_started:
                    # Start first frame, check if it has code blocks
                    first_slide_components = self._get_first_slide_components()
                    has_code = any(
                        isinstance(comp, CodeBlock) for comp in first_slide_components
                    )

                    if has_code:
                        result.append("\\begin{frame}[fragile]")
                    else:
                        result.append("\\begin{frame}")
                    frame_started = True
                result.append(component.to_latex(config))

        # Close the last frame if needed
        if frame_started:
            result.append("\\end{frame}")

        return "\n".join(result)

    def _get_next_slide_components(self, slide_break):
        """Get components for the next slide after a slide break."""
        try:
            slide_break_index = self.components.index(slide_break)
            next_components = []

            for i in range(slide_break_index + 1, len(self.components)):
                if isinstance(self.components[i], SlideBreak):
                    break
                next_components.append(self.components[i])

            return next_components
        except ValueError:
            return []

    def _get_first_slide_components(self):
        """Get components for the first slide."""
        first_slide_components = []

        for component in self.components:
            if isinstance(component, SlideBreak):
                break
            first_slide_components.append(component)

        return first_slide_components

    def _get_default_preamble(self):
        """Fallback LaTeX preamble if template doesn't provide one."""
        return """\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage{float}
\\usepackage{listings}
\\usepackage{xcolor}"""

    def to_json(self):
        obj = {"type": "document", "components": [c.to_json() for c in self.components]}
        json_str = json.dumps(obj, indent=4)
        return json_str


class Content:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def to_latex(self, config: TexConfig):
        return "".join([c.to_latex(config) for c in self.components])

    def to_json(self):
        return {"type": "content", "components": [c.to_json() for c in self.components]}


class Text:
    def __init__(self, text: str):
        self.text = preprocess_text(text)

    def to_latex(self, config: TexConfig):
        return config.apply_simple("text", content=self.text)

    def to_json(self):
        return {"type": "text", "text": self.text}


class InlineBold:
    def __init__(self, text: str):
        self.text = preprocess_text(text)

    def to_latex(self, config: TexConfig):
        return config.apply_simple("bold", content=self.text)

    def to_json(self):
        return {"type": "inline_bold", "text": self.text}


class InlineItalic:
    def __init__(self, text: str):
        self.text = preprocess_text(text)

    def to_latex(self, config: TexConfig):
        return config.apply_simple("italic", content=self.text)

    def to_json(self):
        return {"type": "inline_italic", "text": self.text}


class InlineCode:
    def __init__(self, text: str):
        self.text = preprocess_text(text)

    def to_latex(self, config: TexConfig):
        return config.apply_simple("inline_code", content=self.text)

    def to_json(self):
        return {"type": "inline_code", "text": self.text}


class InlineFormula:
    def __init__(self, text: str):
        self.text = text

    def to_latex(self, config: TexConfig):
        return config.apply_simple("inline_formula", content=self.text)

    def to_json(self):
        return {"type": "inline_formula", "text": self.text}


class Paragraph:
    def __init__(self, content: Content):
        self.content = content

    def to_latex(self, config: TexConfig):
        return config.apply_simple("paragraph", content=self.content.to_latex(config))

    def to_json(self):
        return {"type": "paragraph", "content": self.content.to_json()}


class FormulaBlock:
    def __init__(self, text):
        self.text = text

    def to_latex(self, config: TexConfig):
        return config.apply_simple("block_formula", content=self.text)

    def to_json(self):
        return {"type": "formula_block", "text": self.text}


class CodeBlock:
    def __init__(self, lang=None):
        self.lang = lang if lang else "text"
        self.code = []

    def add_code(self, code):
        self.code.append(code)

    def to_latex(self, config: TexConfig):
        return config.apply_simple(
            "code_block", code="\n".join(self.code), lang=self.lang
        )

    def to_json(self):
        return {"type": "code_block", "code": self.code, "lang": self.lang}


class Image:
    def __init__(self, path: str, caption: Content):
        self.path = path
        self.caption = caption

    def to_latex(self, config: TexConfig):
        # Generate a simple label from the caption text
        caption_text = self.caption.to_latex(config)
        label = (
            caption_text.replace(" ", "_")
            .replace("\\", "")
            .replace("{", "")
            .replace("}", "")
            .lower()[:20]
        )
        if not label:
            label = "image"
        return config.apply_simple(
            "image", src=self.path, alt=caption_text, width="0.8", label=label
        )

    def to_json(self):
        return {"type": "image", "path": self.path, "caption": self.caption.to_json()}


class Heading:
    def __init__(self, title: Content, level):
        self.title = title
        self.level = level

    def to_latex(self, config: TexConfig):
        content = self.title.to_latex(config)
        if self.level == 1:
            return config.apply_simple("heading1", content=content)
        elif self.level == 2:
            return config.apply_simple("heading2", content=content)
        elif self.level == 3:
            return config.apply_simple("heading3", content=content)
        elif self.level == 4:
            return config.apply_simple("heading4", content=content)
        elif self.level == 5:
            return config.apply_simple("heading5", content=content)
        else:
            return config.apply_simple("bold", content=content)

    def to_json(self):
        return {
            "type": "heading",
            "title": self.title.to_json(),
            "level": self.level,
        }


class OrderedList:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def to_latex(self, config: TexConfig):
        return config.apply_simple(
            "ordered_list", items="\n".join([i.to_latex(config) for i in self.items])
        )

    def to_json(self):
        return {"type": "ordered_list", "items": [i.to_json() for i in self.items]}


class UnorderedList:

    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def to_latex(self, config: TexConfig):
        return config.apply_simple(
            "unordered_list", items="\n".join([i.to_latex(config) for i in self.items])
        )

    def to_json(self):
        return {"type": "unordered_list", "items": [i.to_json() for i in self.items]}


class ListItem:
    def __init__(self):
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def to_latex(self, config: TexConfig):
        return config.apply_simple(
            "list_item", content="".join([c.to_latex(config) for c in self.components])
        )

    def to_json(self):
        return {
            "type": "list_item",
            "components": [c.to_json() for c in self.components],
        }


class SlideBreak:
    """Represents a slide break for presentations (---)"""

    def __init__(self):
        pass

    def to_latex(self, config: TexConfig):
        return config.apply_simple("slide_break", content="")

    def to_json(self):
        return {"type": "slide_break"}
