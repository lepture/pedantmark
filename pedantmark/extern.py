from ._cmark import lib, ffi


def escape_html(text, secure=False):
    source = text.encode('utf-8')
    rv = lib.escape_html(source, len(source), int(secure))
    return ffi.string(rv).decode('utf-8')


class BaseRenderer(object):
    LITERAL_TYPES = {
        'document', 'html_block', 'text', 'strikethrough',
        'code', 'html_inline', 'paragraph',
    }

    def __init__(self):
        self._userdata = ffi.new_handle(self)

    def _unknown(self):
        return b'<!-- unknown -->'

    def __call__(self, root, options):
        return lib.cmark_render_pedant(
            lib.pedant_render_node, root, options, self._userdata)

    def document(self, text):
        return text

    def thematic_break(self):
        return b'<br />'

    def html_block(self, text):
        return text

    def code_block(self, text, lang):
        out = b'<pre><code'
        if lang:
            out += b' class="language-' + lang + b'"'
        return out + b'>' + text + b'</code></pre>\n'

    def paragraph(self, text):
        return b'<p>' + text + b'</p>'

    def text(self, text):
        return text

    def strikethrough(self, text):
        return b'<del>' + text + b'</del>'

    def code(self, text):
        return b'<code>' + text + b'</code>'

    def linebreak(self):
        return b'\n'

    def html_inline(self, text):
        return text


@ffi.def_extern()
def pedant_render_node(buf, node, text, userdata):
    rndr = ffi.from_handle(userdata)
    node_type = ffi.string(lib.pedant_get_node_type(node)).decode('utf-8')

    result = None
    if node_type in rndr.LITERAL_TYPES:
        func = getattr(rndr, node_type)
        result = func(ffi.string(text))
    elif node_type == 'code_block':
        result = rndr.code_block(ffi.string(text), lang=b'python')

    if result:
        lib.cmark_strbuf_puts(buf, result)
