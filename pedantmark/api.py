from ._cmark import lib, ffi
from .consts import get_options, attach_extensions


def markdown(text, options=None, extensions=None, renderer='html', width=0):
    if options is None:
        options = []
    if extensions is None:
        extensions = []

    _options = get_options(*options)
    parser = lib.cmark_parser_new(_options)
    try:
        _extensions = attach_extensions(parser, *extensions)

        bytes_text = text.encode('utf-8')
        lib.cmark_parser_feed(parser, bytes_text, len(bytes_text))
        root = lib.cmark_parser_finish(parser)

        output = _render_root(renderer, root, _options, _extensions, width)
    finally:
        lib.cmark_parser_free(parser)
    return output


def html(text, options=None):
    if options is None:
        options = []

    _options = get_options(*options)
    bytes_text = text.encode('utf-8')
    rv = lib.cmark_markdown_to_html(bytes_text, len(bytes_text), _options)
    return ffi.string(rv).decode('utf-8')


def _render_root(renderer, root, options, extensions, width):
    if renderer == 'html':
        output = lib.cmark_render_html(root, options, extensions)
    elif renderer == 'xml':
        output = lib.cmark_render_xml(root, options)
    elif renderer == 'man':
        output = lib.cmark_render_man(root, options, width)
    elif renderer == 'commonmark':
        output = lib.cmark_render_commonmark(root, options, width)
    elif renderer == 'plaintext':
        output = lib.cmark_render_plaintext(root, options, width)
    elif renderer == 'latex':
        output = lib.cmark_render_latex(root, options, width)
    else:
        raise ValueError('Invalid "renderer" value')

    return ffi.string(output).decode('utf-8')
