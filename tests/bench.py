# coding: utf-8

import os
import time
import functools


class benchmark(object):
    suites = []

    def __init__(self, name):
        self._name = name

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(text, loops=1000):
            start = time.clock()
            while loops:
                func(text)
                loops -= 1
            end = time.clock()
            return end - start
        # register
        benchmark.suites.append((self._name, wrapper))
        return wrapper

    @classmethod
    def bench(cls, text, loops=100):
        print('Parsing the CommonMark spec.txt %d times...' % loops)
        for name, func in cls.suites:
            try:
                total = func(text, loops=loops)
                print('{0}: {1}'.format(name, total))
            except ImportError:
                print('{0} is not available'.format(name))


@benchmark('pedantmark.html')
def benchmark_pedant_html(text):
    import pedantmark
    pedantmark.html(text)


@benchmark('pedantmark.markdown')
def benchmark_pedant_markdown(text):
    import pedantmark
    pedantmark.markdown(
        text,
        options=[pedantmark.OPT_FOOTNOTES],
        extensions=['autolink', 'strikethrough', 'table'],
        renderer='html',
    )


@benchmark('pedantmark.custom')
def benchmark_pedant_custom(text):
    import pedantmark
    pedantmark.markdown(
        text,
        options=[pedantmark.OPT_FOOTNOTES],
        extensions=['autolink', 'strikethrough', 'table'],
        renderer=pedantmark.HTMLRenderer(),
    )


@benchmark('misaka')
def benchmark_misaka(text):
    import misaka as m
    extensions = (
        m.EXT_NO_INTRA_EMPHASIS | m.EXT_FENCED_CODE | m.EXT_AUTOLINK |
        m.EXT_TABLES | m.EXT_STRIKETHROUGH
    )
    md = m.Markdown(m.HtmlRenderer(), extensions=extensions)
    md(text)


@benchmark('mistune')
def benchmark_mistune(text):
    import mistune
    mistune.markdown(text)


@benchmark('mistletoe')
def benchmark_mistletoe(text):
    import mistletoe
    mistletoe.markdown(text)


@benchmark('commonmark')
def benchmark_commonmark(text):
    import commonmark
    commonmark.commonmark(text)


@benchmark('markdown')
def benchmark_markdown(text):
    import markdown
    markdown.markdown(text, extensions=['extra'])


if __name__ == '__main__':
    root = os.path.dirname(__file__)
    filepath = os.path.join(root, 'spec.txt')
    with open(filepath, 'r') as f:
        text = f.read()

    benchmark.bench(text)
