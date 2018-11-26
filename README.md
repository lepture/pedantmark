# Pedantic Markdown

<a href="https://lepture.com/donate"><img src="https://img.shields.io/badge/donate-lepture-ff69b4.svg?maxAge=2592000" /></a>
<a href="https://pypi.org/project/pedantmark/"><img src="https://img.shields.io/pypi/wheel/pedantmark.svg?maxAge=2592000" /></a>

**pedantmark** is (not only) a python binding for the GitHub's fork of CommonMark (cmark).
It has also been enhanced to support custom renderers.

> Only two maybes I've thought of: Strict Markdown or Pedantic Markdown. "Strict" still doesn't seem right.
>
> -- [John Gruber](https://twitter.com/gruber/status/507615356295200770)

Ok, let's call it **pedantmark**.


## Install

**pedantmark** is available in Python 2.7 and 3.5+ for Linux and Mac,
Python 3.5+ for Windows. Wheels are built by [multibuild][].

Install wheels by pip:

    $ pip install pedantmark

[multibuild]: https://github.com/matthew-brett/multibuild


## Standard Usage

The C source code has serval built-in renderers. The simplest interface is
`pedantmark.html(text, options)`, which will render text into HTML.

```python
import pedantmark

text = '...'
html = pedantmark.html(text, options=[pedantmark.OPT_VALIDATE_UTF8])
```

The function `pedantmark.html()` accepts no extensions, but you can add
extensions via `pedantmark.markdown()`:

```python
import pedantmark

text = '...'
html = pedantmark.markdown(
    text,
    options=[pedantmark.OPT_VALIDATE_UTF8],
    extensions=['strikethrough', 'autolink', 'table'],
    renderer='html',
)
```

Available extensions: `table`, `autolink`, `tagfilter`, `strikethrough`.
You can enable them all with a shortcut:

    pedantmark.markdown(..., extensions=pedantmark.EXTENSIONS)

Available renderers: `html`, `xml`, `man`, `commonmark`, `plaintext`,
and `latex`.

## Options

Here is a full list of options:

```
#: Include a `data-sourcepos` attribute on all block elements.
OPT_SOURCEPOS

#: Render `softbreak` elements as hard line breaks.
OPT_HARDBREAKS

#: Render `softbreak` elements as spaces.
OPT_NOBREAKS

#: Validate UTF-8 in the input before parsing, replacing illegal
#: sequences with the replacement character U+FFFD.
OPT_VALIDATE_UTF8

#: Convert straight quotes to curly, --- to em dashes, -- to en dashes.
OPT_SMART

#: Use GitHub-style <pre lang="x"> tags for code blocks instead of
#: <pre><code class="language-x">.
OPT_PRE_LANG

#: Be liberal in interpreting inline HTML tags.
OPT_LIBERAL_HTML_TAG

#: Parse footnotes.
OPT_FOOTNOTES

#: Only parse strikethroughs if surrounded by exactly 2 tildes.
OPT_STRIKETHROUGH_DOUBLE_TILDE

#: Use style attributes to align table cells instead of align attributes.
OPT_TABLE_PREFER_STYLE_ATTRIBUTES

#: Include the remainder of the info string in code blocks in
#: a separate attribute.
OPT_FULL_INFO_STRING

#: Allow raw HTML and unsafe links, `javascript:`, `vbscript:`, `file:`,
#: and all `data:` URLs -- by default, only `image/png`, `image/gif`,
#: `image/jpeg`, or `image/webp` mime types are allowed. Without this
#: option, raw HTML is replaced by a placeholder HTML comment, and unsafe
#: links are replaced by empty strings.
OPT_UNSAFE
```

## Custom Renderer

Besides the native renderers, **pedantmark** has provided you a custom renderer,
which you can customize the output yourself. Here is an example of pygments code
highlighting integration:

```python
from pedantmark import HTMLRenderer, markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class MyRenderer(HTMLRenderer):
    def code_block(self, code, lang):
        if lang:
            # everything is in bytes
            lang = lang.decode('utf-8')
            code = code.decode('utf-8')
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            output = highlight(code, lexer, formatter)
            # return bytes
            return output.encode('utf-8')
        return super(MyRenderer, self).code_block(code, lang)

text = '...'
markdown(text, renderer=MyRenderer())
```

The default `HTMLRenderer` has a built-in hook for code highlight, you don't need
to subclass at all:

```python
def add_code_highlight(code, lang):
    lang = lang.decode('utf-8')
    code = code.decode('utf-8')
    lexer = get_lexer_by_name(lang, stripall=True)
    formatter = html.HtmlFormatter()
    output = highlight(code, lexer, formatter)
    return output.encode('utf-8')

text = '...'
markdown(text, renderer=HTMLRenderer(highlight=add_code_highlight))
```

Here is a full list of renderers:

```
thematic_break(self)
html_block(self, text)
block_quote(self, text)
code_block(self, text, lang)
heading(self, text, level, index=None)
paragraph(self, text)
list_item(self, text)
list(self, text, ordered, start=None)
table_cell(self, text, tag, align=None)
table_row(self, text)
table_header(self, text)
table(self, text)
softbreak(self)
linebreak(self)
html_inline(self, text)
text(self, text)
emph(self, text)
strong(self, text)
strikethrough(self, text)
code(self, text)
link(self, url, text, title)
image(self, src, alt, title)
footnote_ref(self, key)
footnote_item(self, text, index):
footnotes(self, text)
```

## Author & License

This library is created by Hsiaming Yang, licensed under BSD.
