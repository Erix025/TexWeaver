import re

from . import markdown as xwm
from .tex_config import DefaultConfig, TexConfig


class TexParser:
    def __init__(self):
        self.document = xwm.Document()
        self.in_code_block = False
        self.current_code_block = None
        self.current_list = None
        self.in_formula_block = False
        self.current_formula_content = []

    def parse(self, markdown_text):
        lines = markdown_text.splitlines()
        for line in lines:
            self._parse_line(line)

    def _preprocess_line(self, line):
        # remove leading and trailing whitespaces
        line = line.strip()
        # remove trailing comments
        line = re.sub(r"<!--.*-->", "", line)
        return line

    def _parse_line(self, line):

        # Block formula ($$...$$)
        if line.startswith("$$"):
            if self.in_formula_block:
                # close formula block
                formula_content = "\n".join(self.current_formula_content)
                self.document.add_component(xwm.FormulaBlock(formula_content))
                self.in_formula_block = False
                self.current_formula_content = []
            else:
                # open formula block
                self.in_formula_block = True
                # Check if there's content on the same line
                content_on_line = line[2:].strip()
                if content_on_line:
                    self.current_formula_content.append(content_on_line)
            return

        if self.in_formula_block:
            # append content to formula block
            self.current_formula_content.append(line)
            return

        # Codeblock
        if line.startswith("```"):
            if self.in_code_block:
                # close codeblock
                self.document.add_component(self.current_code_block)
                self.in_code_block = False
                self.current_code_block = None
            else:
                # open codeblock
                pattern = r"```(\w+)"
                match = re.match(pattern, line)
                if match:
                    language = match.group(1)
                    self.current_code_block = xwm.CodeBlock(lang=language)
                else:
                    self.current_code_block = xwm.CodeBlock()
                self.in_code_block = True
            return

        if self.in_code_block:
            # append code to codeblock
            self.current_code_block.add_code(line)
            return

        # remove leading and trailing whitespaces
        line = self._preprocess_line(line)

        # slide break (---)
        if line == "---":
            self.current_list = None
            self.document.add_component(xwm.SlideBreak())
            return

        # unordered list
        if re.match(r"^[-+*]\s", line):
            if self.current_list is None or not isinstance(
                self.current_list, xwm.UnorderedList
            ):
                # start new unordered list
                self.current_list = xwm.UnorderedList()
                self.document.add_component(self.current_list)
            self._parse_list_item(line, self.current_list)
            return

        # ordered list
        if re.match(r"^\d+\.\s", line):
            if self.current_list is None or not isinstance(
                self.current_list, xwm.OrderedList
            ):
                # start new ordered list
                self.current_list = xwm.OrderedList()
                self.document.add_component(self.current_list)
            self._parse_list_item(line, self.current_list)
            return

        self.current_list = None

        # heading
        pattern = r"^(#+)\s+(.*)"
        match = re.match(pattern, line)
        if match:
            level = len(match.group(1))
            title = self._parse_content(match.group(2))
            self.document.add_component(xwm.Heading(title=title, level=level))
            return

        # image
        pattern = r"!\[([^\]]+)\]\(([^)]+)\)"
        match = re.match(pattern, line)
        if match:
            caption = self._parse_content(match.group(1))
            path = match.group(2)
            self.document.add_component(xwm.Image(path=path, caption=caption))
            return

        # paragraph
        content = self._parse_content(line)
        if len(content.components) > 0:
            self.document.add_component(xwm.Paragraph(content))

    def _parse_content(self, line):
        # 正则表达式匹配内联代码和公式
        pattern = r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\$[^$]+\$|[^`$*]+)"
        matches = re.findall(pattern, line)

        content = xwm.Content()

        for match in matches:
            if match.startswith("`") and match.endswith("`"):
                # 内联代码
                content.add_component(xwm.InlineCode(match[1:-1]))
            elif match.startswith("$") and match.endswith("$"):
                # 数学公式
                content.add_component(xwm.InlineFormula(match[1:-1]))
            elif match.startswith("**") and match.endswith("**"):
                content.add_component(xwm.InlineBold(match[2:-2]))
            elif match.startswith("*") and match.endswith("*"):
                content.add_component(xwm.InlineItalic(match[1:-1]))
            else:
                # 普通文本
                content.add_component(xwm.Text(match))

        return content

    def _parse_list_item(self, line, list_obj):
        item = xwm.ListItem()
        content = re.sub(r"^[-+*]\s|\d+\.\s", "", line).strip()
        item.add_component(self._parse_content(content))
        list_obj.add_item(item)

    @property
    def doc(self):
        return self.document
