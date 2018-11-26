import pedantmark


TEXT = '''
# h

a `b` ~c~

<div></div>
'''


def test_default_html():
    html = pedantmark.html(TEXT)
    assert '<h1>h</h1>' in html
    assert '<code>b</code>' in html
    assert '~c~' in html
    assert 'omitted' in html

    html = pedantmark.html(TEXT, [pedantmark.OPT_UNSAFE])
    assert '<div></div>' in html


def test_markdown_html():
    html = pedantmark.markdown(TEXT, renderer='html')
    assert html == pedantmark.html(TEXT)

    html = pedantmark.markdown(
        TEXT, renderer='html',
        extensions=['strikethrough']
    )
    assert '<del>c</del>' in html

    html = pedantmark.markdown(
        TEXT, renderer='html',
        options=[pedantmark.OPT_STRIKETHROUGH_DOUBLE_TILDE],
        extensions=['strikethrough']
    )
    assert '~c~' in html


def test_markdown_man():
    rv = pedantmark.markdown(TEXT, renderer='man')
    assert r'\f[C]b\f[]' in rv


def test_markdown_latex():
    rv = pedantmark.markdown(TEXT, renderer='latex')
    assert r'\section{h}' in rv


def test_markdown_plaintext():
    rv = pedantmark.markdown(TEXT, renderer='plaintext')
    assert r'a b ~c~' in rv


def test_markdown_commonmark():
    rv = pedantmark.markdown(TEXT, renderer='commonmark')
    assert r'# h' in rv


def test_markdown_xml():
    rv = pedantmark.markdown(TEXT, renderer='xml')
    assert '<heading level="1">' in rv


def test_markdown_invalid():
    try:
        pedantmark.markdown(TEXT, renderer='invalid')
        success = True
    except ValueError:
        success = False
    assert success is False


def test_invalid_extension():
    try:
        pedantmark.markdown(TEXT, extensions=['invalid'])
        success = True
    except ValueError:
        success = False
    assert success is False
