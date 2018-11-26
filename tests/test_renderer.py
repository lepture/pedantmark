import pedantmark
from pedantmark import markdown, HTMLRenderer


def test_strong():
    rv = markdown('**a**', renderer=HTMLRenderer())
    assert rv.strip() == '<p><strong>a</strong></p>'


def test_emph():
    rv = markdown('_a_', renderer=HTMLRenderer())
    assert rv.strip() == '<p><em>a</em></p>'


def test_strikethrough():
    rv = markdown('~a~', renderer=HTMLRenderer(), extensions=['strikethrough'])
    assert rv.strip() == '<p><del>a</del></p>'


def test_code():
    rv = markdown('`a`', renderer=HTMLRenderer())
    assert rv.strip() == '<p><code>a</code></p>'


def test_link():
    rv = markdown('[a](</a>)', renderer=HTMLRenderer())
    assert rv.strip() == '<p><a href="/a">a</a></p>'

    rv = markdown('[a](</a> "b")', renderer=HTMLRenderer())
    assert rv.strip() == '<p><a href="/a" title="b">a</a></p>'

    rv = markdown('[a](<javascript:void> "b")', renderer=HTMLRenderer())
    assert rv.strip() == '<p><a href="" title="b">a</a></p>'


def test_image():
    rv = markdown('![a](</a>)', renderer=HTMLRenderer())
    assert rv.strip() == '<p><img src="/a" alt="a" /></p>'

    # rv = markdown('![a](</a> "b")', renderer=HTMLRenderer())
    # assert rv.strip() == '<p><img src="/a" alt="a" title="b" /></p>'

    rv = markdown('![a](<javascript:void> "b")', renderer=HTMLRenderer())
    assert rv.strip() == '<p><!-- dangerous image --></p>'


def test_thematic_break():
    rv = markdown('***', renderer=HTMLRenderer())
    assert rv.strip() == '<hr />'


def test_block_quote():
    rv = markdown('> a', renderer=HTMLRenderer())
    assert rv.strip() == '<blockquote><p>a</p>\n</blockquote>'


def test_code_block():
    rv = markdown('    a\n', renderer=HTMLRenderer())
    assert rv.strip() == '<pre><code>a\n</code></pre>'

    rv = markdown('```c\na\n```', renderer=HTMLRenderer())
    assert rv.strip() == '<pre><code class="language-c">a\n</code></pre>'

    def highlight(code, lang):
        return b'test'

    rv = markdown('```c\na\n```', renderer=HTMLRenderer(highlight))
    assert rv == 'test'


def test_ordered_list():
    rv = markdown('1. a', renderer=HTMLRenderer())
    assert rv.strip() == '<ol>\n<li>a</li>\n</ol>'

    rv = markdown('5. a', renderer=HTMLRenderer())
    assert rv.strip() == '<ol start="5">\n<li>a</li>\n</ol>'


def test_unordered_list():
    rv = markdown('- a', renderer=HTMLRenderer())
    assert rv.strip() == '<ul>\n<li>a</li>\n</ul>'


def test_footnote():
    s = '[^1]\n\n[^1]: a'
    rv = markdown(
        s, renderer=HTMLRenderer(),
        options=[pedantmark.OPT_FOOTNOTES]
    )
    assert 'id="fn' in rv
    assert 'class="footnotes"' in rv


TABLE_TEXT_1 = '''
a1 | a2
-- | --
b1 | b2
'''

TABLE_TEXT_2 = '''
a1  | a2
:-- | :--:
b1  | b2
'''


def test_table():
    rv = markdown(
        TABLE_TEXT_1, renderer=HTMLRenderer(),
        extensions=['table'],
    )
    assert '<th>' in rv

    rv = markdown(
        TABLE_TEXT_2, renderer=HTMLRenderer(),
        extensions=['table'],
    )
    assert 'style=' in rv
