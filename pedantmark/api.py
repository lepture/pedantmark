from ._cmark import lib, ffi

#: Include a `data-sourcepos` attribute on all block elements.
OPT_SOURCEPOS = lib.CMARK_OPT_SOURCEPOS

#: Render `softbreak` elements as hard line breaks.
OPT_HARDBREAKS = lib.CMARK_OPT_HARDBREAKS

#: Render `softbreak` elements as spaces.
OPT_NOBREAKS = lib.CMARK_OPT_NOBREAKS

#: Validate UTF-8 in the input before parsing, replacing illegal
#: sequences with the replacement character U+FFFD.
OPT_VALIDATE_UTF8 = lib.CMARK_OPT_VALIDATE_UTF8

#: Convert straight quotes to curly, --- to em dashes, -- to en dashes.
OPT_SMART = lib.CMARK_OPT_SMART

#: Use GitHub-style <pre lang="x"> tags for code blocks instead of
#: <pre><code class="language-x">.
OPT_PRE_LANG = lib.CMARK_OPT_GITHUB_PRE_LANG

#: Be liberal in interpreting inline HTML tags.
OPT_LIBERAL_HTML_TAG = lib.CMARK_OPT_LIBERAL_HTML_TAG

#: Parse footnotes.
OPT_FOOTNOTES = lib.CMARK_OPT_FOOTNOTES

#: Only parse strikethroughs if surrounded by exactly 2 tildes.
OPT_STRIKETHROUGH_DOUBLE_TILDE = lib.CMARK_OPT_STRIKETHROUGH_DOUBLE_TILDE

#: Use style attributes to align table cells instead of align attributes.
OPT_TABLE_PREFER_STYLE_ATTRIBUTES = lib.CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES
#: Include the remainder of the info string in code blocks in
#: a separate attribute.

OPT_FULL_INFO_STRING = lib.CMARK_OPT_FULL_INFO_STRING

#: Allow raw HTML and unsafe links, `javascript:`, `vbscript:`, `file:`,
#: and all `data:` URLs -- by default, only `image/png`, `image/gif`,
#: `image/jpeg`, or `image/webp` mime types are allowed. Without this
#: option, raw HTML is replaced by a placeholder HTML comment, and unsafe
#: links are replaced by empty strings.
OPT_UNSAFE = lib.CMARK_OPT_UNSAFE

#: Available extensions
EXTENSIONS = ('table', 'autolink', 'tagfilter', 'strikethrough')


def markdown(text, options=None, extensions=None, renderer='html',
             width=0, state=None):
    """Parse text as markdown and render it into other format of string.

    :text: string of text.
    :options: list of options for cmark.
    :extensions: list of extensions.
    :renderer: renderer type or HTMLRenderer instance.
    :width: width option for renderers like man/latext.
    :state: MarkdownState instance for HTMLRenderer.
    :return: string
    """
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

        output = _render_root(
            renderer, root, _options, _extensions, width, state)
    finally:
        lib.cmark_parser_free(parser)
    return output


def html(text, options=None):
    """Parse text as markdown and render it into HTML string.

    :text: string of text.
    :options: list of options for cmark.
    :return: HTML string.
    """
    if options is None:
        options = []

    _options = get_options(*options)
    bytes_text = text.encode('utf-8')
    rv = lib.cmark_markdown_to_html(bytes_text, len(bytes_text), _options)
    return ffi.string(rv).decode('utf-8')


def attach_extensions(parser, *names):
    if not names:
        return ffi.NULL

    lib.cmark_gfm_core_extensions_ensure_registered()
    for name in names:
        extension = lib.cmark_find_syntax_extension(name.encode('utf-8'))
        if extension == ffi.NULL:
            raise ValueError('Invalid extensions: {!r}'.format(name))
        lib.cmark_parser_attach_syntax_extension(parser, extension)

    return lib.cmark_parser_get_syntax_extensions(parser)


def get_options(*options):
    value = lib.CMARK_OPT_DEFAULT
    for opt in options:
        value = value | opt
    return value


def _render_root(renderer, root, options, extensions, width, state):
    if callable(renderer):
        return renderer(root, options, state)
    elif renderer == 'html':
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
