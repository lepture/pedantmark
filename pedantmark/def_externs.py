from ._cmark import ffi


@ffi.def_extern()
def rndr_header(node, userdata):
    rndr = ffi.from_handle(userdata)
    rndr.header(node)
