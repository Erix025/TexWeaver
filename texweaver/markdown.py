from .tex_config import TexConfig
import json
class Document:
    def __init__(self):
        self.components = []
        
    def add_component(self, component):
        self.components.append(component)    
    
    def to_latex(self, config : TexConfig):
        return '\n'.join([c.to_latex() for c in self.components])
    
    def to_json(self):
        obj = {
            'type': 'document',
            'components': [c.to_json() for c in self.components]
        }
        json_str = json.dumps(obj, indent=4)
        return json_str
        

class Paragraph:
    def __init__(self):
        self.components = []
    
    def add_component(self, component):
        self.components.append(component)
        
    def to_latex(self):
        return ''.join([c.to_latex() for c in self.components])
    
    def to_json(self):
        return {
            'type': 'paragraph',
            'components': [c.to_json() for c in self.components]
        }
    
class Text:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return self.text
    
    def to_json(self):
        return {
            'type': 'text',
            'text': self.text
        }
    
class InlineBold:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return '\\textbf{%s}' % self.text
    
    def to_json(self):
        return {
            'type': 'inline_bold',
            'text': self.text
        }
    
class InlineItalic:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return '\\textit{%s}' % self.text
    
    def to_json(self):
        return {
            'type': 'inline_italic',
            'text': self.text
        }
    
class InlineCode:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return '\\texttt{%s}' % self.text
    
    def to_json(self):
        return {
            'type': 'inline_code',
            'text': self.text
        }
    
class InlineFormula:
    def __init__(self, text):
        self.text = text
        
    def to_latex(self, config : TexConfig):
        return '$%s$' % self.text
    
    def to_json(self):
        return {
            'type': 'inline_formula',
            'text': self.text
        }
    
class CodeBlock:
    def __init__(self, lang = None):
        self.lang = lang if lang else 'text'
        self.code = []
        
    def add_code(self, code):
        self.code.append(code)
        
    def to_latex(self, config : TexConfig):
        return '\\begin{lstlisting}[language=%s]\n%s\n\\end{lstlisting}' % (self.lang, '\n'.join(self.code))
    def to_json(self):
        return {
            'type': 'code_block',
            'code': self.code,
            'lang': self.lang
        }
    
class Image:
    def __init__(self, path, caption):
        self.path = path
        self.caption = caption
        
    def to_latex(self, config : TexConfig):
        return '\\begin{figure}\n\\centering\n\\includegraphics{%s}\n\\caption{%s}\n\\end{figure}' % (self.path, self.caption)
    
    def to_json(self):
        return {
            'type': 'image',
            'path': self.path,
            'caption': self.caption
        }
    
class Heading:
    def __init__(self, title, level):
        self.title = title
        self.level = level
        
    def to_latex(self, config : TexConfig):
        if self.level == 2:
            return '\\chapter{%s}\n' % self.title
        elif self.level == 3:
            return '\\section{%s}\n' % self.title
        elif self.level == 4:
            return '\\subsection{%s}\n' % self.title
        else:
            return '\\textbf{%s}\n' % self.title
        
    def to_json(self):
        return {
            'type': 'heading',
            'title': self.title,
            'level': self.level,
        }
    
class OrderedList:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def to_latex(self, config : TexConfig):
        return '\\begin{enumerate}\n%s\n\\end{enumerate}' % '\n'.join(['\\item %s' % i.to_latex() for i in self.items])
    
    def to_json(self):
        return {
            'type': 'ordered_list',
            'items': [i.to_json() for i in self.items]
        }
    
class UnorderedList:
    
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def to_latex(self, config : TexConfig):
        return '\\begin{itemize}\n%s\n\\end{itemize}' % '\n'.join(['\\item %s' % i.to_latex() for i in self.items])
    
    def to_json(self):
        return {
            'type': 'unordered_list',
            'items': [i.to_json() for i in self.items]
        }
    
class ListItem:
    def __init__(self):
        self.components = []
        
    def add_component(self, component):
        self.components.append(component)
        
    def to_latex(self, config : TexConfig):
        return ''.join([c.to_latex() for c in self.components])
    
    def to_json(self):
        return {
            'type': 'list_item',
            'components': [c.to_json() for c in self.components]
        }
