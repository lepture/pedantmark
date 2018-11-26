from pedantmark import escape_html, escape_href


def test_escape_html():
    assert escape_html('<a>') == '&lt;a&gt;'


def test_escape_href():
    assert escape_href('http://a b') == 'http://a%20b'
