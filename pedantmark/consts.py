from ._cmark import lib, ffi


DEFAULT_OPTION = lib.CMARK_OPT_DEFAULT

OPTIONS = {
    #: Include a `data-sourcepos` attribute on all block elements.
    'sourcepos': lib.CMARK_OPT_SOURCEPOS,

    #: Render `softbreak` elements as hard line breaks.
    'hardbreaks': lib.CMARK_OPT_HARDBREAKS,

    #: Render `softbreak` elements as spaces.
    'nobreaks': lib.CMARK_OPT_NOBREAKS,

    #: Validate UTF-8 in the input before parsing, replacing illegal
    #: sequences with the replacement character U+FFFD.
    'utf8': lib.CMARK_OPT_VALIDATE_UTF8,

    #: Convert straight quotes to curly, --- to em dashes, -- to en dashes.
    'smart': lib.CMARK_OPT_SMART,

    #: Use GitHub-style <pre lang="x"> tags for code blocks instead of
    #: <pre><code class="language-x">.
    'pre_lang': lib.CMARK_OPT_GITHUB_PRE_LANG,

    #: Be liberal in interpreting inline HTML tags.
    'liberal_html': lib.CMARK_OPT_LIBERAL_HTML_TAG,

    #: Parse footnotes.
    'footnotes': lib.CMARK_OPT_FOOTNOTES,

    #: Only parse strikethroughs if surrounded by exactly 2 tildes.
    'strict_strikethrough': lib.CMARK_OPT_STRIKETHROUGH_DOUBLE_TILDE,

    #: Use style attributes to align table cells instead of align attributes.
    'table_prefer_style': lib.CMARK_OPT_TABLE_PREFER_STYLE_ATTRIBUTES,

    #: Include the remainder of the info string in code blocks in
    #: a separate attribute.
    'full_info': lib.CMARK_OPT_FULL_INFO_STRING,

    #: Allow raw HTML and unsafe links, `javascript:`, `vbscript:`, `file:`,
    #: and all `data:` URLs -- by default, only `image/png`, `image/gif`,
    #: `image/jpeg`, or `image/webp` mime types are allowed. Without this
    #: option, raw HTML is replaced by a placeholder HTML comment, and unsafe
    #: links are replaced by empty strings.
    'unsafe': lib.CMARK_OPT_UNSAFE,
}


def get_options(*names):
    value = DEFAULT_OPTION
    for name in names:
        value = value | OPTIONS[name]
    return value


EXTENSIONS = {
    'table', 'autolink', 'tagfilter', 'strikethrough',
}


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
