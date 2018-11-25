import cffi

ffi = cffi.FFI()

with open('pedantmark/cmark_cdef.h', 'r') as f:
    CDEF_H = f.read()

with open('pedantmark/extern_cdef.h', 'r') as f:
    CDEF_H += f.read()

MODULE_H = '''
#ifndef CMARK_MODULE_H
#define CMARK_MODULE_H

#ifdef __cplusplus
extern "C" {
#endif

#define CMARKEXTENSIONS_STATIC_DEFINE

#include "cmark-gfm.h"
#include "cmark-gfm-extension_api.h"
#include "cmark-gfm-core-extensions.h"
#include "extern.h"

#ifdef __cplusplus
}
#endif

#endif
'''

SOURCES_FILES = '''
cmark-gfm/src/arena.c
cmark-gfm/src/blocks.c
cmark-gfm/src/buffer.c
cmark-gfm/src/cmark.c
cmark-gfm/src/cmark_ctype.c
cmark-gfm/src/commonmark.c
cmark-gfm/src/footnotes.c
cmark-gfm/src/houdini_href_e.c
cmark-gfm/src/houdini_html_e.c
cmark-gfm/src/houdini_html_u.c
cmark-gfm/src/html.c
cmark-gfm/src/inlines.c
cmark-gfm/src/iterator.c
cmark-gfm/src/latex.c
cmark-gfm/src/linked_list.c
cmark-gfm/src/man.c
cmark-gfm/src/map.c
cmark-gfm/src/node.c
cmark-gfm/src/plaintext.c
cmark-gfm/src/plugin.c
cmark-gfm/src/references.c
cmark-gfm/src/registry.c
cmark-gfm/src/render.c
cmark-gfm/src/scanners.c
cmark-gfm/src/syntax_extension.c
cmark-gfm/src/utf8.c
cmark-gfm/src/xml.c
cmark-gfm/extensions/autolink.c
cmark-gfm/extensions/core-extensions.c
cmark-gfm/extensions/ext_scanners.c
cmark-gfm/extensions/strikethrough.c
cmark-gfm/extensions/table.c
cmark-gfm/extensions/tagfilter.c
pedantmark/extern.c
'''

ffi.cdef(CDEF_H)
ffi.set_source(
    'pedantmark._cmark',
    MODULE_H,
    sources=SOURCES_FILES.split(),
    include_dirs=(
        'cmark-gfm/src',
        'cmark-gfm/extensions',
        'vendors/src',
        'vendors/extensions',
        'pedantmark',
    )
)

if __name__ == '__main__':
    import subprocess
    subprocess.call(['cmake', '../cmark-gfm'], cwd='vendors')
    ffi.compile(verbose=True)
