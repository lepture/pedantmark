from ._cmark import lib, ffi


def escape_html(text, secure=False):
    source = text.encode('utf-8')
    rv = lib.escape_html(source, len(source), int(secure))
    return ffi.string(rv).decode('utf-8')


class BaseRenderer(object):
    def __init__(self):
        self._userdata = ffi.new_handle(self)

    def _unknown(self, node, entering):
        return '<!-- unknown -->'

    def __call__(self, root, options):
        return lib.cmark_render_pedant(
            lib.pedant_render_node, root, options, self._userdata)

    def strikethrough(self, text):
        return '<del>' + text + '</del>'


@ffi.def_extern()
def pedant_render_node(buf, node, text, options, userdata):
    rndr = ffi.from_handle(userdata)
    node_type = ffi.string(lib.pedant_get_node_type(node)).decode('utf-8')

    result = None
    if node_type == 'strikethrough':
        result = rndr.strikethrough(text)

    if result:
        lib.cmark_strbuf_puts(buf, result.encode('utf-8'))
