import sys
import glob
import cffi


INCLUDE_DIRS = [
    'cmark-gfm/src',
    'cmark-gfm/extensions',
    'pedantmark',
]
SOURCES_FILES = [
    f for f in glob.iglob('cmark-gfm/src/*.c') if not f.endswith('main.c')
]
SOURCES_FILES.extend(list(glob.iglob('cmark-gfm/extensions/*.c')))
SOURCES_FILES.append('pedantmark/extern.c')


def _compiler_type():
    import distutils.dist
    import distutils.ccompiler
    dist = distutils.dist.Distribution()
    dist.parse_config_files()
    cmd = dist.get_command_obj('build')
    cmd.ensure_finalized()
    compiler = distutils.ccompiler.new_compiler(compiler=cmd.compiler)
    return compiler.compiler_type


COMPILER_TYPE = _compiler_type()
if COMPILER_TYPE == 'unix':
    EXTRA_COMPILE_ARGS = ['-std=c99']
    INCLUDE_DIRS.append('vendors/unix/src')
    INCLUDE_DIRS.append('vendors/unix/extensions')
elif COMPILER_TYPE == 'msvc':
    EXTRA_COMPILE_ARGS = ['/TP']
    INCLUDE_DIRS.append('vendors/windows/src')
    INCLUDE_DIRS.append('vendors/windows/extensions')


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

ffi.cdef(CDEF_H)
ffi.set_source(
    'pedantmark._cmark',
    MODULE_H,
    sources=SOURCES_FILES,
    include_dirs=INCLUDE_DIRS,
    extra_compile_args=EXTRA_COMPILE_ARGS,
)

if __name__ == '__main__':
    ffi.compile(verbose=True)
