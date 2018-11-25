pedantmark
==========

Usage
-----

Here is a simple usage::

    import pedantmark

    text = '''
    # level 1 head

    This is a ~~deleted~~ string[^1].

    [^1]: strikethrough is an extension.
    '''

    html = pedantmark.markdown(
        text,
        options=[pedantmark.OPT_VALIDATE_UTF8, pedantmark.OPT_FOOTNOTES],
        extensions=['strikethrough'],
    )
