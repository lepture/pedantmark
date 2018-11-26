pedantmark
==========

    Only two maybes I've thought of: Strict Markdown or Pedantic Markdown. "Strict" still doesn't seem right.

    -- `John Gruber`_

.. _`John Gruber`: https://twitter.com/gruber/status/507615356295200770)

Ok, let's call it **pedantmark**.

**pedantmark** is (not only) a python binding for the GitHub's fork of CommonMark (cmark).
It has been enhanced by me (Hsiaoming Yang) to support custom renderers.

.. note::
   If you are a C pro, please help me to improve the C code in this repo.

Install
-------

**pedantmark** is available in Python 2.7 and 3.5+ for Linux and Mac,
Python 3.5+ for Windows. Wheels are built by multibuild_.

Install wheels by pip::

    $ pip install pedantmark

.. _multibuild: https://github.com/matthew-brett/multibuild


Standard Usage
--------------

The C source code has serval built-in renderers. The simplest interface is
``pedantmark.html(text, options)``, which will render text into HTML.

.. code-block:: python

    import pedantmark

    text = '...'
    html = pedantmark.html(text, options=[pedantmark.OPT_VALIDATE_UTF8])

The function ``pedantmark.html()`` accepts no extensions, but you can add
extensions via ``pedantmark.markdown()``:

.. code-block:: python

    import pedantmark

    text = '...'
    html = pedantmark.markdown(
        text,
        options=[pedantmark.OPT_VALIDATE_UTF8],
        extensions=['strikethrough', 'autolink', 'table'],
        renderer='html',
    )

Available extensions: ``table``, ``autolink``, ``tagfilter``, ``strikethrough``.
You can enable them all with a shortcut::

    pedantmark.markdown(..., extensions=pedantmark.EXTENSIONS)

Available renderers: ``html``, ``xml``, ``man``, ``commonmark``, ``plaintext``,
and ``latex``.

Custom Renderer
---------------

Besides the native renderers, **pedantmark** has provided you a custom renderer,
which you can customize the output yourself. Here is an example of pygments code
highlighting integration:

.. code-block:: python

    from pedantmark import HTMLRenderer, markdown
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import html

    class MyRenderer(HTMLRenderer):
        def code_block(self, code, lang):
            if lang:
                # everything is in bytes
                lang = lang.decode('utf-8')
                code = code.decode('utf-8')
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = html.HtmlFormatter()
                output = highlight(code, lexer, formatter)
                # return bytes
                return output.encode('utf-8')
            return super(MyRenderer, self).code_block(code, lang)

    text = '...'
    markdown(text, renderer=MyRenderer())

The default ``HTMLRenderer`` has a built-in hook for code highlight, you don't need
to subclass at all:

.. code-block:: python

    def add_code_highlight(code, lang):
        lang = lang.decode('utf-8')
        code = code.decode('utf-8')
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        output = highlight(code, lexer, formatter)
        return output.encode('utf-8')

    text = '...'
    markdown(text, renderer=HTMLRenderer(highlight=add_code_highlight))

Author & License
----------------

This library is created by Hsiaming Yang, licensed under BSD.
