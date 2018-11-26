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
