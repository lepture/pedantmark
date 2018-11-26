Pedantic Markdown
=================

**pedantmark** is (not only) a python binding for the GitHub's fork of CommonMark (cmark).
It has also been enhanced to support custom renderers.

Install
-------

**pedantmark** is available in Python 2.7 and 3.5+ for Linux and Mac,
Python 3.5+ for Windows.

Install wheels by pip::

    $ pip install pedantmark

Usage
-----

A simple overview of how to use pedantmark:

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
``latex`` and custom renderers.

Author & License
----------------

This library is created by Hsiaming Yang, licensed under BSD.
