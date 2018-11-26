#!/usr/bin/env python
import re
import sys
from setuptools import setup
from setuptools.command.build_ext import build_ext

_version_re = re.compile(r"__version__ = '(.*)'")


with open('pedantmark/__init__.py', 'r') as f:
    version = _version_re.search(f.read()).group(1)


with open('README.rst') as f:
    long_description = f.read()


class custom_build_ext(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        is_windows = sys.platform == 'win32'
        is_py2 = sys.version_info[0] < 3
        if self.compiler is None and is_windows and is_py2:
            self.compiler = 'mingw32'


setup(
    name='pedantmark',
    version=version,
    description='Python binding of GitHub cmark with extensions and renderers',
    long_description=long_description,
    url='https://github.com/lepture/pedantmark',
    zip_safe=False,
    license='BSD',
    packages=['pedantmark'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=["cffi>=1.11.0"],
    setup_requires=["cffi>=1.11.0"],
    cffi_modules=["build_ffi.py:ffi"],
    cmdclass={'build_ext': custom_build_ext},
)
