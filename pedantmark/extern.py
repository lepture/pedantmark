from ._cmark import lib, ffi


def escape_html(text, secure=False):
    source = text.encode('utf-8')
    rv = lib.escape_html(source, len(source), int(secure))
    return _to_s(rv)


def escape_href(url):
    source = url.encode('utf-8')
    rv = lib.escape_href(source, len(source))
    return _to_s(rv)


class MarkdownState(object):
    def __init__(self, toc_level=0):
        self.footnotes = []
        self.toc = []
        self.toc_level = toc_level


class HTMLRenderer(object):
    BREAK_TYPES = {'thematic_break', 'linebreak', 'softbreak'}
    TEXT_TYPES = {
        'document', 'html_block', 'block_quote', 'list_item',
        'table_row', 'table_header', 'table',
        'text', 'emph', 'strong', 'strikethrough',
        'code', 'html_inline', 'footnote_ref',
    }

    def __init__(self, highlight=None, hardbreaks=False, nobreaks=False):
        self._highlight = highlight
        self._hardbreaks = hardbreaks
        self._nobreaks = nobreaks

    def _unknown(self):
        return b'<!-- unknown -->'

    def __call__(self, root, options, state=None):
        if state is None:
            state = MarkdownState()
        userdata = ffi.new_handle((self, state))
        output = _to_b(lib.cmark_render_pedant(
            lib.pedant_render_node, root, options, userdata))

        if state.footnotes:
            text = b''.join(
                self.footnote_item(s, i+1)
                for i, s in enumerate(state.footnotes)
            )
            output += self.footnotes(text)
        return output.decode('utf-8')

    def none(self):
        return b''

    def custom_block(self, text):
        return b'TODO'

    def custom_inline(self, text):
        return b'TODO'

    def document(self, text):
        return text

    def thematic_break(self):
        """Rendering thematic break tag like ``<hr>``."""
        return b'<hr />\n'

    def html_block(self, text):
        """Rendering block level pure html content.

        :param text: text content of the html snippet.
        """
        return text

    def block_quote(self, text):
        """Rendering <blockquote> with the given text.

        :param text: text content of the blockquote.
        """
        return b'<blockquote>' + text + b'</blockquote>\n'

    def code_block(self, text, lang):
        """Rendering block level code. ``pre > code``.

        :param code: text content of the code block.
        :param lang: language of the given code.
        """
        if self._highlight and lang:
            return self._highlight(text, lang)
        out = b'<pre><code'
        if lang:
            out += b' class="language-' + lang + b'"'
        return out + b'>' + text + b'</code></pre>\n'

    def heading(self, text, level, index=None):
        """Rendering heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param index: index of this heading in TOC (if enabled).
        """
        tag = b'h' + str(level).encode('utf-8')
        out = b'<' + tag
        if index:
            out += b' id="toc-' + str(index).encode('utf-8') + b'"'
        return out + b'>' + text + b'</' + tag + b'>\n'

    def paragraph(self, text):
        """Rendering paragraph tags. Like ``<p>``."""
        return b'<p>' + text + b'</p>\n'

    def list_item(self, text):
        """Rendering list item snippet. Like ``<li>``."""
        return b'<li>' + text + b'</li>\n'

    def list(self, text, ordered, start=None):
        """Rendering list tags like ``<ul>`` and ``<ol>``.

        :param body: body contents of the list.
        :param ordered: whether this list is ordered or not.
        :param start: start property for ordered list ``<ol>``.
        """
        if not ordered:
            return b'<ul>\n' + text + b'</ul>\n'
        out = b'<ol'
        if start is not None and start != 1:
            out += b' start="' + str(start).encode('utf-8') + b'"'
        return out + b'>\n' + text + b'</ol>\n'

    def table_cell(self, text, tag, align=None):
        """Rendering a table cell. Like ``<th>`` ``<td>``.

        :param text: content of current table cell.
        :param tag: tag of ``th`` or ``td``.
        :param align: align of current table cell.
        """
        out = b'<' + tag
        if align:
            out += b' style="text-align:' + align + b'"'
        return out + b'>' + text + b'</' + tag + b'>\n'

    def table_row(self, text):
        """Render a row of a table.

        :param text: content of the table row.
        """
        return b'<tr>\n' + text + b'</tr>\n'

    def table_header(self, text):
        """Render thead row of a table.

        :param text: content of the table row.
        """
        return b'<thead><tr>\n' + text + b'</tr></thead>\n'

    def table(self, text):
        """Wrapper of the table content."""
        return b'<table>\n' + text + b'</table>\n'

    def softbreak(self):
        """Rendering soft linebreaks depending on options."""
        if self._hardbreaks:
            return self.linebreak()
        if self._nobreaks:
            return b' '
        return b'\n'

    def linebreak(self):
        """Rendering line break like ``<br />``."""
        return b'<br />\n'

    def html_inline(self, text):
        """Rendering inline level pure html content.

        :param text: text content of the html snippet.
        """
        return text

    def text(self, text):
        """Rendering plain text.

        :param text: text content.
        """
        return text

    def emph(self, text):
        """Rendering *emphasis* text.

        :param text: text content for emphasis.
        """
        return b'<em>' + text + b'</em>'

    def strong(self, text):
        """Rendering **strong** text.

        :param text: text content for emphasis.
        """
        return b'<strong>' + text + b'</strong>'

    def strikethrough(self, text):
        """Rendering ~~strikethrough~~ text.

        :param text: text content for strikethrough.
        """
        return b'<del>' + text + b'</del>'

    def code(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        return b'<code>' + text + b'</code>'

    def link(self, url, text, title):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param text: text content for description.
        :param title: title content for `title` attribute.
        """
        # autolink url ended with \n
        url = url.strip()
        out = b'<a href="' + url + b'"'
        if title:
            out += b' title="' + title + b'"'
        return out + b'>' + text + b'</a>'

    def image(self, src, alt, title):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param alt: alt text of the image.
        :param title: title text of the image.
        """
        out = b'<img src="' + src + b'"'
        if alt:
            out += b' alt="' + alt + b'"'
        if title:
            out += b' title="' + title + b'"'
        return out + b' />'

    def footnote_ref(self, key):
        """Rendering the ref anchor of a footnote.

        :param key: identity key for the footnote.
        """
        out = b'<sup class="footnote-ref"><a href="#fn' + key
        out += b'" id="fnref' + key + b'">'
        return out + key + b'</a></sup>'

    def footnote_item(self, text, index):
        """Rendering a footnote item.

        :param text: text content of the footnote.
        :param index: index of the footnote item.
        """
        ref_ix = str(index).encode('utf-8')
        out = b'<li id="fn' + ref_ix + b'">\n'
        backref = b' <a class="footnote-backref" href="#fnref' + ref_ix
        backref += b'">&#8617;</a>'
        i = text.rfind(b'</')
        if i == -1:
            return out + text + backref + b'<li>\n'
        return out + text[:i] + backref + text[i:] + b'<li>\n'

    def footnotes(self, text):
        """Wrapper for all footnotes.

        :param text: contents of all footnotes.
        """
        out = b'<section class="footnotes"><ol>\n'
        return out + text + b'</ol></section>\n'


_ALIGN_SHORTCUTS = {'l': b'left', 'c': b'center', 'r': b'right'}


@ffi.def_extern()
def pedant_render_node(buf, node, text, userdata):
    rndr, state = ffi.from_handle(userdata)
    node_type = _to_s(lib.pedant_get_node_type(node))

    result = None
    if node_type in rndr.TEXT_TYPES:
        func = getattr(rndr, node_type)
        result = func(_to_b(text))
    elif node_type in rndr.BREAK_TYPES:
        result = getattr(rndr, node_type)()
    elif node_type == 'heading':
        result = _render_heading(rndr, node, text, state)
    elif node_type == 'code_block':
        result = _render_code_block(rndr, node, text)
    elif node_type == 'list':
        result = _render_list(rndr, node, text)
    elif node_type == 'paragraph':
        result = _render_paragraph(rndr, node, text)
    elif node_type == 'link':
        result = _render_link(rndr, node, text)
    elif node_type == 'image':
        result = _render_link(rndr, node, text, False)
    elif node_type == 'footnote_def':
        state.footnotes.append(_to_b(text))
    elif node_type == 'table_cell':
        result = _render_table_cell(rndr, node, text)
    else:
        result = '<!-- unknown type: {} -->'.format(node_type).encode('utf-8')

    if result:
        lib.cmark_strbuf_puts(buf, result)


def _render_heading(rndr, node, text, state):
    level = lib.pedant_get_node_heading_level(node)
    text = _to_b(text)
    if level <= state.toc_level:
        state.toc.append((text, level))
        return rndr.heading(text, level, len(state.toc))
    return rndr.heading(text, level)


def _render_table_cell(rndr, node, text):
    info = _to_s(lib.pedant_get_node_table_cell_info(node))
    if info[0] == 'h':
        tag = b'th'
    else:
        tag = b'td'
    if len(info) < 2:
        return rndr.table_cell(_to_b(text), tag)
    return rndr.table_cell(_to_b(text), tag, _ALIGN_SHORTCUTS[info[1]])


def _render_paragraph(rndr, node, text):
    tight = lib.pedant_get_node_paragraph_tight(node)
    if tight:
        return rndr.text(_to_b(text))
    return rndr.paragraph(_to_b(text))


def _render_code_block(rndr, node, text):
    info = _to_b(lib.pedant_get_node_code_info(node))
    if info:
        lang = info.split(b' ', 1)[0]
    else:
        lang = None
    return rndr.code_block(_to_b(text), lang)


def _render_list(rndr, node, text):
    bullet = lib.pedant_get_node_list_bullet(node)
    if bullet:
        return rndr.list(_to_b(text), False)
    start = lib.pedant_get_node_list_start(node)
    return rndr.list(_to_b(text), True, start)


def _render_link(rndr, node, text, is_link=True):
    url = lib.pedant_get_node_link_url(node)
    title = lib.pedant_get_node_link_title(node)
    if is_link:
        return rndr.link(_to_b(url), _to_b(text), _to_b(title))
    return rndr.image(_to_b(url), _to_b(text), _to_b(title))


def _to_b(s):
    if s == ffi.NULL:
        return b''
    return ffi.string(s)


def _to_s(s):
    if s == ffi.NULL:
        return ''
    return ffi.string(s).decode('utf-8')
