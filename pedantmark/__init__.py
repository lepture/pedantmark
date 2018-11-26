from .api import (
    markdown, html, EXTENSIONS,
    OPT_SOURCEPOS,
    OPT_HARDBREAKS,
    OPT_NOBREAKS,
    OPT_VALIDATE_UTF8,
    OPT_SMART,
    OPT_PRE_LANG,
    OPT_LIBERAL_HTML_TAG,
    OPT_FOOTNOTES,
    OPT_STRIKETHROUGH_DOUBLE_TILDE,
    OPT_TABLE_PREFER_STYLE_ATTRIBUTES,
    OPT_FULL_INFO_STRING,
    OPT_UNSAFE,
)
from .extern import (
    escape_html, escape_href,
    MarkdownState, HTMLRenderer,
)

__all__ = [
    'markdown', 'html', 'EXTENSIONS',
    'OPT_SOURCEPOS',
    'OPT_HARDBREAKS',
    'OPT_NOBREAKS',
    'OPT_VALIDATE_UTF8',
    'OPT_SMART',
    'OPT_PRE_LANG',
    'OPT_LIBERAL_HTML_TAG',
    'OPT_FOOTNOTES',
    'OPT_STRIKETHROUGH_DOUBLE_TILDE',
    'OPT_TABLE_PREFER_STYLE_ATTRIBUTES',
    'OPT_FULL_INFO_STRING',
    'OPT_UNSAFE',
    'escape_html', 'escape_href',
    'MarkdownState', 'HTMLRenderer',
]

__version__ = '0.1'
__author__ = 'Hsiaoming Yang <me@lepture.com>'
